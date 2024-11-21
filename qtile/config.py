# Copyright (c) 2009 Aldo Cortesi
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
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger
from datetime import datetime
import os
import subprocess

# ENVIRONMENT VARIABLES AND PREFERENCES 
os.environ['QT_QPA_PLATFORMTHEME'] = 'qt5ct' 
os.environ['XCURSOR_THEME'] = 'Breeze_Light'
preferred_terminal = "qterminal"
screen_locker = ["betterlockscreen", "--lock"]
suspend_program = ["systemctl", "suspend"]
monospace = "Cascadia Code"

# MACHINE SPECIFIC VARS:
userhome = os.path.expanduser("~/")
config_dir = f"{userhome}/.config/qtile/"
# BOOLEANS:
cursor_warp=True

# HOOKS:
@hook.subscribe.startup_once
def autostart_once():
    if qtile.core.name == "wayland":
        script= userhome + ".config/qtile/autostart-wayland.sh" 
        subprocess.run([script])
        logger.warning("Autostarted Wayland script")
    else:
        logger.warning("Started the autostart once script")
        script= userhome + ".config/qtile/autostart-once.sh"
        subprocess.run([script])
@hook.subscribe.startup
def autostart():
    if qtile.core.name != "wayland":
        logger.warning("Autostart hook has fired off.")
        script= userhome + ".config/qtile/autostart.sh"
        subprocess.run([script])
        logger.warning("Autostarted X11 script")
@hook.subscribe.client_name_updated
def window_rules(client):
    if "UMass Amherst Mail" in client.name:
        client.togroup("3")
    if "Google Keep" in client.name:
        client.togroup("1")
    if "ksnip" in client.name:
        client.enable_floating()
        client.center()
@hook.subscribe.screens_reconfigured
def screen_reconf():
    logger.warning("Screens have been reconfigured")
    qtile.reload_config()
@lazy.group.function
def unminimize_all(group):
    for win in group.windows:
        if win.minimized:
            win.toggle_minimize()
mod = "mod4"
alt = "mod1"
terminal = preferred_terminal if not None else guess_terminal()
menu = "rofi -show drun"
# make it simple to see if config gets updated
date = datetime.now()
logger.warning(date)
date = f'{date.hour}:{date.minute:02d}'
# Switch screen window functionality
def window_cycle_screen(qtile, move_window=True, change_screen=True):
    i = qtile.screens.index(qtile.current_screen)
    # move to screen i + 1 and wrap back around to the first screen
    if move_window: 
        group = qtile.screens[(i+1) % len(qtile.screens)].group.name
        qtile.current_window.togroup(group)
    if change_screen:
        qtile.to_screen((i+1) % len(qtile.screens))
# Screen locker 
def lock_screen(qtile, screen_locker_x: list[str] | None = None, screen_locker_wayland: list[str] | None = None, suspend: bool=False):
    if qtile.core.name != "wayland":
        if screen_locker_x != None: 
            subprocess.Popen(screen_locker_x)
        else: return
    else:
        if screen_locker_wayland != None:
            subprocess.Popen(screen_locker_wayland)
        else: return
    if suspend:
        subprocess.run(suspend_program)
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return", lazy.layout.toggle_split(), 
        desc="Toggle between split and unsplit sides of stack"), 
    Key([mod], "Return", lazy.spawn(terminal),
        desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"), 
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "e", lazy.spawn("pcmanfm-qt"), desc="Launch file [e]xplorer"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "r", lazy.spawn(os.path.expanduser("~/.config/qtile/autostart.sh")), desc="Resize the virtual display to match the window"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "space", lazy.spawn(menu), desc="Spawn a command using a prompt widget"),
    # custom keys
    Key([mod], "i", lazy.spawn("firefox"), desc="Quick shortcut to [i]nternet browser"),
    Key([mod], "comma", lazy.function(window_cycle_screen)),
    Key([mod], "period", lazy.function(window_cycle_screen, move_window=False)),
    Key([alt], "Tab", lazy.group.next_window()),
    Key([alt], "l", lazy.function(lock_screen, screen_locker_x=screen_locker)),
    Key([alt, "shift"], "l", lazy.function(lock_screen, screen_locker_x=screen_locker, suspend=True)),
    Key([mod, "shift"], "m", unminimize_all, desc="Unminimize all windows in current group")
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = [Group(i) for i in "123456789"]
# The second part is specific to Alacritty
groups.append(ScratchPad("dropdown terminal", [DropDown("terminal", terminal, opacity=0.8), DropDown("config", terminal + " -e vim " + userhome + ".config/qtile/config.py")]
    ))
keys.append(Key([], "F10", lazy.group["dropdown terminal"].dropdown_toggle("terminal")))
keys.append(Key([mod], "c", lazy.group["dropdown terminal"].dropdown_toggle("config")))
for i in groups[:9]:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4, margin=2, margin_on_single=0),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font=monospace,
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# LaunchBar progs
progs = [(config_dir + "firefox.png", "firefox", "open the web browser firefox"),
         (config_dir + "terminal.png", terminal, "open the terminal emulator alacritty"),
         (config_dir + "folder.png", "pcmanfm-qt", "open the file explorer pcmanfm")]
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CPUGraph(),
                widget.GroupBox(),
                widget.LaunchBar(progs=progs, padding=5),
                widget.Prompt(),
                widget.Spacer(length=10),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox(f"configuration at {str(date)}", name="default"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Bluetooth(background = "#445e93", fmt="<b>{}</b>", padding=10), 
                widget.Systray(),
                # widget.BatteryIcon(theme_path="/usr/share/icons/Papirus-Dark"),
                widget.Clock(format="%Y-%m-%d %H:%M"),
                widget.Image(filename=config_dir + "shutdown.png", mouse_callbacks={"Button1": lazy.spawn(config_dir + "PowerOptions/dialog.py")}),
            ],
            32,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
        wallpaper=userhome + "Pictures/wallpapers/budapest.jpg",
        wallpaper_mode="fill"
    ),
    Screen(
        # for the second screen, if connected
        top=bar.Bar(
            [widget.GroupBox(),
             widget.Spacer(length=10),
             widget.WindowName(),
             ],
             32
        ),
        wallpaper=userhome + "Pictures/wallpapers/budapest.jpg",
        wallpaper_mode="fill"
    ),
]
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()), 
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
#wl_xcursor_theme = Breeze_Light 
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
