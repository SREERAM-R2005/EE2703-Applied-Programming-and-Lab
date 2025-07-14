import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Sample coordinates for the keys [(x, y, width, height), ...]
keys = [
    (0, 0, 2, 2),  # Example: key at (0,0) with width=2 and height=2
    (2, 0, 2, 2),
    (4, 0, 2, 2),
    (6, 0, 2, 2),
    (8, 0, 2, 2),
    (10, 0, 2, 2),
]

# Create a figure and axis
fig, ax = plt.subplots()

# Iterate through the keys and add them as rectangles
for key in keys:
    x, y, width, height = key
    rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='black', facecolor='lightgray')
    ax.add_patch(rect)
    
    # Optionally, add labels to the keys
    ax.text(x + width/2, y + height/2, 'Key', fontsize=10, ha='center', va='center')

# Set the limits of the plot to accommodate all keys
ax.set_xlim(-1, 12)
ax.set_ylim(-1, 3)

# Set the aspect ratio to equal to ensure the keys are square
ax.set_aspect('equal')

# Hide axes
ax.axis('off')

# Display the keyboard layout
plt.show()
