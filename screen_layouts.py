from libqtile.config import Screen
from libqtile import widget, bar
from myUtils import run
import re

keyboard_layout_widget = widget.KeyboardLayout(
    configured_keyboards=['us', 'il'],
    foreground='f44165',
)

primary_screen = Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    disable_drag=True,
                ),
                widget.Prompt(),
                widget.WindowName(fontsize=12),
                widget.Sep(),
                widget.Backlight(
                    foreground='1d1f21',
                    initial_background='f1ce4f',
                    background='f1ce4f',
                    backlight_name="intel_backlight",
                    brightness_file='brightness',
                    update_interval=0.1,
                    format='{percent: 2.0%} '
                ),
                widget.Sep(),
                widget.Volume(emoji=False),
                widget.Volume(emoji=True),
                widget.Sep(),
                widget.TextBox(text=""),
                widget.Pacman(),
                widget.TextBox(text="Updates Available"),
                widget.Sep(),
                widget.Wlan(
                    foreground='42bcf4',
                    interface='wlp3s0',
                    format=' {essid} {quality}/70'
                ),
                widget.Sep(),
                widget.TextBox(
                    text='',
                    foreground='f44165'
                ),
                keyboard_layout_widget,
                widget.Sep(),
                widget.Clock(
                    format=' %H:%M:%S',
                    timezone="Asia/Jerusalem",
                    foreground='#50e6a4'
                ),
                widget.Sep(),
                widget.Clock(
                    format=' %d/%m/%Y',
                    foreground='f4a142'
                ),
                widget.Sep(),
                widget.Systray(),
                widget.Sep(),
                widget.BatteryIcon(
                    battery_name='BAT1',
                    
                   
                ),

                widget.Sep(text="|"),
                widget.BatteryIcon(
                    battery_name="BAT0",
                    
                ),
            ],
            28,
            background='0F1213'
        ),
)

secondary_screen = Screen(
    bottom=bar.Bar(
        [
            widget.GroupBox(disable_drag=True),
            widget.WindowName(),
            widget.TextBox(text='', foreground='18BAEB'),
            widget.CPUGraph(),
            widget.Sep(),
            widget.DF(visible_on_warn=False, partition='/home/simon'),
            widget.Sep(),
            widget.DF(visible_on_warn=False, partition='/'),
            widget.Sep(),
            widget.MemoryGraph(frequency=0.5),
        ],
        28,
        background='0F1213'
    ),
)

one_screen_layout = [
    primary_screen
]

two_screen_layout = [
    primary_screen,
    secondary_screen
]
