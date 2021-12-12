import colorsys
import math
import pandas
import matplotlib


def color_list_redv(size, green=200, blue=200, curvature=0.3):
    """Get a color gradient as a list of hex values

    This helper returns a list of given length populated with hex values at a consistent
    blue and green level while varying the red level. This is useful for diverging sequences

    Args:
        size (int): Defined size of the list
        green(int): value between 0 and 255. Default to 200
        blue(int): value between 0 and 255. Default to 200
        curvature (float): a value defining the curvature of the color gradient.
                        A lower number pushes the colors at the low end of the gradient closer together and stretches
                        out the colors at the high end, and vice-versa

    Returns:
        A list of hex values
    """
    return ['#%02x%02x%02x' % (round(math.pow((x/size),curvature)*255), green, blue) for x in range(0, size, 1)]

def color_list_lightness(size, hue=0.25, saturation=1, low=0, high=360):
    """Get a color gradient as a list of hex values

    This helper returns a list of given length populated with hex values at a consistent
    hue and saturation level. This is useful for a one dimensional sequence

    Args:
        size (int): Defined size of the list
        lightness(float): value between 0 and 1. Default to 0.75 for a pastel look
        saturation(float): value between 0 and 1. Default to 1
        low (int): hue index value between 0 and 360
        high (int): hue index value between 0 and 360

    Returns:
        A list of hex values
    """

    assert low>=0, "Low range must be greater than or equal to 0"
    assert high<=360, "High range must be less than or equal to 360"
    assert low<high-size, "High must be greater than Low by at least the number of required intervals"

    color = [colorsys.hls_to_rgb(hue, math.pow(x/360,0.8), saturation) for x in range(low, high, round((high-low)/size))]
    return ['#%02x%02x%02x' % (round(x[0]*255), round(x[1]*255), round(x[2]*255)) for x in color]


def color_list(size, lightness=0.75, saturation=1, low=0, high=360):
    """Get a color gradient as a list of hex values

    This helper returns a list of given length populated with hex values at a consistent
    lightness and saturation level. This is useful for categorical values

    Args:
        size (int): Defined size of the list
        lightness(float): value between 0 and 1. Default to 0.75 for a pastel look
        saturation(float): value between 0 and 1. Default to 1
        low (int): hue index value between 0 and 360
        high (int): hue index value between 0 and 360

    Returns:
        A list of hex values
    """
    assert low>=0, "Low range must be greater than or equal to 0"
    assert high<=360, "High range must be less than or equal to 360"
    assert low<high-size, "High must be greater than Low by at least the number of required intervals"
    color = [colorsys.hls_to_rgb(x/360, lightness, saturation) for x in range(low, high, round((high-low)/size))]
    return ['#%02x%02x%02x' % (round(x[0]*255), round(x[1]*255), round(x[2]*255)) for x in color]


def get_plot_legend(df, category, aggs={}, color_type=color_list, **kwargs):
    """Get a color coded legend for plotting

    This helper returns a DataFrame of the levels to be plotted with associated colors

    Args:
        df (DataFrame): A pandas DataFrame
        category (str): The name of the column to groupby
        aggs (dict): A dictionary of strings where the key is the name of the column and the value is the aggregation function
        color_type (func): The color function to use

    Returns:
        A legend DataFrame containing aggregate statistics and a color coded column of hex values
    """
    keep_cols = [x for x in aggs.keys()] + [category]
    legend_sum = (df[keep_cols]
                      .groupby(category, as_index=False)
                      .agg(aggs)
                      .rename(columns={x:x+"_"+str(aggs[x]) for x in aggs})
                     )
    colors = color_type(size=len(legend_sum.index), **kwargs)
    legend_sum['color'] = colors

    return legend_sum, legend_sum.style.apply(lambda col: ['background-color: %s' % (colors[i]) for i in range(len(colors))],
                                  subset=['color']
                                 )


def plot_categoricals(df, ax, plot_legend, category):
    """Plot categoricals by color

    Intended to be used in conjunction with get_plot_legend to plot categoricals by color

    Args:
        df (DataFrame): A pandas DataFrame
        ax (matplotlib ax object): The axis to plot on
        plot_legend (DataFrame): A legend DataFrame output by get_plot_legend with the categorical variable and corresponding color
        category (str): The name of the column to groupby

    Returns:
        A matplotlib plot
    """

    for x in range(len(plot_legend.index)):
        df.loc[df[category] == plot_legend.iloc[x][category]].plot(ax=ax, color=plot_legend.iloc[x]["color"])