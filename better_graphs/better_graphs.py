"""
This file acts as a template for building beautiful graphs inspired by the
fantastic book "Trees, Maps and Theorems" by Jean-Luc Doumont.

It also includes a minimum-working example.

For publication-style graphs can be integrated with TEX font rendering.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def beautify_bars_h(ax, index, rounding=2, factor=0.1, num_bars_per_group=1):
    """
    Beautify a horizontal bar plot.

    Parameters
    ----------
    ax : matplotlib axis object
      Axis containing bar plot that must be made pretty
    index : array-like
      Index value of the FIRST set of bars that are plotted on `ax`.
    rounding : float {2}
      The number of decimal places to round annotate text values to
    factor : float, {0.1}
      Controls the horizontal spacing of the various design elements
    num_bars_per_group : float, {1}
      Specifies how many bars make up each "group".

    Returns
    -------
    None
    """
    max_value = 0
    num = len(ax.patches)
    p0 = ax.patches[0]

    # If more than one bar grouped together
    if num_bars_per_group > 1:
        p1 = ax.patches[int(num / num_bars_per_group)]
        gap = p1.get_y() - p0.get_y() - p0.get_height()
        gap = np.round(gap, 3)
    else:
        gap = 0

    width = p0.get_height()  # `Width` of bar is the height of the patch

    # Calculate y-tick placement to be centered in group of bars
    yticks = index + ((num_bars_per_group - 1) / 2 * (width + gap))

    # Find where to extend the plot area to
    for p in ax.patches:
        if p.get_width() > max_value:
            max_value = p.get_width()

    ax.set_xticks([])  # set x-ticks
    ax.set_xlim(-factor * max_value,
                max_value * (1 + 3 * factor))  # Sets xlimits
    ax.set_yticks(yticks)  # Sets yticks
    ax.tick_params(axis='y', which='both', length=0)  # Removes ytick marks

    # The right-edge to which the lines must go.
    edge = max_value * (1 + factor + 0.5 * factor)
    # The left-edge of the value text.
    font_begin = max_value * (1 + 2 * factor + 0.5 * factor)

    # For each bar
    for p in ax.patches:
        val = np.round(p.get_width(), rounding)  # Round its value
        # Draw the value as text on right-margin
        ax.annotate(
            val,
            xy=(p.get_x() + font_begin, p.get_y() + gap / 2),
            horizontalalignment='left',
            xycoords='data')

        # Draw the lines from bar to edge
        xs = [p.get_width(), edge]
        ys = [p.get_y() + p.get_height() / 2, p.get_y() + p.get_height() / 2]
        ax.plot(xs, ys, color='k', linewidth=1)

        # Remove spines
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)


def add_custom_ticks(ax, newLocs, newLabels, which='x'):
    """
    Add custom ticks to plot axes `ax` on either the x or y axis at location `newLocs` with tick labels `newLabels`.
    Existing ticks will be overwritten.

    Parameters
    ----------
    ax
    newLocs
    newLabels
    which

    Returns
    -------

    """

    locs = None
    labels = None

    if which == 'x':
        xticks = ax.get_xticks()
        ax.set_xticklabels(xticks)  # "Set" ticks must be done to access text
        locs, labels = plt.xticks()  # Get xticks
        labels = [x.get_text() for x in labels]  # Extract text from labels
    elif which == 'y':
        yticks = ax.get_yticks()
        ax.set_yticklabels(yticks)
        locs, labels = plt.yticks()
        labels = [x.get_text() for x in labels]

    tick_dict = dict(zip(locs, labels))  # Place ticks in dictionary

    # Update tick dictionary
    for loc, lab in zip(newLocs, newLabels):
        tick_dict[loc] = lab

    # Extract tick locations and labels
    locs = list(tick_dict.keys())
    labels = list(tick_dict.values())

    # Set new Ticks
    if which == 'x':
        ax.set_xticks(locs)
        ax.set_xticklabels(labels)
    elif which == 'y':
        ax.set_yticks(locs)
        ax.set_yticklabels(labels)


def set_limits(ax, x_factor=0.1, y_factor=0.1, spines=True):
    """
    Set the limits of the axes, have them end with ticks.

    Parameters
    ----------
    ax
    x_factor
    y_factor
    spines

    Returns
    -------

    """

    # x-axis
    xticks = ax.get_xticks()
    ax.set_xticklabels(xticks)  # Must be set before getting access
    locs, labels = plt.xticks()

    x_max = np.max(locs)
    x_min = np.min(locs)

    # y-axis
    yticks = ax.get_yticks()
    ax.set_yticklabels(yticks)
    locs, labels = plt.yticks()

    y_max = np.max(locs)
    y_min = np.min(locs)

    ax.set_xlim(x_min - x_max * x_factor,
                x_max * (x_factor + 1))  # Sets x limits
    ax.set_ylim(y_min - y_max * y_factor,
                y_max * (y_factor + 1))  # Sets y limits

    if spines:
        ax.spines['bottom'].set_bounds(x_min, x_max)
        ax.spines['left'].set_bounds(y_min, y_max)


