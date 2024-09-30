import board # type: ignore
import busio

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.scanners import DiodeOrientation
from kmk.modules.macros import Delay, Macros, Tap, Press, Release

keyboard = KMKKeyboard()

keyboard.col_pins = (
    board.GP3,
    board.GP4,
    board.GP5
)
keyboard.row_pins = (
    board.GP0,
    board.GP1,
    board.GP2
)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

media_keys = MediaKeys()
macros = Macros()
keyboard.extensions.append(media_keys)
keyboard.extensions.append(macros)

back_nav = KC.MACRO(
    Press(KC.LGUI),
    Delay(25),
    Press(KC.LALT),
    Delay(25),
    Tap(KC.LEFT),
    Delay(25),
    Release(KC.LGUI),
    Delay(25),
    Release(KC.LALT),
    )

forward_nav = KC.MACRO(
    Press(KC.LGUI),
    Delay(25),
    Press(KC.LALT),
    Delay(25),
    Tap(KC.RIGHT),
    Delay(25),
    Release(KC.LGUI),
    Delay(25),
    Release(KC.LALT),
    )

find_all_intellij = KC.MACRO(
    Tap(KC.LSHIFT),
    Delay(25),
    Tap(KC.LSHIFT),
)

# Matrix 3x3 keymap, 9 keys in total
keyboard.keymap = [
    [
        KC.NUMPAD_7, KC.NUMPAD_8, KC.NUMPAD_9,
        KC.NUMPAD_4, KC.NUMPAD_5, KC.NUMPAD_6,
        KC.NUMPAD_1, KC.NUMPAD_2, KC.NUMPAD_3,
    ],
    [
        KC.F22, KC.F23, KC.F24,
        KC.F19, KC.F20, KC.F21,
        KC.F16, KC.F17, KC.F18,
    ],
    [
        KC.F19, KC.NO, KC.NO,
        KC.F16, KC.F17, KC.F18,
        KC.F13, KC.F14, KC.F15,
    ],
    [
        back_nav, forward_nav, KC.LCTRL(KC.LGUI(KC.Q)),
        KC.LGUI(KC.L), KC.LGUI(KC.F7), find_all_intellij,
        KC.LGUI(KC.O), KC.LALT(KC.F7), KC.LGUI(KC.F12),
    ]
]

keymap_legend = [
    [
        [
            "7, 8, 9"
        ],
        [
            "4, 5, 6"
        ],
        [
            "1, 2, 3"
        ]
    ],
    [
        [
            "F22, F23, F24"
        ],
        [
            "F19, F20, F21"
        ],
        [
            "F16, F17, F18"
        ]
    ],
    [
        [
            "F19, N/A, N/A"
        ],
        [
            "F16, F17, F18"
        ],
        [
            "F13, F14, F15"
        ]
    ],
    [
        [
            "BCK, FWD, LCK"
        ],
        [
            "LIN, FUS, FND"
        ],
        [
            "CLS, USG, MTD"
        ]
    ]
]

i2c_bus = busio.I2C(board.GP17, board.GP16)

driver = SSD1306(
    # Mandatory:
    i2c=i2c_bus,
    # Optional:
    #device_address=0x3C,
)

display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=64, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    brightness=0.8, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=20, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=60, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
)

display.entries = [
    TextEntry(text="Layer: ", x=0, y=0),
    TextEntry(text="NUMPAD_MODE", x=64, y=12, layer=0, x_anchor="M"),
    TextEntry(text="0", x=38, y=0, layer=0),
    TextEntry(text=str(keymap_legend[0][0]), x=64, y=24, layer=0, x_anchor="M"),
    TextEntry(text=str(keymap_legend[0][1]), x=64, y=36, layer=0, x_anchor="M"),
    TextEntry(text=str(keymap_legend[0][2]), x=64, y=48, layer=0, x_anchor="M"),
    TextEntry(text="F_MODE_WIN", x=64, y=12, layer=1, x_anchor="M"),
    TextEntry(text="1", x=38, y=0, layer=1),
    TextEntry(text=str(keymap_legend[1][0]), x=64, y=24, layer=1, x_anchor="M"),
    TextEntry(text=str(keymap_legend[1][1]), x=64, y=36, layer=1, x_anchor="M"),
    TextEntry(text=str(keymap_legend[1][2]), x=64, y=48, layer=1, x_anchor="M"),
    TextEntry(text="F_MODE_MAC", x=64, y=12, layer=2, x_anchor="M"),
    TextEntry(text="2", x=38, y=0, layer=2),
    TextEntry(text=str(keymap_legend[2][0]), x=64, y=24, layer=2, x_anchor="M"),
    TextEntry(text=str(keymap_legend[2][1]), x=64, y=36, layer=2, x_anchor="M"),
    TextEntry(text=str(keymap_legend[2][2]), x=64, y=48, layer=2, x_anchor="M"),
    TextEntry(text="INTELLI_MAC", x=64, y=12, layer=3, x_anchor="M"),
    TextEntry(text="3", x=38, y=0, layer=3),
    TextEntry(text=str(keymap_legend[3][0]), x=64, y=24, layer=3, x_anchor="M"),
    TextEntry(text=str(keymap_legend[3][1]), x=64, y=36, layer=3, x_anchor="M"),
    TextEntry(text=str(keymap_legend[3][2]), x=64, y=48, layer=3, x_anchor="M"),
]

keyboard.extensions.append(display)

def on_move_do(state):
    if state is not None and state['direction'] == -1:
       display.reset_wake_timer()
       if keyboard.active_layers[0] > 0:
           keyboard.active_layers[0] -= 1
       else:
           keyboard.active_layers[0] = len(keyboard.keymap) - 1
    elif state is not None and state['direction'] != -1:
        display.reset_wake_timer()
        if keyboard.active_layers[0] < len(keyboard.keymap) - 1:
            keyboard.active_layers[0] += 1
        else:
            keyboard.active_layers[0] = 0

# Rotary encoder that also acts as a key
encoder_handler = EncoderHandler()
encoder_handler.divisor = 2
encoder_handler.pins = [(board.GP18, board.GP19, board.GP20)]
encoder_handler.map = [
        (
        (KC.TRNS, KC.TRNS, KC.NLCK),
        ),
        (
        (KC.TRNS, KC.TRNS, KC.a),
        ),
        (
        (KC.TRNS, KC.TRNS, KC.b),
        ),
        (
        (KC.LCTRL, KC.LCTRL, KC.c),
        ),
]
encoder_handler.on_move_do = lambda x, y, state: on_move_do(state)
keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()
