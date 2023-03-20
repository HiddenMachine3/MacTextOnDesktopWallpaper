import subprocess
import os
import datetime
import time
from screeninfo import get_monitors

curr_dir = os.path.dirname(os.path.realpath(__file__))
curr_wall = curr_dir + "/" + "original.jpg"
notes = curr_dir + "/" + "notes.txt"

# print(curr_dir, curr_wall, notes)

# --
text_color = "white"  # text color
size = "20"  # text size (real size depends on the scale factor of your wallpaper)
border = 120  # space around your text blocks
columns = 2  # (max) number of columns
n_lines = 10  # (max) number of lines per column


# --

def run_command(cmd):
    exit_code = os.system(cmd)
    if exit_code != 0:  # if the exit code is not normal
        print("Command\n", cmd, "\n", "has exit code", exit_code)
    # subprocess.run(["osascript", "-e", cmd])


def get_monitor_dimensions():
    m = get_monitors()[0]
    w = int(int(m.width) / columns) - 2 * border
    h = int(m.height) - 2 * border
    return w, h


def read_text(file):
    with open(file) as src:
        return [l.strip() for l in src.readlines()]


def slice_lines(lines, n_lines, columns):
    markers = [i for i in range(len(lines)) if i % n_lines == 0]
    last = len(lines)
    markers = markers + [last] if markers[-1] != last else markers
    textblocks = [lines[markers[i]:markers[i + 1]] for i in range(len(markers) - 1)]
    filled_blocks = len(textblocks)
    if filled_blocks < columns:
        for n in range(columns - filled_blocks):
            textblocks.insert(len(textblocks), [])
    for i in range(columns):
        textblocks[i] = ("\n").join(textblocks[i])
    return textblocks[:columns]


def create_section(psize, text, layer):
    run_command("convert -background none -fill " + text_color + " -border " + str(border) +
                " -bordercolor none -pointsize " + size + " -size " + psize +
                " caption:" + '"' + text + '" ' + layer)


def set_overlay():
    # -- INIT
    boxes = slice_lines(read_text(notes), n_lines, columns)
    w, h = get_monitor_dimensions()
    layers = []
    print("width and height : ", w, h)

    # deciding the name of the new desktop image
    datestr = '{date:%Y%m%d_%H_%M_%S}'.format(date=datetime.datetime.now())
    wall_img = curr_dir + "/" + f"walltext_{datestr}.jpg"
    print(wall_img)

    # Remove previous walltext_  images(the previous images which had text in them)
    for img in [img for img in os.listdir(curr_dir) if img.startswith("walltext_")]:
        os.remove(curr_dir + "/" + img)

    # --------

    # - MAKING THE NEW IMAGE
    #   -   -   Making the text mask
    for i in range(len(boxes)):
        layer = curr_dir + "/" + "layer_" + str(i + 1) + ".png"
        create_section(str(w) + "x" + str(h), boxes[i], layer)
        layers.append(layer)
    run_command("convert " + " ".join(layers) + " " + "+append " + curr_dir + "/" + "layer_span.png")

    #   -   -   Transferring text mask onto background  image
    run_command(
        "convert " + curr_wall + " " + curr_dir + "/" + "layer_span.png" + " -background None -layers merge " + wall_img)

    # - UPDATING THE DESKTOP BACKGROUND IMAGE
    subprocess.run(["osascript", "-e",
                    f'tell application "System Events" to tell every desktop to set picture to "{wall_img}" as POSIX file'])
    """
    This is a little better than the "tell application Finder" method. It changes the backgrounds of all 
    visible desktops. So, it works on multiple monitors, unlike the Finder one. However, it doesn't change 
    the backgrounds of desktops that aren't currently visible
    
    For reference, this was the command using Finder
    #cmd = f'osascript -e \'tell application "Finder" to set desktop picture to POSIX file "{wall_img}"\''
    """
    # -

    # - CLEANUP
    for img in [img for img in os.listdir(curr_dir) if img.startswith("layer_")]:
        os.remove(curr_dir + "/" + img)
    # -


while True:
    text_1 = read_text(notes)
    print(text_1)
    time.sleep(5)
    text_2 = read_text(notes)
    if text_2 != text_1:  # If there is a change, then it will update the wallpaper
        set_overlay()
