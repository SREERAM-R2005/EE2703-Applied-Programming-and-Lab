
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
from collections import defaultdict
import numpy as np
import matplotlib.colors as mcolors
import random
from matplotlib.animation import FuncAnimation

# QWERTY Keyboard layout data

keys = {
    # Number row
    "`": {"pos": (0, 4), "start": "a"},
    "1": {"pos": (1.5, 4), "start": "a"},
    "2": {"pos": (3, 4), "start": "a"},
    "3": {"pos": (4.5, 4), "start": "s"},
    "4": {"pos": (6, 4), "start": "d"},
    "5": {"pos": (7.5, 4), "start": "f"},
    "6": {"pos": (9, 4), "start": "j"},
    "7": {"pos": (10.5, 4), "start": "j"},
    "8": {"pos": (12, 4), "start": "k"},
    "9": {"pos": (13.5, 4), "start": "l"},
    "0": {"pos": (15, 4), "start": ";"},
    "-": {"pos": (16.5, 4), "start": ";"},
    "=": {"pos": (18, 4), "start": ";"},
    # Top letter row
    "q": {"pos": (2.5, 3), "start": "a"},
    "w": {"pos": (4, 3), "start": "s"},
    "e": {"pos": (5.5, 3), "start": "d"},
    "r": {"pos": (7, 3), "start": "f"},
    "t": {"pos": (8.5, 3), "start": "f"},
    "y": {"pos": (10, 3), "start": "j"},
    "u": {"pos": (11.5, 3), "start": "j"},
    "i": {"pos": (13, 3), "start": "k"},
    "o": {"pos": (14.5, 3), "start": "l"},
    "p": {"pos": (16, 3), "start": ";"},
    "[": {"pos": (17.5, 3), "start": ";"},
    "]": {"pos": (19, 3), "start": ";"},
    "\\": {"pos": (21.5, 3), "start": ";"},
    # Home row
    "a": {"pos": (3, 2), "start": "a"},
    "s": {"pos": (4.5, 2), "start": "s"},
    "d": {"pos": (6.0, 2), "start": "d"},
    "f": {"pos": (7.5, 2), "start": "f"},
    "g": {"pos": (9, 2), "start": "f"},
    "h": {"pos": (10.5, 2), "start": "j"},
    "j": {"pos": (12, 2), "start": "j"},
    "k": {"pos": (13.5, 2), "start": "k"},
    "l": {"pos": (15, 2), "start": "l"},
    ";": {"pos": (16.5, 2), "start": ";"},
    "'": {"pos": (18, 2), "start": ";"},
    # Bottom letter row
    "z": {"pos": (4, 1), "start": "a"},
    "x": {"pos": (5.5, 1), "start": "s"},
    "c": {"pos": (7, 1), "start": "d"},
    "v": {"pos": (8.5, 1), "start": "f"},
    "b": {"pos": (10, 1), "start": "f"},
    "n": {"pos": (11.5, 1), "start": "j"},
    "m": {"pos": (13, 1), "start": "j"},
    ",": {"pos": (14.5, 1), "start": "k"},
    ".": {"pos": (16, 1), "start": "l"},
    "/": {"pos": (17.5, 1), "start": ";"},
    # Special keys
    "Shift_L": {"pos": (0, 1), "start": "a"},
    "Shift_R": {"pos": (19, 1), "start": ";"},
    "Backspace": {"pos": (19.5, 4), "start": ";"},
    "Tab": {"pos": (0, 3), "start": "a"},
    "Space": {"pos": (6, 0), "start": "f"},
    "Capslock": {"pos": (0, 2), "start": "a"},
    "Enter": {"pos": (19.5, 2), "start": ";"},
    "\\": {"pos": (20.5, 3), "start": ";"},
}

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

special_keys = [
    "Shift_L",
    "Shift_R",
    "Backspace",
    "Tab",
    "Space",
    "Enter",
    "Capslock",
    "\\",
]

# Converting the "start" element in the keys dictionary to its coordinates for easy access.
for i in keys.keys():
    char = keys[i]["start"]
    keys[i]["start"] = keys[char]["pos"]


# Function for calculating euclidean distance between two keys
def calc_distance(keys, text):
    tot_distance = 0
    for char in text:
        if char == " ":
            continue
        for key in characters[char]:
            x2 = keys[key]["pos"][0]
            y2 = keys[key]["pos"][1]
            x1 = keys[key]["start"][0]
            y1 = keys[key]["start"][1]

            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            tot_distance += dist
    return tot_distance


def get_new_layout(current_layout):
    # Create a copy of the current layout
    new_layout = current_layout.copy()
    # Get only the non-special keys for swapping
    non_special_keys = [key for key in new_layout if key not in special_keys]
    # Randomly selecting two non-special keys to swap
    key1, key2 = random.sample(non_special_keys, 2)
    # Swap their positions
    new_layout[key1], new_layout[key2] = new_layout[key2], new_layout[key1]

    return new_layout


def simulated_annealing(layout, initial_temp, cooling_rate, num_iterations, input_text):
    # Initial route and distance
    current_layout = layout
    # Calculating the distance travelled to type the input_text using the current layout
    current_distance = calc_distance(current_layout, input_text)

    # Initialising the best layout and the best distance as current layout and current distance respectively
    best_layout = current_layout.copy()
    best_distance = current_distance

    temp = initial_temp
    # Storing the distances and the best distances as arrays in order to plot
    distances = [current_distance]
    best_distances = [best_distance]

    for i in range(num_iterations):

        # getting the newlayout by swapping two randomly chosen keys
        new_layout = get_new_layout(current_layout)
        new_distance = calc_distance(new_layout, input_text)
        # Acceptance probability
        try:
            p = np.exp((current_distance - new_distance) / temp)
        except:                                                    #This is done to tackle overflow
            p = 1000000000
        if new_distance < current_distance or random.random() < p:
            current_layout = new_layout
            current_distance = new_distance

            if current_distance < best_distance:
                best_layout = current_layout.copy()
                best_distance = current_distance

        temp *= cooling_rate
        distances.append(current_distance)
        best_distances.append(best_distance)

    return best_layout, best_distances, distances


# Function to draw a key with a given color and optional width/height using Rectangle
def draw_key(ax, label, position, color, width=1.5, height=1):
    x, y = position
    rect = patches.Rectangle(
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


# Function to normalize values for the color map
def normalize(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)


# Create a custom colormap
colors = ["blue", "green", "yellow", "orange", "red"]
blue_red = mcolors.LinearSegmentedColormap.from_list("blue_red", colors)
cmap = blue_red

# Special key widths for non-standard keys
special_key_widths = {
    "Shift_L": 4,
    "Shift_R": 3.5,
    "Space": 12,
    "Backspace": 3,
    "Tab": 2.5,
    "Capslock": 3,
    "Enter": 3,
    "\\": 2,
}


# Counter function to calculate the frequency of keys
def counter(input_text: str) -> dict:
    frequencies = defaultdict(int)
    for char in input_text:
        char = characters.get(
            char, ()
        )  # Get the character's mapped keys from `characters`
        for key in char:
            if key in special_keys:  # Avoid counting special keys for each character
                continue
            frequencies[key] += 1
    return frequencies


def create_keyboard_heatmap(input_text: str, layout: dict):
    frequency = counter(input_text)
    fig, ax = plt.subplots(figsize=(15, 6))

    # Flatten all keys for normalization
    all_keys = list(layout.keys())
    max_freq = max(frequency.values()) if frequency else 1

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=max_freq))
    sm.set_array([])

    # Plot keys based on the modified layout
    for key, key_info in layout.items():
        pos = key_info["pos"]  # Get the position of the key
        key_freq = frequency.get(key, 0)  # Get the frequency of the key, 0 if not used
        color_value = cmap(
            normalize(key_freq, 0, max_freq)
        )  # Normalize color based on frequency
        width = special_key_widths.get(
            key, 1.5
        )  # Use default width of 1.5 unless a special key
        draw_key(ax, key, pos, color=color_value, width=width)

    ax.set_xlim(-1, 30)
    ax.set_ylim(-1, 6)
    ax.set_aspect("equal")
    ax.axis("off")
    # Add color bar
    cbar = plt.colorbar(sm, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label("Key Press Frequency", fontsize=12)

    plt.savefig("keyboard_heatmap.png")


# Setting the parameters
initial_temp = 1000
cooling_rate = 0.98
num_iterations = 1000


# Input text
input_text = input("Enter text: ")

# Run simulated annealing
best_layout, best_distances, distances = simulated_annealing(
    keys, initial_temp, cooling_rate, num_iterations, input_text
)

# Display the best distance
print("Best Distance:", best_distances[-1])

# Displaying the heatmap for the best layout obtained from simulated annealing
create_keyboard_heatmap(input_text, best_layout)


def update(frame, best_distances, distances, distance_line, cur_dist_line):
    # Update the distance line data for best distances up to the current frame
    distance_line.set_data(range(frame + 1), best_distances[: frame + 1])

    # Update the current distance line data for the current frame
    cur_dist_line.set_data(range(frame + 1), distances[: frame + 1])

    return distance_line, cur_dist_line


def main():
    # Set up the figure
    fig, ax1 = plt.subplots(figsize=(10, 5))
    fig.suptitle("Simulated Annealing Distance over Iterations")

    # Set up the plot limits
    ax1.set_xlim(0, num_iterations)
    ax1.set_ylim(min(best_distances) - 10, max(distances) + 10)
    ax1.set_title("Layout Optimization")
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Distance")

    # Initialize the lines that will be updated in the animation
    (distance_line,) = ax1.plot([], [], "r-", label="Best Distance")
    (cur_dist_line,) = ax1.plot([], [], "b-", label="Current Distance")

    ax1.legend()

    # Create the animation
    anim = FuncAnimation(
        fig,
        update,
        frames=range(0, num_iterations),
        fargs=(best_distances, distances, distance_line, cur_dist_line),
        interval=50,
        blit=True,
        repeat=False,
    )

    anim.save("animation.gif", writer="pillow", fps=30)


# Run the animation
main()
