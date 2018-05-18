import seaborn as sns
import matplotlib.pyplot as plt


def set_pretty_defaults(palette='Set1', context='paper', font_scale=2, line_width=2, tex=True, **kwargs):
    """
    Sets up good-looking default settings for matplotlib
    that form a good basis for 99% of graphs.

    Parameters
    ----------
    palette : string, optional
        Specifies the color palette to use. Uses Seaborn colours.
    context : string, optional
        Specifies the plot context. Uses Seaborn contexts.
    font_scale : int, optional
        Font-scaling to use with given context.
    line_width : float, optional
        Line width to use when drawing plots.
    """
    
    font = 'CMU Serif'
    if 'font' in kwargs:
        font = kwargs['font']

    # Set Seaborn template
    sns.set_style('ticks')
    sns.set_palette(palette)
    sns.set_context(context, font_scale=font_scale)

    # Set Matplotlib tweaks
    plt.rc('xtick', direction='in')
    plt.rc('ytick', direction='in')
    plt.rc('lines', linewidth=line_width)

    # Additional matplotlib rc tweaks
    # plt.rc(**kwargs)

    # Enable LaTeX font rendering
    if tex:
        plt.rc('text', usetex=True)
        plt.rc('font', serif=font)
        plt.rc('font', family='serif')
        plt.rc('text.latex', preamble=r'\usepackage{amsmath}')
