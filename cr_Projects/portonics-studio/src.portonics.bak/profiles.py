# Profiles Component
# Profile management for Portonics Studio

import json
import os
from typing import Dict, List, Optional, Any
from enum import Enum
from .device import PortonicsDevice, Capability
from .key_customization import KeyRemapEntry, RemapAction


class ProfileName(Enum):
    """Default profile names."""
    DEFAULT = "Default"
    GAMING = "Gaming"
    CODING = "Coding"
    TABLET = "Tablet"
    CUSTOM = "Custom"


class Profile:
    """A profile containing key remappings and settings."""

    def __init__(self, name: str = ProfileName.DEFAULT.value, 
                 description: str = ""):
        self.name = name
        self.description = description
        self.remappings: Dict[int, KeyRemapEntry] = {}
        self.last_modified = os.path.getmtime(__file__) if os.path.exists(__file__) else 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "remappings": {
                str(k): v.to_dict() for k, v in self.remappings.items()
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Profile":
        """Create profile from dictionary."""
        profile = cls(name=data.get("name", ProfileName.DEFAULT.value),
                      description=data.get("description", ""))
        for key_str, entry_data in data.get("remappings", {}).items():
            key_code = int(key_str)
            entry = KeyRemapEntry.from_dict(entry_data)
            profile.remappings[key_code] = entry
        return profile


class ProfilesManager:
    """Manage saved profiles locally on the device."""

    PROFILES_DIR = "profiles"

    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.profiles: Dict[str, Profile] = {}
        self._current_profile_name: Optional[str] = None
        self._ensure_profiles_dir()

    def _ensure_profiles_dir(self):
        """Ensure the profiles directory exists."""
        profiles_dir = os.path.join(self.base_path, self.PROFILES_DIR)
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir, exist_ok=True)

    def list_profiles(self) -> List[Dict[str, Any]]:
        """List all saved profiles.

        Returns:
            List of profile summaries.
        """
        profiles_dir = os.path.join(self.base_path, self.PROFILES_DIR)
        profiles = []
        
        # Load any existing profile files
        if os.path.exists(profiles_dir):
            for filename in os.listdir(profiles_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(profiles_dir, filename)
                    try:
                        with open(filepath, "r") as f:
                            data = json.load(f)
                        profile = Profile.from_dict(data)
                        profile.filepath = filepath
                        self.profiles[profile.name] = profile
                        profiles.append({
                            "name": profile.name,
                            "description": profile.description,
                            "remapping_count": len(profile.remappings),
                            "is_current": profile.name == self._current_profile_name,
                        })
                    except (json.JSONDecodeError, Exception) as e:
                        logger.warning(f"Failed to load profile {filename}: {e}")
        
        return profiles or self._get_default_profiles()

    def _get_default_profiles(self) -> List[Dict[str, Any]]:
        """Return default profile information without loading from disk."""
        return [
            {
                "name": profile.value,
                "description": f"{profile.value} profile for Portonics Studio",
                "remapping_count": 0,
                "is_current": self._current_profile_name == profile.value,
            }
            for profile in ProfileName
        ]

    def create_profile(self, name: str, description: str = "") -> Profile:
        """Create a new profile.

        Args:
            name: The profile name.
            description: Optional description.

        Returns:
            The newly created profile.
        """
        profile = Profile(name=name, description=description)
        self.profiles[name] = profile
        self._save_profile(profile)
        return profile

    def rename_profile(self, old_name: str, new_name: str) -> bool:
        """Rename a profile.

        Args:
            old_name: Current profile name.
            new_name: New profile name.

        Returns:
            True if renamed successfully.
        """
        if old_name not in self.profiles:
            return False
        if new_name in self.profiles:
            return False
        
        profile = self.profiles.pop(old_name)
        profile.name = new_name
        self.profiles[new_name] = profile
        self._save_profile(profile)
        return True

    def duplicate_profile(self, source_name: str, new_name: str) -> bool:
        """Duplicate a profile.

        Args:
            source_name: Profile to duplicate.
            new_name: Name for the new profile.

        Returns:
            True if duplicated successfully.
        """
        if source_name not in self.profiles:
            return False
        if new_name in self.profiles:
            return False
        
        source_profile = self.profiles[source_name]
        new_profile = Profile(name=new_name, description=f"Duplicate of {source_name}")
        new_profile.remappings = dict(source_profile.remappings)
        self.profiles[new_name] = new_profile
        self._save_profile(new_profile)
        return True

    def delete_profile(self, name: str) -> bool:
        """Delete a profile.

        Args:
            name: Profile name to delete.

        Returns:
            True if deleted successfully.
        """
        if name == ProfileName.DEFAULT.value:
            return False  # Prevent deleting default profile
        
        if name not in self.profiles:
            return False
        
        filepath = self.profiles[name].filepath
        try:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
            del self.profiles[name]
            return True
        except Exception as e:
            logger.error(f"Failed to delete profile {name}: {e}")
            return False

    def activate_profile(self, name: str) -> bool:
        """Activate a profile.

        Args:
            name: Profile name to activate.

        Returns:
            True if activated successfully.
        """
        if name not in self.profiles:
            return False
        
        self._current_profile_name = name
        self._save_current_profile_marker()
        return True

    def get_current_profile(self) -> Optional[Profile]:
        """Get the currently active profile.

        Returns:
            The active profile, or None if no profile is active.
        """
        if self._current_profile_name and self._current_profile_name in self.profiles:
            return self.profiles[self._current_profile_name]
        return None

    def get_profile(self, name: str) -> Optional[Profile]:
        """Get a profile by name.

        Args:
            name: Profile name.

        Returns:
            The profile, or None if not found.
        """
        return self.profiles.get(name)

    def save_remappings_to_profile(self, profile_name: str, 
                                    remappings: Dict[int, KeyRemapEntry]) -> bool:
        """Save key remappings to a profile.

        Args:
            profile_name: The profile name.
            remappings: The remappings to save.

        Returns:
            True if saved successfully.
        """
        if profile_name not in self.profiles:
            return False
        
        profile = self.profiles[profile_name]
        profile.remappings = remappings
        return self._save_profile(profile)

    def _save_profile(self, profile: Profile) -> bool:
        """Save a profile to disk.

        Args:
            profile: The profile to save.

        Returns:
            True if saved successfully.
        """
        profiles_dir = os.path.join(self.base_path, self.PROFILES_DIR)
        filepath = os.path.join(profiles_dir, f"{profile.name}.json")
        
        try:
            with open(filepath, "w") as f:
                json.dump(profile.to_dict(), f, indent=2)
            profile.filepath = filepath
            return True
        except Exception as e:
            logger.error(f"Failed to save profile {profile.name}: {e}")
            return False

    def _save_current_profile_marker(self):
        """Save a marker file for the current profile."""
        marker_path = os.path.join(self.base_path, "current_profile.json")
        if self._current_profile_name:
            with open(marker_path, "w") as f:
                json.dump({"current_profile": self._current_profile_name}, f)
        else:
            with open(marker_path, "w") as f:
                json.dump({"current_profile": None}, f)