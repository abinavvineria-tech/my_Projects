# Lighting Studio Component
# RGB/lighting controls for supported Portonics keyboards

from typing import Optional, List, Dict, Any
from enum import Enum
from .device import Capability, PortonicsDevice


class LightingEffect(Enum):
    """Supported lighting effects."""
    STATIC = "static"
    WAVE = "wave"
    BREATHING = "breathing"
    REACTIVE = "reactive"
    SPECTRUM = "spectrum"
    OFF = "off"


class LightingStudio:
    """RGB and lighting control center for Portonics keyboards."""

    def __init__(self, device: PortonicsDevice):
        self.device = device
        self._effect: LightingEffect = LightingEffect.OFF
        self._brightness: int = 50
        self._is_on: bool = False
        self._per_key_rgb: Dict[int, tuple[int, int, int]] = {}
        self._speed: int = 1
        self._direction: int = 0  # 0-3 for directions

    @property
    def supported(self) -> bool:
        """Check if this device supports RGB/lighting."""
        return self.device.has_capability(Capability.RGB) or \
               self.device.has_capability(Capability.LIGHTING_EFFECTS)

    def turn_on(self) -> Dict[str, Any]:
        """Turn on the keyboard lighting."""
        if not self.supported:
            return {"success": False, "reason": "Lighting not supported by this device"}
        self._is_on = True
        self._effect = LightingEffect.STATIC
        return {"success": True, "effect": self._effect.value, "on": True}

    def turn_off(self) -> Dict[str, Any]:
        """Turn off the keyboard lighting."""
        if not self.supported:
            return {"success": False, "reason": "Lighting not supported by this device"}
        self._is_on = False
        return {"success": True, "effect": self._effect.value, "on": False}

    def set_effect(self, effect: LightingEffect) -> Dict[str, Any]:
        """Set the lighting effect.

        Args:
            effect: The lighting effect to set.

        Returns:
            Operation result.
        """
        if not self.supported:
            return {"success": False, "reason": "Lighting not supported by this device"}
        self._effect = effect
        return {"success": True, "effect": effect.value}

    def set_brightness(self, brightness: int) -> Dict[str, Any]:
        """Set the brightness level (0-100).

        Args:
            brightness: Brightness percentage (0-100).

        Returns:
            Operation result.
        """
        if not self.supported:
            return {"success": False, "reason": "Lighting not supported by this device"}
        self._brightness = max(0, min(100, brightness))
        return {"success": True, "brightness": self._brightness}

    def set_speed(self, speed: int) -> Dict[str, Any]:
        """Set the effect speed.

        Args:
            speed: Speed level (1-10).

        Returns:
            Operation result.
        """
        if not self.supported:
            return {"success": False, "reason": "Lighting not supported by this device"}
        self._speed = max(1, min(10, speed))
        return {"success": True, "speed": self._speed}

    def set_direction(self, direction: int) -> Dict[str, Any]:
        """Set the lighting direction.

        Args:
            direction: Direction (0=none, 1=left, 2=right, 3=forward).

        Returns:
            Operation result.
        """
        if not self.supported:
            return {"success": False, "reason": "Lighting not supported by this device"}
        self._direction = direction % 4
        return {"success": True, "direction": self._direction}

    def set_per_key_rgb(self, key_code: int, r: int, g: int, b: int) -> Dict[str, Any]:
        """Set per-key RGB color.

        Args:
            key_code: The key code.
            r: Red component (0-255).
            g: Green component (0-255).
            b: Blue component (0-255).

        Returns:
            Operation result.
        """
        if not self.supported:
            return {"success": False, "reason": "Lighting not supported by this device"}
        self._per_key_rgb[key_code] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        return {"success": True, "color": (r, g, b)}

    def get_status(self) -> Dict[str, Any]:
        """Get current lighting status."""
        return {
            "on": self._is_on,
            "effect": self._effect.value,
            "brightness": self._brightness,
            "speed": self._speed,
            "direction": self._direction,
            "per_key_count": len(self._per_key_rgb),
            "supported": self.supported,
        }

    def get_disabled_reason(self) -> str:
        """Get reason why lighting is disabled."""
        if not self.device.has_capability(Capability.RGB):
            return "RGB controls not available"
        if not self.device.has_capability(Capability.LIGHTING_EFFECTS):
            return "Lighting effects not available"
        return ""


class LightingStateView:
    """UI-friendly lighting state representation."""

    @staticmethod
    def from_device(device: PortonicsDevice) -> Dict[str, Any]:
        """Create a lighting state view from device capabilities.

        Args:
            device: The PortonicsDevice instance.

        Returns:
            Dictionary with lighting state info for UI display.
        """
        has_rgb = device.has_capability(Capability.RGB)
        has_effects = device.has_capability(Capability.LIGHTING_EFFECTS)

        if not has_rgb and not has_effects:
            return {
                "available": False,
                "message": "Lighting controls not available for this device",
                "disabled": True,
            }

        return {
            "available": True,
            "rgb_supported": has_rgb,
            "effects_supported": has_effects,
            "disabled": False,
        }