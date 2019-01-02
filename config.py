from libqtile.config import Key, Screen, Group, Drag, Click, Match, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from myUtils import *
from screen_layouts import one_screen_layout,get_two_screen_layout , two_screen_layout, keyboard_layout_widget

terminal = "gnome-terminal"
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


def close_all_window_in_group(name):

    def callback(qtile):
        windows = qtile.cmd_items(name)
        for window in windows:
            window.cmd_kill()
    return callback

@hook.subscribe.client_new
def screenshot(window):
    if "gnome-screenshot" in window.window.get_wm_class():
        window.floating = True

@hook.subscribe.startup
def starting_programs():
    #run("xfce4-terminal")
    run("feh --bg-scale '/home/simon/wallpapers/Landscapes/1490049666110.png'")
    run("synclient VertEdgeScroll=1 TapButton1=1 TapButton2=3 TapButton3=2")
    run("synclient PalmDetect=1")
    run("synclient PalmMinWidth=8")
    run("synclient PalmMinX=100")
    run("compton ")
    runone("tracker daemon --start")
    runone("nm-applet --no-agent")
    #runone("redshift-gtk")
    runone("xrdb ~/.Xresources")
    runone('steam')
    runone('blueman-applet')
    runone_flatpak('com.discordapp.Discord', pname='discord')
    runone_flatpak('com.spotify.Client', pname='spotify')

def set_screen_layout():
    global screens
    screens = get_screen_layout(len(query_screens()))
    if len(query_screens()) == 1:
        run(home_path+'.screenlayout/l1.sh')
    else:
        run(home_path+'.screenlayout/l2.sh')


def get_screen_layout(screen_count):
    if screen_count == 1:
        return one_screen_layout
    return get_two_screen_layout(get_number_of_screens())


set_screen_layout()


@hook.subscribe.screen_change
def screen_change(qtile, ev):
    set_screen_layout()
    #run("killall dropobx")
    #runone("dropbox")
    qtile.cmd_restart()


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
    Key([win, 'shift'], 'k', lazy.layout.flip()),

    # Switch window focus to other pane(s) of stack
    Key(
        [win], "space",
        lazy.function(toggle_keyboard_layout())
    ),

    # Swap panes of split stack
    Key(
        [win, 'shift'], "space",
        lazy.window.toggle_floating()
    ),

    Key(
        [win], 'c',
        lazy.spawn('google-chrome-stable')
    ),

    Key(
        [win, alt], 'p',
        lazy.spawn('{}pycharm-2017.2.3/bin/pycharm.sh'.format(paths['jetbrains']))
    ),

    Key(
        [win, alt], 'i',
        lazy.spawn('{}idea-IU-172.4343.14/bin/idea.sh'.format(paths['jetbrains']))
    ),

    Key(
        [win, alt], 'w',
        lazy.spawn('{}WebStorm-172.3757.55/bin/webstorm.sh'.format(paths['jetbrains']))
    ),

    Key(
        [win, alt], 'g',
        lazy.spawn("{}Gogland-172.2696.28/bin/gogland.sh".format(paths['jetbrains']))
    ),

    Key(
        [win, alt], 'f',
        lazy.spawn('firefox')
    ),
    Key(
      [win, "shift"], 'v', lazy.group['scratchpad'].dropdown_toggle('term')
    ),
    Key(
        [win, alt], 's', lazy.spawn('gnome-screenshot --interactive')
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
        [win], "Return",
        lazy.function(toggle_keyboard_layout())
    ),
    Key([win], "Return", lazy.spawn(terminal)),

    # Toggle between different layouts as defined below
    Key([win], "Tab", lazy.next_layout()),
    Key([win], "w", lazy.window.kill()),

    Key([win, "control"], "r", lazy.restart()),
    Key([win, "control"], "q", lazy.shutdown()),
    Key([win], "r", lazy.spawn('rofi -show run -theme Pop-Dark')),
]


groups = [
    Group('a',
          matches=[
            Match(wm_class=["Chromium", "chromium"]),
            Match(wm_class=["google-chrome", "Google-chrome"]),
            Match(wm_class=["Firefox"]),
          ],
          layouts=[
            layout.MonadTall(border_width=1, margin=3, ratio=0.65),
          ]),
    Group('s', matches=[
        Match(wm_class=["jetbrains-pycharm"]),
        Match(wm_class=["jetbrains-idea-ce"]),
        Match(wm_class=["jetbrains-idea"]),
        Match(wm_class=["jetbrains-webstorm"]),
        Match(wm_class=["jetbrains-gogland"]),
        Match(wm_class=["jetbrains-clion"]),
    ]),
    Group('d', matches=[
        Match(wm_class=["dosbox"]), Match(wm_class=["code - oss"])
    ]),
    Group('f', matches=[
        Match(wm_class=['VirtualBox'])
    ]),
    Group('u', matches=[
        Match(wm_class=['Steam'])
    ]),
    Group('i', matches=[
        Match(wm_class=['discord'])
    ]),
    Group('o', matches=[
	Match(wm_class=['spotify', 'Spotify'])
    ]),
    Group('p'),
]

for i in groups:
    # mod1 + letter of group = switch to group
    if i.name is not 'scratchpad':
        keys.append(
            Key([win], i.name, lazy.group[i.name].toscreen())
        )

        # mod1 + shift + letter of group = switch to & move focused window to group
        keys.append(
            Key([win, "shift"], i.name, lazy.window.togroup(i.name))
        )

layouts = [
    layout.MonadTall(border_width=1, margin=7),
    layout.Max(),
]

widget_defaults = dict(
    font='Hack',
    fontsize=13,
    padding=2,
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
#dgroups_app_rules = [
#    Rule(Match(title=["Welcome to PyCharm"]), float=True, break_on_match=False),
#    Rule(Match(wm_class=["jetbrains-idea"]), group="s", float=False, break_on_match=False),
#    Rule(Match(title=["Welcome to IntelliJ IDEA"]), group="s", float=True, break_on_match=False),
#    Rule(Match(title=["Welcome to WebStorm"]), float=True, break_on_match=False),
#    Rule(Match(title=["Welcome to CLion"]), float=True, break_on_match=False),
#]
dgroups_app_rules = [
    Rule(Match(wm_class=["sun-awt-X11-XWindowPeer"]), float=True)
]

main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(auto_float_types=[
    'notification',
    'toolbar',
    'splash',
    'dialog',
    'utility'
])
auto_fullscreen = True
focus_on_window_activation = "smart"
wmname = "LG3D"
