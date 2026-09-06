# Key Customization Component
# Key remapping interface for compatible devices

from typing import Optional, Dict, List, Any
from enum import Enum
from .device import Capability, PortonicsDevice


class RemapAction(Enum):
    """Possible remapping actions."""
    NORMAL_KEY = "normal"
    SHORTCUT = "shortcut"
    MEDIA_CONTROL = "media_control"
    APP_SHORTCUT = "app_shortcut"
    MACRO = "macro"
    DISABLE = "disable"


class KeyRemapEntry:
    """A single key remapping configuration."""

    def __init__(self, key_code: int, action: RemapAction, details: Optional[Dict] = None):
        self.key_code = key_code
        self.action = action
        self.details = details or {}
        self.applied = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "key_code": self.key_code,
            "action": self.action.value,
            "details": self.details,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KeyRemapEntry":
        """Create from dictionary."""
        action = RemapAction(data.get("action", "normal"))
        return cls(
            key_code=data.get("key_code", 0),
            action=action,
            details=data.get("details"),
        )


class KeyCustomization:
    """Key remapping and customization interface."""

    def __init__(self, device: PortonicsDevice):
        self.device = device
        self.remappings: Dict[int, KeyRemapEntry] = {}
        self._supported_actions: List[RemapAction] = []

    @property
    def supported(self) -> bool:
        """Check if this device supports key remapping."""
        return self.device.has_capability(Capability.KEY_REMAP)

    def can_remap(self, key_code: int) -> bool:
        """Check if a specific key can be remapped."""
        if not self.supported:
            return False
        # All keys can potentially be remapped on supported devices
        return key_code in self._get_available_keys()

    def _get_available_keys(self) -> List[int]:
        """Get list of available key codes for remapping."""
        # Return basic keyboard key codes
        return list(range(4, 200))  # Common HID key codes

    def remap_key(self, key_code: int, action: RemapAction, details: Optional[Dict] = None) -> Optional[KeyRemapEntry]:
        """Remap a key to a new action.

        Args:
            key_code: The key code to remap.
            action: The action to map the key to.
            details: Additional action details.

        Returns:
            The remap entry if successful, None if not supported.
        """
        if not self.supported:
            return None

        # Verify the key can be remapped
        if not self.can_remap(key_code):
            return None

        entry = KeyRemapEntry(key_code=key_code, action=action, details=details)
        self.remappings[key_code] = entry
        entry.applied = True
        return entry

    def unremap_key(self, key_code: int) -> bool:
        """Unremap a key.

        Args:
            key_code: The key code to unremap.

        Returns:
            True if unremapping was successful.
        """
        if key_code in self.remappings:
            del self.remappings[key_code]
            return True
        return False

    def get_remapping(self, key_code: int) -> Optional[KeyRemapEntry]:
        """Get the current remapping for a key.

        Args:
            key_code: The key code to check.

        Returns:
            The remap entry if configured, None otherwise.
        """
        return self.remappings.get(key_code)

    def get_all_remappings(self) -> Dict[int, KeyRemapEntry]:
        """Get all current key remappings."""
        return self.remappings.copy()

    def save_to_profile(self, profile_name: str) -> bool:
        """Save remappings to a profile.

        Args:
            profile_name: The profile name to save to.

        Returns:
            True if saved successfully.
        """
        if not self.supported:
            return False
        # In a real implementation, this would persist the remappings
        # to the profile storage system
        logger.info(f"Saving remappings to profile: {profile_name}")
        return True

    def get_supported_actions(self) -> List[str]:
        """Get list of supported remap action types as strings."""
        if not self.supported:
            return []
        return [action.value for action in self._get_available_actions()]

    def _get_available_actions(self) -> List[RemapAction]:
        """Get available remap actions based on device capabilities."""
        actions = [RemapAction.NORMAL_KEY]
        if self.device.has_capability(Capability.MACROS):
            actions.append(RemapAction.MACRO)
        if self.device.has_capability(Capability.KEY_REMAP):
            actions.extend([
                RemapAction.SHORTCUT,
                RemapAction.MEDIA_CONTROL,
                RemapAction.APP_SHORTCUT,
            ])
        actions.append(RemapAction.DISABLE)
        return actions