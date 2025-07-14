import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
from collections import defaultdict
import numpy as np
import matplotlib.colors as mcolors

# Define the layout with adjusted positions
characters = {
    # Lowercase letters (unchanged)
    "a": ("a",),
    "b": ("b",),
    "c": ("c",),
    "d": ("d",),
    "e": ("e",),
    "f": ("f",),
    "g": ("g",),
    "h": ("h",),
    "i": ("i",),
    "j": ("j",),
    "k": ("k",),
    "l": ("l",),
    "m": ("m",),
    "n": ("n",),
    "o": ("o",),
    "p": ("p",),
    "q": ("q",),
    "r": ("r",),
    "s": ("s",),
    "t": ("t",),
    "u": ("u",),
    "v": ("v",),
    "w": ("w",),
    "x": ("x",),
    "y": ("y",),
    "z": ("z",),
    # Uppercase letters (updated)
    "A": ("Shift_R", "a"),
    "B": ("Shift_R", "b"),
    "C": ("Shift_R", "c"),
    "D": ("Shift_R", "d"),
    "E": ("Shift_R", "e"),
    "F": ("Shift_R", "f"),
    "G": ("Shift_R", "g"),
    "H": ("Shift_L", "h"),
    "I": ("Shift_L", "i"),
    "J": ("Shift_L", "j"),
    "K": ("Shift_L", "k"),
    "L": ("Shift_L", "l"),
    "M": ("Shift_L", "m"),
    "N": ("Shift_L", "n"),
    "O": ("Shift_L", "o"),
    "P": ("Shift_L", "p"),
    "Q": ("Shift_R", "q"),
    "R": ("Shift_R", "r"),
    "S": ("Shift_R", "s"),
    "T": ("Shift_R", "t"),
    "U": ("Shift_L", "u"),
    "V": ("Shift_R", "v"),
    "W": ("Shift_R", "w"),
    "X": ("Shift_R", "x"),
    "Y": ("Shift_L", "y"),
    "Z": ("Shift_R", "z"),
    # Numbers and their shifted symbols (updated)
    "1": ("1",),
    "!": ("Shift_R", "1"),
    "2": ("2",),
    "@": ("Shift_R", "2"),
    "3": ("3",),
    "#": ("Shift_R", "3"),
    "4": ("4",),
    "$": ("Shift_R", "4"),
    "5": ("5",),
    "%": ("Shift_R", "5"),
    "6": ("6",),
    "^": ("Shift_L", "6"),
    "7": ("7",),
    "&": ("Shift_L", "7"),
    "8": ("8",),
    "*": ("Shift_L", "8"),
    "9": ("9",),
    "(": ("Shift_L", "9"),
    "0": ("0",),
    ")": ("Shift_L", "0"),
    # Other symbols (updated)
    "`": ("`",),
    "~": ("Shift_R", "`"),
    "-": ("-",),
    "_": ("Shift_L", "-"),
    "=": ("=",),
    "+": ("Shift_L", "="),
    "[": ("[",),
    "{": ("Shift_L", "["),
    "]": ("]",),
    "}": ("Shift_L", "]"),
    "\\": ("\\",),
    "|": ("Shift_L", "\\"),
    ";": (";",),
    ":": ("Shift_L", ";"),
    "'": ("'",),
    '"': ("Shift_L", "'"),
    ",": (",",),
    "<": ("Shift_L", ","),
    ".": (".",),
    ">": ("Shift_L", "."),
    "/": ("/",),
    "?": ("Shift_L", "/"),
    # Space (unchanged)
    " ": ("Space",),
}

QWERTY_LAYOUT = {
    "row1": {
        "keys": "`1234567890-=",
        "positions": [
            (0, 4),
            (1.5, 4),
            (3, 4),
            (4.5, 4),
            (6, 4),
            (7.5, 4),
            (9, 4),
            (10.5, 4),
            (12, 4),
            (13.5, 4),
            (15, 4),
            (16.5, 4),
            (18, 4),
        ],
    },
    "row2": {
        "keys": "qwertyuiop[]",
        "positions": [
            (2.5, 3),
            (4.0, 3),
            (5.5, 3),
            (7, 3),
            (8.5, 3),
            (10, 3),
            (11.5, 3),
            (13, 3),
            (14.5, 3),
            (16, 3),
            (17.5, 3),
            (19, 3),
        ],
    },
    "row3": {
        "keys": "asdfghjkl;'",
        "positions": [
            (3, 2),
            (4.5, 2),
            (6, 2),
            (7.5, 2),
            (9, 2),
            (10.5, 2), (13, 3)
            (12, 2),
            (13.5, 2),
            (15, 2),
            (16.5, 2),
            (18, 2),
        ],
    },
    "row4": {
        "keys": "zxcvbnm,./",
        "positions": [
            (4, 1),
            (5.5, 1),
            (7, 1),
            (8.5, 1),
            (10, 1),
            (11.5, 1),
            (13, 1),
            (14.5, 1),
            (16, 1),
            (17.5, 1),
        ],
    },
    "special_keys": {
        "Shift_L": (0, 1),
        "Shift_R": (19, 1),
        "Space": (6, 0),
        "Backspace": (19.5, 4),
        "Tab": (0, 3),
        "CapsLock": (0, 2),
        "Enter": (19.5, 2),
        "\\": (20.5, 3),
    },
}

home_row = {
    "a": (3, 2),
    "s": (4.5, 2),
    "d": (6, 2),
    "f": (7.5, 2),
    "j": (13, 2),
    "k": (14.5, 2),
    "l": (16, 2),
    ";": (17.5, 2),
}

key_dict = (
    {}
)  # a dictionary which contains the keys and the values as their coordinates.
for row in QWERTY_LAYOUT:  # A for loop to populate the key_dict
    if row != "special_keys":
        for j in range(len(QWERTY_LAYOUT[row]["keys"])):
            key_dict[QWERTY_LAYOUT[row]["keys"][j]] = QWERTY_LAYOUT[row]["positions"][j]
for i in QWERTY_LAYOUT["special_keys"]:
    key_dict[i] = QWERTY_LAYOUT["special_keys"][i]

"""
calc_distance function first finds out the home key which is nearest to the input text key 
in order to find the starting position of the finger. Tis is done by calulating the distance
from all the keys in the home row to the input key and finding the key in the homerow 
for which the distance is minimum After figuring out the home key the euclidean distance
formula is used to calculate the distance between the two keys. Though
the actual distance is twice of this, its disregarded as mentioned int he problem statement. 
"""


def calc_distance(text):
    tot_distance = 0
    for key in text:
        if key == " ":
            continue
        for keys in characters[key]:
            x2 = key_dict[keys][0]
            y2 = key_dict[keys][1]

            min = 1000
            home_row_char = ""
            # finding the home row keyto be used
            for j in home_row:
                x1 = home_row[j][0]
                y1 = home_row[j][1]
                dist = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
                if dist < min:
                    min = dist
                    home_row_char = j

            x1 = key_dict[home_row_char][0]
            y1 = key_dict[home_row_char][1]
            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            tot_distance += dist
    return tot_distance


# Function to draw a key with a given color and optional width/height using Rectangle
def draw_key(ax, label, position, color, width=1.5, height=1):
    x, y = position
    rect = patches.Rectangle(  # Used to draw rectangular key
        (x, y),
        width,
        height,
        edgecolor="black",
        facecolor=color,
        linewidth=1,
        alpha=0.5,
    )
    ax.add_patch(rect)

    ax.text(
        x + width / 2,
        y + height / 2,
        label,
        fontsize=10,
        ha="center",
        va="center",
        color="black",
        fontweight="bold",
    )


# scales the value between 0 and 1 to associate each key'color to its relative frequency
def normalize(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)


# get colormap
colors = ["blue", "green", "yellow", "orange", "red"]
blue_red = mcolors.LinearSegmentedColormap.from_list("blue_red", colors)
cmap = blue_red


# counter function calculates the frequency of occurence of various keys in the input text
def counter(input_text: str) -> dict:
    frequencies = defaultdict(int)
    for char in input_text:
        keys = characters[char]
        for key in keys:
            if key == "Space":
                continue
            frequencies[key] += 1
    return frequencies


# Function to create heatmap based on input string
def create_keyboard_heatmap(input_text: str):
    frequency = counter(input_text)  # Count frequency of each character
    fig, ax = plt.subplots(figsize=(15, 6))
    # Get total number of keys for normalizing color based on frequency
    all_keys = [
        key
        for row in QWERTY_LAYOUT
        if row != "special_keys"
        for key in QWERTY_LAYOUT[row]["keys"]
    ]
    max_freq = max(frequency.values()) if frequency else 1  # Avoid division by zero

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=max_freq))
    sm.set_array([])

    # plot the main keys with a colormap based on frequency
    for row in QWERTY_LAYOUT:
        if row != "special_keys":
            keys = QWERTY_LAYOUT[row]["keys"]
            positions = QWERTY_LAYOUT[row]["positions"]
            for key, pos in zip(keys, positions):
                key_freq = frequency.get(
                    key, 0
                )  # Get the frequency of the key, 0 if not in input
                color_value = cmap(normalize(key_freq, 0, max_freq))
                draw_key(ax, key, pos, color_value)

    special_keys = QWERTY_LAYOUT["special_keys"]
    special_key_widths = {
        "Shift_L": 4,
        "Shift_R": 3.5,
        "Space": 12,
        "Backspace": 3,
        "Tab": 2.5,
        "CapsLock": 3,
        "Enter": 3,
        "\\": 2,
    }

    for key, pos in special_keys.items():
        key_freq = frequency.get(  # get the frequency of the key, 0 if not in input
            key, 0
        )
        color_value = cmap(
            normalize(key_freq, 0, max_freq)
        )  # normalizes the frequency to get the color_value
        width = special_key_widths.get(
            key, 2
        )  # key width is set to 2 as default unless specified
        draw_key(ax, key, pos, color=color_value, width=width)

    ax.set_xlim(-1, 30)
    ax.set_ylim(-1, 6)
    ax.set_aspect("equal")
    ax.axis("off")

    # Adds the color bar to the plot
    cbar = plt.colorbar(sm, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label("Key Press Frequency", fontsize=12)
    plt.savefig("hmap.png")


input_text = input("Enter text : ")
print(calc_distance(input_text))

create_keyboard_heatmap(input_text)
