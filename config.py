# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERSsa BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click, Match, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from myUtils import *
from screen_layouts import one_screen_layout, two_screen_layout, keyboard_layout_widget

terminal = 'urxvt'
win = "mod4"
alt = "mod1"
screens = []

home_path = '/home/simon/'
paths = {
    'config': '{}.config/'.format(home_path),
    'jetbrains': '{}.local/opt/jetbrains/'.format(home_path),
    'wallpapers': '{}/Pictures/wallpapers/'.format(home_path)
}

worksapces = {
    'Chromium': 'a',
    'Programming': 's',
    'Dosbox': 'd'
}


def toggle_keyboard_layout():
    global keyboard_layout_widget

    def callback(qtile):
        keyboard_layout_widget.next_keyboard()

    return callback


def move_window(direction):

    def callback(qtile):
        window = qtile.currentWindow
        info = window.cmd_info()
        is_floating = info['floating']
        if is_floating:
            if direction == 'Left':
                window.cmd_move_floating(-10, 0, 0, 0)
            elif direction == 'Right':
                window.cmd_move_floating(10, 0, 0, 0)
            elif direction == 'Up':
                window.cmd_move_floating(0, -10, 0, 0)
            elif direction == 'Down':
                window.cmd_move_floating(0, 10, 0, 0)
        else:
            if direction == 'Left':
                window.group.layout.cmd_swap_left()
            elif direction == 'Right':
                window.group.layout.cmd_swap_right()
            elif direction == 'Up':
                window.group.layout.cmd_shuffle_up()
            elif direction == 'Down':
                window.group.layout.cmd_shuffle_down()

        pass
    return callback


# HOOKS

@hook.subscribe.startup
def starting_programs():
    run("feh --bg-scale {}beauty/1.jpg".format(paths['wallpapers']))
    run("synclient VertEdgeScroll=1 TapButton1=1 TapButton2=3 TapButton3=2")
    runone("compton --config {}compton.conf".format(paths['config']))
    runone("dropbox")
    runone("redshift-gtk")


def set_screen_layout():
    global screens
    screens = get_screen_layout(len(query_screens()))
    if len(query_screens()) == 1:
        run(home_path+'.screenlayout/l1.sh')
    if len(query_screens()) == 2:
        run(home_path+'.screenlayout/l2.sh')


def get_screen_layout(screen_count):
    if screen_count == 2:
         return two_screen_layout
    elif screen_count == 1:
        return one_screen_layout
    return []


set_screen_layout()


@hook.subscribe.screen_change
def screen_change(qtile, ev):
    set_screen_layout()
    run("killall dropobx")
    runone("dropbox")
    qtile.cmd_restart()


# @hook.subscribe.client_new
# def java_dialog(window):
#    if ((window.window.get_wm_class() == 'sun-awt-X11-XwindowPeer' and
#                 window.window.get_wm_hints()['window_group'] != 0) or
#                 (window.window.get_wm_class() == 'sun-awt-X11-XDialogPeer')):
#        window.floating = True


# KEYS


keys = [
    # Switch between windows in current MonadTall

    # window moving shortcuts
    Key([win], "Left", lazy.layout.left()),
    Key([win], "Right", lazy.layout.right()),
    Key([win], "Down", lazy.layout.down()),
    Key([win], "Up", lazy.layout.up()),
    Key([win, 'shift'], "Left", lazy.function(move_window("Left"))),
    Key([win, 'shift'], "Right", lazy.function(move_window("Right"))),
    Key([win, 'shift'], "Down", lazy.function(move_window("Down"))),
    Key([win, 'shift'], "Up", lazy.function(move_window("Up"))),
    Key([win], 'l', lazy.layout.grow()),
    Key([win], 'j', lazy.layout.shrink()),
    Key([win], 'k', lazy.layout.flip()),

    # Switch window focus to other pane(s) of stack
    Key(
        [win], "space",
        lazy.function(toggle_keyboard_layout())
    ),

    # Swap panes of split stack
    Key(
        [win, 'shift'], "space",
        [win, 'shift'], "space",
        lazy.window.toggle_floating()
    ),

    Key(
        [win], 'c',
        lazy.spawn('chromium')
    ),

    Key(
        [win, alt], 'p',
        lazy.spawn('{}pycharm-2017.2.3/bin/pycharm.sh'.format(paths['jetbrains']))
    ),

    Key(
        [win, alt], 'i',
        lazy.spawn('{}idea-IC-172.3317.53/bin/idea.sh'.format(paths['jetbrains']))
    ),

    Key(
        [win, alt], 'w',
        lazy.spawn('{}WebStorm-172.3757.55/bin/webstorm.sh'.format(paths['jetbrains']))
    ),

    Key(
        [win, alt], 'f',
        lazy.spawn('firefox')
    ),


    #XF86 buttons

    Key(
        [], 'XF86AudioRaiseVolume',
        lazy.spawn('amixer -q -D pulse sset Master 5%+')
    ),

    Key(
        [], 'XF86AudioLowerVolume',
        lazy.spawn('amixer -q -D pulse sset Master 5%-')
    ),

    Key(
        [], 'XF86AudioMute',
        lazy.spawn('amixer -q -D pulse sset Master toggle')
    ),

    Key(
        [], 'XF86MonBrightnessUp',
        lazy.spawn('light -A 5')
    ),

    Key(
        [], 'XF86MonBrightnessDown',
        lazy.spawn('light -U 5')
    ),

    Key(
        [win, 'shift'], 'm',
        lazy.window.toggle_fullscreen()
    ),


    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [win, "shift"], "Return",
        lazy.function(toggle_keyboard_layout())
    ),
    Key([win], "Return", lazy.spawn(terminal)),

    # Toggle between different layouts as defined below
    Key([win], "Tab", lazy.next_layout()),
    Key([win], "w", lazy.window.kill()),

    Key([win, "control"], "r", lazy.restart()),
    Key([win, "control"], "q", lazy.shutdown()),
    Key([win], "r", lazy.spawn('rofi -show run')),
]


groups = [
    Group('a',
          matches=[
            Match(wm_class=["Chromium"]),
            Match(wm_class=["Firefox"]),
          ]),
    Group('s', matches=[
        Match(wm_class=["jetbrains-pycharm"]),
        Match(wm_class=["jetbrains-idea-ce"]),
        Match(wm_class=["jetbrains-webstorm"]),
        Match(wm_class=["jetbrains-gogland"]),
        Match(wm_class=["jetbrains-clion"]),
    ]),
    Group('d', matches=[
        Match(wm_class=["dosbox"])
    ]),
    Group('f', matches=[
        Match(wm_class=['VirtualBox'])
    ]),
    Group('u'),
    Group('i'),
    Group('o'),
    Group('p'),
]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([win], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([win, "shift"], i.name, lazy.window.togroup(i.name))
    )

layouts = [
    layout.MonadTall(),
    layout.Max(),
]

widget_defaults = dict(
    font='Hack, Awesome',
    fontsize=14,
    background='1d1f21',
    padding=3,
)

# Drag floating layouts.
mouse = [
    Drag([win], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([win], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([win], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = [
    Rule(Match(title=["Welcome to PyCharm"]), float=True, break_on_match=False),
    Rule(Match(title=["Welcome to IntelliJ IDEA"]), float=True, break_on_match=False),
    Rule(Match(title=["Welcome to WebStorm"]), float=True, break_on_match=False),
    Rule(Match(title=["  "]), float=True, break_on_match=False),
]

main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"
extentions = []

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
