# Device Detection Layer
# Handles Bluetooth and USB HID keyboard detection on Android

import logging
from typing import Optional, Dict, Any, List
from .device import PortonicsDevice, ConnectionType, Capability, DeviceState
from .protocol import PortonicsProtocolAdapter, GenericHIDAdapter, Hydra10Adapter, Bubble30Adapter

logger = logging.getLogger(__name__)


class DeviceDetector:
    """Discovers and identifies Portonics keyboards connected via Bluetooth or USB."""

    def __init__(self):
        self._adapters: List[PortonicsProtocolAdapter] = [
            Hydra10Adapter(),
            Bubble30Adapter(),
            GenericHIDAdapter(),
        ]
        self._connected_device: Optional[PortonicsDevice] = None
        self._scanning = False

    def detect_devices(self) -> List[PortonicsDevice]:
        """Scan for and detect all connected Portonics keyboards."""
        devices = []
        # Check Bluetooth devices
        bt_devices = self._scan_bluetooth()
        devices.extend(bt_devices)
        # Check USB devices
        usb_devices = self._scan_usb()
        devices.extend(usb_devices)
        return devices

    def _scan_bluetooth(self) -> List[PortonicsDevice]:
        """Scan for Bluetooth HID keyboards."""
        devices = []
        try:
            # In a real Android implementation, this would use
            # the Android Bluetooth APIs via Plyer or direct JNI
            # For now, we simulate the detection pattern
            logger.info("Scanning Bluetooth HID keyboards...")
            # Placeholder - actual implementation would use Android Bluetooth
        except Exception as e:
            logger.error(f"Bluetooth scan error: {e}")
        return devices

    def _scan_usb(self) -> List[PortonicsDevice]:
        """Scan for USB HID keyboards."""
        devices = []
        try:
            # In a real Android implementation, this would use
            # Android USB host API
            logger.info("Scanning USB HID keyboards...")
            # Placeholder - actual implementation would use Android USB
        except Exception as e:
            logger.error(f"USB scan error: {e}")
        return devices

    def identify_device(self, device_info: dict) -> Optional[PortonicsDevice]:
        """Identify a Portonics keyboard from device info.

        Args:
            device_info: Dictionary with device identification info:
                - name: Device name
                - vendor: Vendor string
                - product_id: Product ID
                - vendor_id: Vendor ID
                - connection_type: Bluetooth or USB

        Returns:
            PortonicsDevice if identified, None otherwise.
        """
        device = PortonicsDevice()
        device.connection_type = ConnectionType(
            device_info.get("connection_type", "bluetooth").lower()
        )

        # Try each adapter to find a match
        for adapter in self._adapters:
            if adapter.detect_device(device_info):
                device = adapter.update_device_info(device)
                device.connection_state = DeviceState.CONNECTED
                logger.info(f"Identified device: {adapter.supported_model}")
                return device

        # If no specific adapter matches, use generic HID
        device = GenericHIDAdapter().update_device_info(device)
        device.connection_state = DeviceState.CONNECTED
        logger.info("Identified as generic Portonics HID keyboard")
        return device

    @property
    def connected_device(self) -> Optional[PortonicsDevice]:
        """Return the currently connected device."""
        return self._connected_device

    @connected_device.setter
    def connected_device(self, device: PortonicsDevice):
        self._connected_device = device
        device.connection_state = DeviceState.CONNECTED

    def disconnect(self):
        """Disconnect the current device."""
        if self._connected_device:
            self._connected_device.connection_state = DeviceState.DISCONNECTED
            self._connected_device = None