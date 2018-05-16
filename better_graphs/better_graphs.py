"""
This file acts as a template for building beautiful graphs inspired by the
fantastic book "Trees, Maps and Theorems" by Jean-Luc Doumont.

It also includes a minimum-working example.

For publication-style graphs can be integrated with TEX font rendering.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def make_better_graph(ax, x_new_ticks=None, y_new_ticks=None, **kwargs):
    """Make a graph better"""

    set_limits(ax, **kwargs)

    if x_new_ticks is not None:
        x_new_locs = list(x_new_ticks.keys())
        x_new_labels = list(x_new_ticks.values())
        add_custom_ticks(ax, new_locs=x_new_locs, new_labels=x_new_labels, which='x')

    if y_new_ticks is not None:
        y_new_locs = list(y_new_ticks.keys())
        y_new_labels = list(y_new_ticks.values())
        add_custom_ticks(ax, new_locs=y_new_locs, new_labels=y_new_labels, which='y')


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


def add_custom_ticks(ax, new_locs, new_labels, which='x'):
    """
    Add custom ticks to plot axes `ax` on either the x or y axis at location `newLocs` with tick labels `newLabels`.
    Existing ticks will be overwritten.

    Parameters
    ----------
    ax
    new_locs
    new_labels
    which

    Returns
    -------

    """

    ticks = None
    labels = None

    if which == 'x':
        ticks = ax.get_xticks()
        # hack that fixes a weird bug in mpl where a float will not be rounded correctly, causing havoc
        ticks = [np.round(tick, 9) for tick in ticks]
        ax.set_xticklabels(ticks)  # "Set" ticks must be done to access text
        labels = ax.get_xticklabels()
        labels = [t.get_text() for t in labels]  # Extract text from labels

    elif which == 'y':
        ticks = ax.get_yticks()
        ticks = [np.round(tick, 9) for tick in ticks]  # Same hack as used for xticks above
        ax.set_yticklabels(ticks)
        labels = ax.get_yticklabels()
        labels = [t.get_text() for t in labels]

    tick_dict = dict(zip(ticks, labels))  # Place ticks in dictionary

    # Update tick dictionary
    for loc, lab in zip(new_locs, new_labels):
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


def set_limits(ax, x_factor=0.1, y_factor=0.1, despine=True):
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

    # Trim
    if xticks.size != 0:
        mask = xticks >= min(ax.get_xlim())  # Select all ticks _larger_ than the lower axis limit
        firsttick = xticks[mask][0]  # Select first tick above the axis lower limit

        mask = xticks <= max(ax.get_xlim())  # Select all ticks _smaller_ than the upper axis limit
        lasttick = xticks[mask][-1]  # Select first tick below the axis upper limit

        ax.spines['bottom'].set_bounds(firsttick, lasttick)
        ax.spines['top'].set_bounds(firsttick, lasttick)

        # Mask our new ticks to be within the range of our "cut" axis
        newticks = xticks[xticks <= lasttick]
        newticks = newticks[newticks >= firsttick]

        ax.set_xticks(newticks)

    # y-axis
    yticks = ax.get_yticks()

    # Trim
    if yticks.size != 0:
        mask = yticks >= min(ax.get_ylim())  # Select all ticks _larger_ than the lower axis limit
        firsttick = yticks[mask][0]  # Select first tick above the axis lower limit

        mask = yticks <= max(ax.get_ylim())  # Select all ticks _smaller_ than the upper axis limit
        lasttick = yticks[mask][-1]  # Select first tick below the axis upper limit

        ax.spines['left'].set_bounds(firsttick, lasttick)
        ax.spines['right'].set_bounds(firsttick, lasttick)

        # Mask our new ticks to be within the range of our "cut" axis
        newticks = yticks[yticks <= lasttick]
        newticks = newticks[newticks >= firsttick]

        ax.set_yticks(newticks)

    # Update our working list of ticks
    xticks = ax.get_xticks()
    yticks = ax.get_yticks()

    # Rescale plot area
    x_max = max(xticks)
    x_min = min(xticks)
    y_max = max(yticks)
    y_min = min(yticks)

    ax.set_xlim(x_min - x_max * x_factor, x_max * (x_factor + 1))
    ax.set_ylim(y_min - y_max * y_factor, y_max * (y_factor + 1))

    if despine:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
