import subprocess, shlex
from libqtile.command import lazy
import subprocess


def query_screens():
    output = [l for l in subprocess.check_output(["xrandr"]).decode("utf-8").splitlines()]
    return [l.split()[0] for l in output if " connected " in l]


def get_number_of_screens():
    output = [l for l in subprocess.check_output(["xrandr"]).decode("utf-8").splitlines()][0]
    output = output.split(",")
    output = output[1].split(' ')
    output =  int(output[2])
    if output < 2000:
        return 1
    else :
        return 2
def runone(cmdline):
    """Check if another instance of an app is running, otherwise start a new one."""
    cmd = shlex.split(cmdline)
    try:
        subprocess.check_call(['pgrep', cmd[0]])
    except:
        run(cmdline)

def runone_flatpak(cmdline, pname):

    cmd = shlex.split(cmdline)
    try:
        subprocess.check_call(['pgrep', pname])
    except:
        run(cmdline)


def run(cmdline):
    subprocess.Popen(shlex.split(cmdline))


def is_jetbrains_welcome_window(window):
    wm_name = window.window.get_wm_name()

    lazy.spawn('chromium {}'.format(wm_name))

    if wm_name == 'Welcome to PyCharm':
        return True

    return False


def is_jetbrains_program(window):
    wm_classes = window.window.get_wm_class()
    for wm_class in wm_classes:
        if wm_class.split('-')[0] == 'jetbrains':
            return True
    return False


def is_chromium(window):
    wm_classes = window.window.get_wm_class()
    for wm_class in wm_classes:
        if wm_class == 'chromium' or wm_class == 'Chromium':
            return True
    return False

print(get_number_of_screens())