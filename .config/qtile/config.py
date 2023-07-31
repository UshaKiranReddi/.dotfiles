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
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule, ScratchPad, DropDown
from libqtile.command import lazy
from typing import List  # noqa: F401
from libqtile.widget import Spacer
from qtile_extras import widget
from libqtile import qtile
from libqtile.backend.x11 import window
from libqtile.confreader import ConfigError
from libqtile.widget import base
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import RectDecoration
from libqtile.config import Match
import arcobattery

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')

# _   __                 ______ _           _ _                 
#| | / /                 | ___ (_)         | (_)                
#| |/ /  ___ _   _ ______| |_/ /_ _ __   __| |_ _ __   __ _ ___ 
#|    \ / _ \ | | |______| ___ \ | '_ \ / _` | | '_ \ / _` / __|
#| |\  \  __/ |_| |      | |_/ / | | | | (_| | | | | | (_| \__ \
#\_| \_/\___|\__, |      \____/|_|_| |_|\__,_|_|_| |_|\__, |___/
#             __/ |                                    __/ |    
#            |___/                                    |___/  

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

keys = [
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen mode"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(["mod1"], "l", lazy.spawn("rofi -show drun"), desc="Launch an application."),
    Key(["mod1"], "z", lazy.spawn("rofi -show window"), desc="Switch between windows."),
  #  Key([mod, "control"], "l", lazy.spawn("betterlockscreen -l"), desc="locks screen"),
  #  Key([mod, "control"], "t", lazy.spawn("telegram-desktop"), desc="telegramDesktop"),
    Key([mod, "control"], "e", lazy.spawn("emacs"), desc="Launch emacs"),
  #  Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.restart(), desc="Reload the config"),

# QTILE LAYOUT KEYS
    Key([mod, "control"], "n", lazy.layout.normalize(), desc='normalize window size ratios'),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS / Switch between windows
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),

 # Keybindings for resizing windows in MonadTall layout
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
        
     # Maximize the focused window
    Key([mod], "m", lazy.window.toggle_maximize()),

    # Minimize the focused window
    Key([mod], "n", lazy.window.toggle_minimize()),

# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),
# FLIP LAYOUT FOR BSP
 #   Key([mod, "mod1"], "k", lazy.layout.flip_up()),
  #  Key([mod, "mod1"], "j", lazy.layout.flip_down()),
   # Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    #Key([mod, "mod1"], "h", lazy.layout.flip_left()),
# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
# SHUTDOWN QTILE
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    ]

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

#keys.extend([
 #   # MOVE WINDOW TO NEXT SCREEN
  #  Key([mod,"shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
   # Key([mod,"shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
#])

#   ____ ____   ___  _   _ ____  ____
#  / ___|  _ \ / _ \| | | |  _ \/ ___|
# | |  _| |_) | | | | | | | |_) \___ \
# | |_| |  _ <| |_| | |_| |  __/ ___) |
#  \____|_| \_\\___/ \___/|_|   |____/

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


groups = [
     Group('1', label="一", layout="monadtall"),
     Group('2', label="二", layout="monadtall"),
     Group('3', label="三", layout="monadtall"),
     Group('4', label="四", layout="monadtall"),
     Group('5', label="五", layout="monadtall"),
     Group('6', label="六", layout="monadtall"),
     Group('7', label="七", layout="monadtall"),
     Group('8', label="八", layout="monadtall"),
     Group('9', label="九", layout="monadtall"),
]
# FOR QWERTY KEYBOARDS
###group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]
# FOR AZERTY KEYBOARDS
#group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]
#group_labels = ["一", " 二", " ", " ", " ", " ", " ", " ", " ",]
###group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]
###group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

###for i in range(len(group_names)):
   ### groups.append(
      ###  Group(
         ###   name=group_names[i],
            ###layout=group_layouts[i].lower(),
           ### label=group_labels[i],
        ###))

for i in groups:
    keys.extend([
        Key([mod], "Right", lazy.screen.next_group(), desc="move to next workspace"),
        Key([mod], "Left", lazy.screen.prev_group(), desc="move to previous workspace"),

    Key([mod], "KP_End", lazy.screen.toggle_group('1'), desc="Switch to workspace 1"),
    Key([mod], "KP_Down", lazy.screen.toggle_group('2'), desc="Switch to workspace 2"),
    Key([mod], "KP_Next", lazy.screen.toggle_group('3'),  desc="Switch to workspace 3"),
    Key([mod], "KP_Left", lazy.screen.toggle_group('4'),  desc="Switch to workspace 4"),
    Key([mod], "KP_Begin", lazy.screen.toggle_group('5'), desc="Switch to workspace 5"),
    Key([mod], "KP_Right", lazy.screen.toggle_group('6'), desc="Switch to workspace 6"),
    Key([mod], "KP_Home", lazy.screen.toggle_group('7'), desc="Switch to workspace 7"),
    Key([mod], "KP_Up", lazy.screen.toggle_group('8'), desc="Switch to workspace 8"),
    Key([mod], "KP_Prior", lazy.screen.toggle_group('9'), desc="Switch to workspace 9"),

        Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            desc="MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE"),
        Key([mod], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen(),
            desc="MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE"),
    ])


#  ____   ____ ____      _  _____ ____ _   _ ____   _    ____  ____
# / ___| / ___|  _ \    / \|_   _/ ___| | | |  _ \ / \  |  _ \/ ___|
# \___ \| |   | |_) |  / _ \ | || |   | |_| | |_) / _ \ | | | \___ \
#  ___) | |___|  _ <  / ___ \| || |___|  _  |  __/ ___ \| |_| |___) |
# |____/ \____|_| \_\/_/   \_\_| \____|_| |_|_| /_/   \_\____/|____/
#
groups.append(ScratchPad('scratchpad', [
     DropDown('term', 'alacritty', width=0.4, height=0.5, x=0.3, y=0.1, opacity=1),
     DropDown('mixer', 'pavucontrol', width=0.4,
             height=0.6, x=0.3, y=0.1, opacity=1),           
]))

keys.extend([
     Key(["control"], "KP_End", lazy.group['scratchpad'].dropdown_toggle('term')),
     Key(["control"], "KP_Down", lazy.group['scratchpad'].dropdown_toggle('mixer')),])
   #  Key(["control"], "KP_Next", lazy.group['scratchpad'].dropdown_toggle('mixer')),])
    # Key(["control"], "KP_Left", lazy.group['scratchpad'].dropdown_toggle('mixer')),])
     #Key(["control"], "KP_Begin", lazy.group['scratchpad'].dropdown_toggle('mixer')),])   

#  _        _ __   _____  _   _ _____ ____
# | |      / \\ \ / / _ \| | | |_   _/ ___|
# | |     / _ \\ V / | | | | | | | | \___ \
# | |___ / ___ \| || |_| | |_| | | |  ___) |
# |_____/_/   \_\_| \___/ \___/  |_| |____/


def init_layout_theme():
    return {"margin":6,
            "border_width":2,
            "border_focus": "#81A1C1",
            "border_normal": "#2E3440"
            }

layout_theme = init_layout_theme()


layouts = [
     layout.MonadTall(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
  #  layout.MonadTall(**layout_theme, new_client_position='top'),
     layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    #layout.MonadWide(**layout_theme),
     layout.Matrix(**layout_theme),
     #layout.Bsp(**layout_theme),
    #layout.Floating(**layout_theme),
   # layout.RatioTile(**layout_theme),
    #layout.Max(**layout_theme)
]

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
   # Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
    Match(wm_class='xfce4-terminal'),
    Match(wm_class='mpv'),
   # Match(wm_class='nitrogen'),

],  fullscreen_border_width = 0, border_width = 0)

auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"   

floating_types = ["notification", "toolbar", "splash", "dialog"]

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

# COLORS FOR THE BAR
def init_colors():
    return [["#D8DEE9", "#D8DEE9"], # color 0
            ["#2E3440", "#2E3440"], # color 1
            ["#4C566A", "#4C566A"], # color 2
            ["#A3BE8C", "#A3BE8C"], # color 3
            ["#8FBCBB", "#8FBCBB"], # color 4
            ["#EBCB8B", "#EBCB8B"], # color 5
            ["#BF616A", "#BF616A"], # color 6
            ["#81A1C1", "#81A1C1"], # color 7
            ["#B48EAD", "#B48EAD"], # color 8
            ["#D08770", "#D08770"]] # color 9

colors = init_colors()

# __          ___     _            _       
# \ \        / (_)   | |          | |      
#  \ \  /\  / / _  __| | __ _  ___| |_ ___ 
#   \ \/  \/ / | |/ _` |/ _` |/ _ \ __/ __|
#    \  /\  /  | | (_| | (_| |  __/ |_\__ \
#     \/  \/   |_|\__,_|\__, |\___|\__|___/
#                        __/ |             
#                       |___/    


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Source Code Pro",
                fontsize = 12,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
              widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[1],
                        background = colors[1]
                        ),
               widget.Image(
                       filename = "~/.config/qtile/menu-pics/morning-glory.png", scale = "False",
                       background = colors[1],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("alacritty")}),
               widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[1],
                        background = colors[1]
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.CurrentLayoutIcon(
                        padding = 0,
                        scale = 0.6,
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.GroupBox(font="Source Code Pro",
                        fontsize = 16,
                        margin_y = 2,
                        margin_x = 3,
                        padding_y = 2,
                        padding_x = 3,
                        borderwidth = 0,
                        disable_drag = True,
                        active = colors[7],
                        inactive = colors[2],
                        rounded = False,
                        highlight_method = "text",       
                        this_current_screen_border = colors[3],
                        foreground = colors[2],
                        background = colors[1],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        background = colors[1],
                        foreground = colors[2],
                        ),
               widget.WindowName(font="Source Code Pro Bold",
                        fontsize = 14,
                        foreground = colors[0],
                        background = colors[1],
                        ),
      #         widget.Pomodoro(
       #                 background = colors[1],
        #                color_active = colors[1],
         ##               color_break = colors[1],
           #             color_inactive = colors[1],
            ##            font = 'Source Code Pro Bold',
              #          icon_size = 14,
               #         decorations = [
                #            RectDecoration (
                 #               colour = colors[5],
                  #              padding_y = 5,
                   #             radius = 2,
                    #            filled = True
                     #       ),
                      #  ], ),
                widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[1],
                        background = colors[1]
                        ),
                widget.Memory(
                        measure_mem = 'M',
                        format = '{MemUsed:.0f}{mm} | {MemTotal:.0f}{mm}',
                        foreground = colors[1],
                        background = colors[1],
                        font = "Source Code Pro Bold",
                        fontsize = 14,
                        decorations = [
                            RectDecoration (
                                colour = colors[6],
                                padding_y = 5,
                                radius = 2,
                                filled = True
                                ),
                        ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[1],
                        background = colors[1]
                        ),
               widget.Clock(
                        foreground = colors[1],
                        background = colors[1],
                        fontsize = 14,
                        font = "Source Code Pro Bold",
                        format="%A-%d-%B-%Y",
                        decorations = [
                            RectDecoration (
                                colour = colors[7],
                                padding_y = 5,
                                radius = 2,
                                filled = True
                            ),
                        ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[1],
                        background = colors[1]
                        ),
               widget.Clock(
                        foreground = colors[1],
                        background = colors[1],
                        fontsize = 14,
                        font = "Source Code Pro Bold",
                        format="%l:%M%p",
                        decorations = [
                            RectDecoration (
                                colour = colors[8],
                                padding_y = 5,
                                radius = 2,
                                filled = True
                            ),
                        ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[1],
                        background = colors[1]
                        ),


                widget.Net(
                            interface="wlp3s0",
                            font = "Source Code Pro Bold",
                               fontsize=14,
                               format="{down}↓↑{up}",
                               foreground=colors[1],
                               background=colors[1],
                               decorations = [
                                   RectDecoration (
                                   colour = colors[9],
                                   padding_y = 5,
                                   radius = 2,
                                   filled = True
                               ),
                             ],
                          ),
              widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[1],
                        background = colors[1]
                        ),
             #  widget.TextBox(
              #         text = "󰕾",
               #        fontsize = 25,
                #       font = "JetBrainsMono Nerd Font Mono",
                 #      foreground = colors[5]),
               widget.PulseVolume(
                    foreground=colors[1],
                    background = colors[1],
                    fmt="墳 {}",
                    font = "Source Code Pro Bold",
                    fontsize = 14,
                    padding = 5,
                    decorations = [
                            RectDecoration (
                                colour = colors[3],
                                padding_y = 5,
                                radius = 2,
                                filled = True
                            ),
                        ],
                ),
               # battery option 1  ArcoLinux Horizontal icons do not forget to import arcobattery at the top
          #      widget.Sep(
           #              linewidth = 1,
            #             padding = 4,
             #            foreground = colors[2],
              #           background = colors[1]
               #          ),
        #        arcobattery.BatteryIcon(
         #                padding=0,
          #               scale=0.7,
           #              y_poss=2,
            #             theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
             ##            update_interval = 5,
               #          background = colors[1]
                #         ),
                # battery option 2  from Qtile
              widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[1],
                        background = colors[1]
                        ),
                widget.Battery(
                         font="Source Code Pro Bold",
                         update_interval = 10,
                         format = "{char} {percent:2.0%}" ,
                         fontsize = 14,
                         foreground = colors[1],
                         background = colors[1],
                         decorations = [
                            RectDecoration (
                                colour = colors[5],
                                padding_y = 5,
                                radius = 2,
                                filled = True
                            ),
                        ],
	                     ),
                widget.Sep(
                        linewidth = 1,
                        padding = 9,
                        foreground = colors[2],
                        background = colors[1],
                        ),
 #              widget.TextBox(
  #                     text = "⏻ ",
   #                    fontsize = 15,
    #                   font = "Source Code Pro Bold",
     #                  foreground = colors[1],
      #                 background = colors[1],
       #                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("archlinux-logout")},
        #                 decorations = [
         #                   RectDecoration (
          #                      colour = colors[8],
           #                     padding_y = 5,
            #                    radius = 5,
             #                   filled = True
              #              ),
               #         ],
                #       ),
       #         widget.Sep(
        #                linewidth = 1,
         #               padding = 9,
          #              foreground = colors[2],
           #             background = colors[1],
            ##            ),

                widget.UPowerWidget(
                        
                        border_colour = '#d8dee9',
                        border_critical_colour = '#bf616a'
                        ),

                widget.Systray(
                        background = colors[1],
                        icon_size = 20,
                        padding = 4
                        ),
              widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[1],
                        background = colors[1]
                        ),

              widget.Sep(
                        linewidth = 1,
                        padding = 4,
                        foreground = colors[1],
                        background = colors[1]
                        ),
 
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=0.8)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=0.8))]
screens = init_screens()

#  _ __ ___   ___  _   _ ___  ___ 
# | '_ ` _ \ / _ \| | | / __|/ _ \
# | | | | | | (_) | |_| \__ \  __/
# |_| |_| |_|\___/ \__,_|___/\___|

# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

main = None
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #####################################################################################
#     ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
#     #####################################################################################
#     d[group_names[0]] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d[group_names[1]] = [ "Atom", "Subl", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d[group_names[2]] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d[group_names[3]] = ["Gimp", "gimp" ]
#     d[group_names[4]] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d[group_names[5]] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d[group_names[6]] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d[group_names[7]] = ["Thunar", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "thunar", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d[group_names[8]] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d[group_names[9]] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ######################################################################################
#
# wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen(toggle=False)

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME









# For checking virtually
#Xephyr -br -ac -noreset -screen 1280x720 :1 &
#DISPLAY=:1 qtile start

