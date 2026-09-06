# Portonics Protocol Adapter Architecture
# Extensible protocol adapters for different Portonics keyboard models

from abc import ABC, abstractmethod
from .device import PortonicsDevice, Capability


class PortonicsProtocolAdapter(ABC):
    """Base protocol adapter for Portonics keyboards."""

    @property
    @abstractmethod
    def supported_model(self) -> str:
        """The model this adapter supports."""

    @property
    @abstractmethod
    def capabilities(self) -> list[Capability]:
        """Capabilities supported by this adapter."""

    @abstractmethod
    def detect_device(self, device_info: dict) -> bool:
        """Detect if a device matches this adapter's model.

        Args:
            device_info: Dictionary with device identification info
                (name, product_id, vendor_id, etc.)

        Returns:
            True if this adapter can handle the device.
        """

    @abstractmethod
    def update_device_info(self, device: PortonicsDevice) -> PortonicsDevice:
        """Update device info after detection.

        Args:
            device: The device to update.

        Returns:
            Updated device with model-specific info.
        """

    @abstractmethod
    def test_key(self, key_code: int) -> dict:
        """Test a physical key press.

        Args:
            key_code: The key code from the HID event.

        Returns:
            Dictionary with key test result.
        """


class GenericHIDAdapter(PortonicsProtocolAdapter):
    """Generic HID adapter providing basic functionality.

    Provides safe basic functionality such as device detection
    and key testing for keyboards without specific protocol support.
    """

    @property
    def supported_model(self) -> str:
        return "Generic Portonics HID"

    @property
    def capabilities(self) -> list[Capability]:
        return [
            Capability.KEY_TESTING,
        ]

    def detect_device(self, device_info: dict) -> bool:
        """Detect generic Portonics HID keyboards via name/vendor."""
        name = device_info.get("name", "").lower()
        vendor = device_info.get("vendor", "").lower()
        return (
            "portonics" in name
            or "portonics" in vendor
            or "hydra" in name
            or "bubble" in name
        )

    def update_device_info(self, device: PortonicsDevice) -> PortonicsDevice:
        """Update device with generic HID info."""
        if not device.model:
            device.model = "Generic Portonics Keyboard"
        device.capabilities = [Capability.KEY_TESTING]
        return device

    def test_key(self, key_code: int) -> dict:
        """Test a key press - generic HID implementation."""
        return {
            "key_code": key_code,
            "key_name": f"Key {key_code}",
            "pressed": True,
            "supported": True,
        }


class Hydra10Adapter(PortonicsProtocolAdapter):
    """Adapter for Portonics Hydra 10 keyboard."""

    @property
    def supported_model(self) -> str:
        return "Hydra 10"

    @property
    def capabilities(self) -> list[Capability]:
        return [
            Capability.KEY_TESTING,
            Capability.BATTERY,
        ]

    def detect_device(self, device_info: dict) -> bool:
        """Detect Hydra 10 by name or product ID."""
        name = device_info.get("name", "").lower()
        return "hydra 10" in name or "hydra10" in name

    def update_device_info(self, device: PortonicsDevice) -> PortonicsDevice:
        """Update device with Hydra 10-specific info."""
        device.model = "Hydra 10"
        device.capabilities = [Capability.KEY_TESTING, Capability.BATTERY]
        return device

    def test_key(self, key_code: int) -> dict:
        """Test a key press on Hydra 10."""
        return {
            "key_code": key_code,
            "key_name": f"Hydra 10 Key {key_code}",
            "pressed": True,
            "supported": True,
        }


class Bubble30Adapter(PortonicsProtocolAdapter):
    """Adapter for Portonics Bubble 3.0 keyboard."""

    @property
    def supported_model(self) -> str:
        return "Bubble 3.0"

    @property
    def capabilities(self) -> list[Capability]:
        return [
            Capability.KEY_TESTING,
            Capability.BATTERY,
        ]

    def detect_device(self, device_info: dict) -> bool:
        """Detect Bubble 3.0 by name."""
        name = device_info.get("name", "").lower()
        return "bubble 3.0" in name or "bubble30" in name

    def update_device_info(self, device: PortonicsDevice) -> PortonicsDevice:
        """Update device with Bubble 3.0-specific info."""
        device.model = "Bubble 3.0"
        device.capabilities = [Capability.KEY_TESTING, Capability.BATTERY]
        return device

    def test_key(self, key_code: int) -> dict:
        """Test a key press on Bubble 3.0."""
        return {
            "key_code": key_code,
            "key_name": f"Bubble 3.0 Key {key_code}",
            "pressed": True,
            "supported": True,
        }