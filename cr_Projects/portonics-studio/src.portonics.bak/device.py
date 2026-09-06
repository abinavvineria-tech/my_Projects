# Portonics Device Abstraction Layer
# Defines the device model and capability system

from enum import Enum, auto


class ConnectionType(Enum):
    BLUETOOTH = "Bluetooth"
    USB = "USB"
    WIRED = "Wired"


class Capability(Enum):
    KEY_TESTING = auto()
    BATTERY = auto()
    RGB = auto()
    LIGHTING_EFFECTS = auto()
    BRIGHTNESS = auto()
    MACROS = auto()
    KEY_REMAP = auto()
    PROFILE_STORAGE = auto()
    FIRMWARE_UPDATE = auto()


class DeviceState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    SCANNING = "scanning"


class PortonicsDevice:
    """Abstraction for a Portonics keyboard device."""

    def __init__(
        self,
        model: str = "",
        vendor: str = "Portonics",
        connection_type: ConnectionType = ConnectionType.BLUETOOTH,
        battery_level: int | None = None,
        firmware_version: str = "",
        capabilities: list[Capability] | None = None,
        connection_state: DeviceState = DeviceState.DISCONNECTED,
    ):
        self.model = model
        self.vendor = vendor
        self.connection_type = connection_type
        self.battery_level = battery_level
        self.firmware_version = firmware_version
        self.capabilities = capabilities if capabilities else []
        self.connection_state = connection_state
        self.last_connected = ""

    @property
    def battery_percentage(self) -> str | None:
        if self.battery_level is not None:
            return f"{self.battery_level}%"
        return None

    def has_capability(self, cap: Capability) -> bool:
        """Check if the device has a specific capability.

        Args:
            cap: The capability to check.

        Returns:
            True if the device has the capability, False otherwise.
        """
        return cap in self.capabilities

    def get_capability_string(self) -> str:
        """Return a human-readable capability string."""
        caps = []
        if self.has_capability(Capability.KEY_TESTING):
            caps.append("Key Testing ✓")
        if self.has_capability(Capability.BATTERY):
            caps.append("Battery ✓")
        if self.has_capability(Capability.RGB):
            caps.append("RGB ✓")
        if self.has_capability(Capability.LIGHTING_EFFECTS):
            caps.append("Lighting Effects ✓")
        if self.has_capability(Capability.MACROS):
            caps.append("Macros ✓")
        if self.has_capability(Capability.KEY_REMAP):
            caps.append("Key Remap ✓")
        if self.has_capability(Capability.PROFILE_STORAGE):
            caps.append("Profile Storage ✓")
        if self.has_capability(Capability.FIRMWARE_UPDATE):
            caps.append("Firmware Update ✓")
        return "  ".join(caps) if caps else "—"

    def __repr__(self):
        return f"PortonicsDevice(model={self.model}, state={self.connection_state.value})"