import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from better_graphs.defaults import set_pretty_defaults
from better_graphs.better_graphs import set_limits, add_custom_ticks

# Data for Plot
x = np.arange(0, 100, 1)
y1 = np.sin(x / 10)
y2 = np.cos(x / 20)

# Let's set the defaults (lots of customization possible)
set_pretty_defaults()

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(x, y1, label='A')
plt.plot(x, y2, label='B')
plt.legend()

# Customization
sns.despine()

# Regular ticks recommended to be limited to three points
# This is unlike Trees, Maps and Theorems, which often shows only two.
# Three points allows user to identify if graph is linear or log scale.
plt.xticks([0, 50, 100])  # Xticks customized here
plt.yticks([-1, 0, 1])  # Yticks customized here

# Set plot limits roughly 10% above / below the max/min values respectively
# and sets spines to match the maximum and minimum tick values
set_limits(ax, x_factor=0.1, y_factor=0.1, spines=True)

# Special ticks
# Can be used to show units as well, which can then be ommitted from x/ylabel
add_custom_ticks(ax, [25, 75], ['0.25s', '0.75s'], 'x')
add_custom_ticks(ax, [0.75], ['0.75W'], 'y')

# Axis labels
plt.xlabel('Time')
plt.ylabel('Power')

plt.tight_layout()  # Fits plot nicely to screen
plt.show()