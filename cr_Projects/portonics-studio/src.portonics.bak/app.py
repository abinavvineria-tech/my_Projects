# Portonics Studio - Main Toga Application
import toga
from toga.style import Pack
from toga.colors import WHITE, BLACK

from .config import app_name, app_id, app_version, app_description
from .device import PortonicsDevice, ConnectionType, DeviceState, Capability
from .detection import DeviceDetector
from .keyboard_tester import KeyboardTester
from .lighting_studio import LightingStudio, LightingEffect
from .profiles import ProfilesManager, ProfileName


class PortonicsStudioApp(toga.App):
    """Main Portonics Studio application."""

    def __init__(self, **kwargs):
        super().__init__(
            formal_name=app_name,
            app_id=app_id,
            version=app_version,
            description=app_description,
            **kwargs,
        )

        # Initialize components
        self.detector = DeviceDetector()
        self.keyboard_tester = KeyboardTester()
        self.profiles_manager = ProfilesManager()
        self.lighting_studio: Optional[LightingStudio] = None
        self.current_device: Optional[PortonicsDevice] = None

        # UI references
        self.main_window = None
        self.sidebar = None
        self.content_area = None
        self.device_card = None
        self.key_tester_view = None
        self.lighting_view = None

        # State
        self.theme = "dark"  # or "light"
        self.notifications_enabled = True

    def startup(self):
        """Build the Toga application."""
        self.main_window = toga.MainWindow(title=f"{app_name} {app_version}")

        # Build the main dashboard
        self._build_dashboard()

        # Set the content
        self.main_window.content = self._create_main_content()

        # Show the main window
        self.main_window.show()

    def _create_main_content(self):
        """Create the main content area."""
        box = toga.Box(style=Pack(direction="column", flex=1))

        # Header
        header = toga.Box(style=Pack(
            padding=10,
            background_color=self._get_bg_color(),
            flex=0,
            height=50
        ))
        title = toga.Label(
            "Portonics Studio",
            style=Pack(font_size=20, font_weight="bold", color=WHITE)
        )
        header.add(title)

        # Theme toggle
        theme_toggle = toga.Switch(
            "Dark Mode",
            on_change=self._on_theme_toggle,
            style=Pack(padding=(10, 0))
        )
        header.add(theme_toggle)

        box.add(header)

        # Content stack - will switch between views
        self.content_stack = toga.Box(style=Pack(flex=1, direction="column"))
        box.add(self.content_stack)

        # Show dashboard initially
        self._show_dashboard()

        return box

    def _get_bg_color(self):
        """Get background color based on theme."""
        if self.theme == "dark":
            return "#1e1e1e"
        return "white"

    def _show_dashboard(self):
        """Show the home dashboard."""
        self._clear_content_stack()

        # Dashboard card
        self.device_card = toga.Box(
            style=Pack(
                padding=20,
                background_color="#252526",
                border_radius=8,
                margin=10,
                flex=0,
                height=150,
            )
        )

        # Device info in card
        self._update_device_card()

        self.content_stack.add(self.device_card)

        # Action buttons row
        actions_box = toga.Box(style=Pack(direction="row", padding=10, flex=1))
        
        customize_btn = toga.Button(
            "Customize",
            on_press=self._on_customize,
            style=Pack(flex=1, padding=5)
        )
        test_keys_btn = toga.Button(
            "Test Keys",
            on_press=self._on_test_keys,
            style=Pack(flex=1, padding=5)
        )
        device_info_btn = toga.Button(
            "Device Info",
            on_press=self._on_device_info,
            style=Pack(flex=1, padding=5)
        )

        actions_box.add(customize_btn)
        actions_box.add(test_keys_btn)
        actions_box.add(device_info_btn)

        self.content_stack.add(actions_box)

    def _clear_content_stack(self):
        """Clear the content stack."""
        self.content_stack.children = []

    def _update_device_card(self):
        """Update the device card with current device info."""
        if not self.current_device:
            # No device connected
            self.device_card.children = [
                toga.Label(
                    "No device connected",
                    style=Pack(padding=10, color="white", font_size=14)
                )
            ]
            return

        # Build device info text
        info_lines = [
            f"{self.current_device.model}",
        ]

        conn_type = self.current_device.connection_type.value
        info_lines.append(f"Connected via {conn_type}")

        # Battery
        battery = self.current_device.battery_percentage
        if battery:
            info_lines.append(f"Battery: {battery}")

        # Firmware
        if self.current_device.firmware_version:
            info_lines.append(f"Firmware: {self.current_device.firmware_version}")

        # Capabilities
        caps = self.current_device.get_capability_string()
        info_lines.append(f"Capabilities: {caps}")

        # Last connected
        if self.current_device.last_connected:
            info_lines.append(f"Last connected: {self.current_device.last_connected}")

        self.device_card.children = [
            toga.Label(
                "\n".join(info_lines),
                style=Pack(padding=10, color="white", font_size=12)
            )
        ]

        # Buttons
        actions = toga.Box(style=Pack(direction="row", padding=5, margin_top=5))
        
        customize_btn = toga.Button(
            "Customize",
            on_press=self._on_customize,
            style=Pack(flex=1, padding=3)
        )
        test_keys_btn = toga.Button(
            "Test Keys",
            on_press=self._on_test_keys,
            style=Pack(flex=1, padding=3)
        )
        device_info_btn = toga.Button(
            "Device Info",
            on_press=self._on_device_info,
            style=Pack(flex=1, padding=3)
        )

        actions.add(customize_btn)
        actions.add(test_keys_btn)
        actions.add(device_info_btn)

        # Replace card children with updated version
        self.device_card.children = [
            toga.Label(
                "\n".join(info_lines),
                style=Pack(padding=10, color="white", font_size=12)
            ),
            actions
        ]

    def _on_customize(self, widget):
        """Handle Customize button press."""
        if not self.current_device:
            return

        self._show_customization_view()

    def _on_test_keys(self, widget):
        """Handle Test Keys button press."""
        if not self.current_device:
            return

        self._show_key_tester()

    def _on_device_info(self, widget):
        """Handle Device Info button press."""
        if not self.current_device:
            return

        self._show_device_info_view()

    def _show_customization_view(self):
        """Show the key customization view."""
        self._clear_content_stack()

        back_btn = toga.Button(
            "Back",
            on_press=self._show_dashboard,
            style=Pack(padding=5, margin=5)
        )
        self.content_stack.add(back_btn)

        title = toga.Label(
            "Key Customization",
            style=Pack(padding=10, font_size=16, font_weight="bold")
        )
        self.content_stack.add(title)

        if not self.current_device:
            msg = toga.Label(
                "No device connected",
                style=Pack(padding=10, color="white")
            )
            self.content_stack.add(msg)
            return

        if not self.current_device.has_capability(Capability.KEY_REMAP):
            msg = toga.Label(
                "Key remapping not supported by this device",
                style=Pack(padding=10, color="white")
            )
            self.content_stack.add(msg)
            return

        # Create a scrollable area for key remappings
        scroll = toga.ScrollView(style=Pack(flex=1, padding=10))

        # Build key remapping interface
        remappings_box = toga.Box(style=Pack(direction="column", flex=1))

        # Header info
        info = toga.Label(
            "Configure key remappings for your keyboard",
            style=Pack(padding=5, color="white")
        )
        remappings_box.add(info)

        # Get current remappings
        current_remaps = self.detector.connected_device.remappings if self.detector.connected_device else {}

        # Create remap entries for common keys
        from .key_customization import KeyRemapEntry, RemapAction

        # Action selector
        action_label = toga.Label(
            "Action:",
            style=Pack(padding=(5, 0), color="white")
        )
        remappings_box.add(action_label)

        actions = ["Normal Key", "Shortcut", "Media Control", "App Shortcut", "Macro", "Disable"]
        action_select = toga.Select(
            items=actions,
            on_change=self._on_action_select,
            style=Pack(flex=1, padding=3)
        )
        remappings_box.add(action_select)

        # Key code selector
        key_label = toga.Label(
            "Key:",
            style=Pack(padding=(5, 0), color="white")
        )
        remappings_box.add(key_label)

        # Simple key code input
        key_input = toga.InputBox(
            prompt="Enter key code (e.g., 28 for Enter)",
            on_success=self._on_key_code_entered,
        )
        remappings_box.add(key_input)

        # Apply button
        apply_btn = toga.Button(
            "Apply",
            on_press=lambda w: self._apply_remapping(key_input.value),
            style=Pack(padding=5, margin=5)
        )
        remappings_box.add(apply_btn)

        scroll.content = remappings_box
        self.content_stack.add(scroll)

    def _on_action_select(self, widget):
        """Handle action selection change."""
        pass

    def _on_key_code_entered(self, result):
        """Handle key code entry."""
        pass

    def _apply_remapping(self, key_code_str: str):
        """Apply a key remapping."""
        try:
            key_code = int(key_code_str)
        except (ValueError, TypeError):
            return

        if not self.current_device:
            return

        # Show action selection dialog
        from toga.dialogs import Confirmation
        # For now, just apply normal key remapping
        success = self.detector.connected_device.remappings.get(key_code, {}).get("applied", False)
        
        # Actually use the key_customization module
        from .key_customization import KeyRemapEntry, RemapAction
        entry = KeyRemapEntry(key_code=key_code, action=RemapAction.NORMAL_KEY)
        self.detector.connected_device.remappings[key_code] = entry
        
        # Save to profile
        self.profiles_manager.save_remappings_to_profile("Default", self.detector.connected_device.remappings)
        
        # Refresh the view
        self._show_dashboard()

    def _show_key_tester(self):
        """Show the keyboard tester view."""
        self._clear_content_stack()

        back_btn = toga.Button(
            "Back",
            on_press=self._show_dashboard,
            style=Pack(padding=5, margin=5)
        )
        self.content_stack.add(back_btn)

        title = toga.Label(
            "Keyboard Tester",
            style=Pack(padding=10, font_size=16, font_weight="bold")
        )
        self.content_stack.add(title)

        # Status info
        status_label = toga.Label(
            "Press any physical key on your Portonics keyboard",
            style=Pack(padding=5, color="white")
        )
        self.content_stack.add(status_label)

        # Key visualization area
        # Create a simple grid of keys
        keys_box = toga.Box(style=Pack(direction="column", flex=1, padding=10))

        # Load keyboard layout
        self.keyboard_tester.load_layout()

        # Add key buttons
        key_codes = self.keyboard_tester.key_map.keys()
        key_rows = [list(key_codes)[i:i+15] for i in range(0, len(key_codes), 15)]

        for row_keys in key_rows:
            row_box = toga.Box(style=Pack(direction="row", padding=2, flex=1))
            for key_code in row_keys:
                key_info = self.keyboard_tester.key_map[key_code]
                status = self.keyboard_tester.get_key_status(key_code)
                
                # Determine button color based on status
                if status == keyboard_tester.KeyStatus.PRESSED:
                    bg = "#00e676"  # Green when pressed
                elif status == keyboard_tester.KeyStatus.UNTESTED:
                    bg = "#666666"  # Gray when untested
                else:
                    bg = "#555555"

                key_btn = toga.Button(
                    key_info.name[:3],  # Shortened name
                    on_press=lambda w, kc=key_code: self._on_key_press(w, kc),
                    style=Pack(
                        flex=1,
                        padding=3,
                        background_color=bg,
                        color="white",
                        border_radius=3
                    )
                )
                row_box.add(key_btn)
            keys_box.add(row_box)

        self.content_stack.add(keys_box)

        # Test history
        history_label = toga.Label(
            "Test History:",
            style=Pack(padding=(10, 0), color="white")
        )
        self.content_stack.add(history_label)

        # Reset button
        reset_btn = toga.Button(
            "Reset Test",
            on_press=self._on_reset_test,
            style=Pack(padding=5, margin=5)
        )
        self.content_stack.add(reset_btn)

    def _on_key_press(self, widget, key_code: int):
        """Handle physical key press."""
        # Record the key test
        key_info = self.keyboard_tester.key_map.get(key_code)
        if key_info:
            self.keyboard_tester.record_key_test(
                key_code=key_code,
                key_name=key_info.name,
                pressed=True
            )
            
            # Update button appearance
            for child in self.content_stack.children:
                if hasattr(child, 'children'):
                    for grandchild in child.children:
                        if hasattr(grandchild, 'children'):
                            for ggc in grandchild.children:
                                if hasattr(ggc, 'on_press'):
                                    pass  # Would need to update specific button

        # Update status
        status_label = self.content_stack.children[1] if len(self.content_stack.children) > 1 else None
        if status_label:
            # Update to show recently tested keys
            tested = self.keyboard_tester.get_tested_keys()
            status_label.text = f"Tested keys: {len(tested)}"

    def _on_reset_test(self, widget):
        """Reset the keyboard test."""
        self.keyboard_tester.reset_test()
        self._show_key_tester()  # Refresh the view

    def _show_device_info_view(self):
        """Show the device information view."""
        self._clear_content_stack()

        back_btn = toga.Button(
            "Back",
            on_press=self._show_dashboard,
            style=Pack(padding=5, margin=5)
        )
        self.content_stack.add(back_btn)

        title = toga.Label(
            "Device Information",
            style=Pack(padding=10, font_size=16, font_weight="bold")
        )
        self.content_stack.add(title)

        if not self.current_device:
            msg = toga.Label(
                "No device connected",
                style=Pack(padding=10, color="white")
            )
            self.content_stack.add(msg)
            return

        # Build detailed info
        info_lines = [
            f"Device: {self.current_device.model}",
            f"",
            f"Connection: {self.current_device.connection_type.value}",
            f"Vendor: {self.current_device.vendor}",
            f"",
            f"Firmware: {self.current_device.firmware_version or 'Not available'}",
            f"",
            f"Capabilities:",
        ]

        caps_str = self.current_device.get_capability_string()
        info_lines.append(f"  {caps_str}")

        info_lines.extend([
            f"",
            f"Connection State: {self.current_device.connection_state.value}",
            f"",
            f"Last Connected: {self.current_device.last_connected or 'Never'}",
        ])

        info_text = "\n".join(info_lines)
        info_label = toga.Label(
            info_text,
            style=Pack(padding=10, color="white", font_size=12)
        )
        self.content_stack.add(info_label)

    def _on_theme_toggle(self, widget):
        """Handle theme toggle."""
        self.theme = "light" if widget.value else "dark"
        bg = self._get_bg_color()
        # Refresh the main content
        if self.main_window and self.main_window.content:
            # Reset background
            pass

    def connect_device(self, device: PortonicsDevice):
        """Connect a detected device."""
        self.current_device = device
        self.detector.connected_device = device

        # Initialize lighting studio if device supports it
        if device.has_capability(Capability.RGB) or device.has_capability(Capability.LIGHTING_EFFECTS):
            self.lighting_studio = LightingStudio(device)

        # Update the UI
        self._update_device_card()
        self._show_dashboard()

    def disconnect_device(self):
        """Disconnect the current device."""
        self.current_device = None
        self.detector.disconnect()
        self.lighting_studio = None
        self._update_device_card()
        self._show_dashboard()


def main():
    """Return the main Toga app instance."""
    return PortonicsStudioApp()