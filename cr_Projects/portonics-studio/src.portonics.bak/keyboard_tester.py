# Keyboard Tester Component
# Interactive keyboard visualization with key event detection

import logging
from typing import Dict, List, Optional, Set
from enum import Enum

logger = logging.getLogger(__name__)


class KeyStatus(Enum):
    UNTESTED = "untested"
    PRESSED = "pressed"
    RELEASED = "released"
    FAILED = "failed"


class KeyInfo:
    """Information about a keyboard key."""

    def __init__(self, key_code: int, name: str, position: tuple[int, int]):
        self.key_code = key_code
        self.name = name
        self.position = position  # (x, y) position on virtual keyboard
        self.status = KeyStatus.UNTESTED
        self.test_count = 0


class KeyboardTester:
    """Full interactive keyboard visualization and testing."""

    def __init__(self):
        self.key_map: Dict[int, KeyInfo] = {}
        self.test_history: List[Dict] = []
        self.tested_keys: Set[int] = set()
        self._layout_loaded = False

    def load_layout(self, layout_name: str = "default") -> None:
        """Load a keyboard layout.

        Args:
            layout_name: Name of the layout to load.
        """
        # Define common keyboard layouts with key positions
        # This is a simplified layout - real implementation would
        # have proper key mapping for each supported model
        self.key_map = self._default_layout()
        self._layout_loaded = True
        logger.info(f"Loaded keyboard layout: {layout_name}")

    def _default_layout(self) -> Dict[int, KeyInfo]:
        """Create a default QWERTY keyboard layout.

        Returns:
            Dictionary mapping key codes to KeyInfo.
        """
        keys = {}
        # Row 1: Esc, F1-F12, ~, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, -, =, Backspace
        key_positions = [
            (106, "Esc"), (107, "F1"), (108, "F2"), (109, "F3"),
            (110, "F4"), (111, "F5"), (113, "F6"), (114, "F7"),
            (115, "F8"), (116, "F9"), (117, "F10"), (118, "F11"),
            (119, "F12"), (0, "~"), (4, "1"), (5, "2"), (6, "3"),
            (7, "4"), (8, "5"), (9, "6"), (10, "7"), (11, "8"),
            (12, "9"), (13, "0"), (14, "-"), (15, "="), (198, "Backspace")
        ]
        for key_code, name in key_positions:
            keys[key_code] = KeyInfo(key_code=key_code, name=name, position=(0, 0))

        # Row 2: Tab, Q, W, E, R, T, Y, U, I, O, P, [, ], Backslash
        key_positions2 = [
            (15, "Tab"), (16, "Q"), (17, "W"), (18, "E"), (19, "R"),
            (20, "T"), (21, "Y"), (22, "U"), (23, "I"), (24, "O"),
            (25, "P"), (30, "["), (31, "]"), (49, "Backslash")
        ]
        for key_code, name in key_positions2:
            keys[key_code] = KeyInfo(key_code=key_code, name=name, position=(0, 0))

        # Row 3: Caps Lock, A, S, D, F, G, H, J, K, L, ;, '"', Enter
        key_positions3 = [
            (58, "Caps Lock"), (30, "A"), (31, "S"), (32, "D"), (33, "F"),
            (34, "G"), (35, "H"), (36, "J"), (37, "K"), (38, "L"),
            (40, ";"), (41, '"'), (51, "Enter")
        ]
        for key_code, name in key_positions3:
            keys[key_code] = KeyInfo(key_code=key_code, name=name, position=(0, 0))

        # Row 4: Shift, Z, X, C, V, B, N, M, ,, ., /, Shift
        key_positions4 = [
            (42, "Shift Left"), (44, "Z"), (45, "X"), (46, "C"), (47, "V"),
            (48, "B"), (49, "N"), (50, "M"), (51, ","), (52, "."),
            (53, "/"), (54, "Shift Right")
        ]
        for key_code, name in key_positions4:
            keys[key_code] = KeyInfo(key_code=key_code, name=name, position=(0, 0))

        # Additional keys
        keys[55] = KeyInfo(key_code=55, name="Ctrl Left", position=(0, 0))
        keys[56] = KeyInfo(key_code=56, name="Shift Left", position=(0, 0))  # Duplicate - remove
        keys[57] = KeyInfo(key_code=57, name="Alt Left", position=(0, 0))
        keys[100] = KeyInfo(key_code=100, name="Ctrl Right", position=(0, 0))
        keys[105] = KeyInfo(key_code=105, name="Alt Right", position=(0, 0))

        return keys

    def record_key_test(self, key_code: int, key_name: str, pressed: bool) -> None:
        """Record a key test event.

        Args:
            key_code: The key code that was pressed.
            key_name: The name of the key.
            pressed: Whether the key was pressed (True) or released (False).
        """
        info = self.key_map.get(key_code)
        if info:
            if pressed:
                info.status = KeyStatus.PRESSED
            else:
                info.status = KeyStatus.RELEASED
            info.test_count += 1
        else:
            # Add new key if not in map
            self.key_map[key_code] = KeyInfo(
                key_code=key_code, name=key_name, position=(0, 0)
            )

        self.tested_keys.add(key_code)
        self.test_history.append({
            "key_code": key_code,
            "key_name": key_name,
            "pressed": pressed,
            "timestamp": len(self.test_history),
        })

    def reset_test(self) -> None:
        """Reset all key test states."""
        for key_info in self.key_map.values():
            key_info.status = KeyStatus.UNTESTED
            key_info.test_count = 0
        self.test_history.clear()
        self.tested_keys.clear()

    def get_tested_keys(self) -> List[int]:
        """Return list of key codes that have been tested."""
        return list(self.tested_keys)

    def get_key_status(self, key_code: int) -> KeyStatus:
        """Get the test status of a specific key."""
        info = self.key_map.get(key_code)
        if info:
            return info.status
        return KeyStatus.UNTESTED

    def get_all_status(self) -> Dict[int, KeyStatus]:
        """Get the test status of all keys."""
        return {code: info.status for code, info in self.key_map.items()}