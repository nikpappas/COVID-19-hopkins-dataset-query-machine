LINESTYLES = {
    'solid': '-',
    'dashed': '--',
    'dash-dot': '-.',
    'dotted': ':'
}

COLORS = {
    'tainted-white': (.9, .9, .91),
    'light-grey': (0.2, 0.2, 0.21),
    'dark-grey': (0.1, 0.1, 0.11),
    'white': (1, 1, 1),
}


class AxConfigBuilder:
    def __init__(self, ax):
        self.ax = ax
        self.tick_params = {}

    def withTickColour(self, color):
        return self.withTickParam("colors", color)

    def withAxis(self, axis):
        return self.withTickParam("axis", axis)

    def withTickParam(self, param, value):
        self.tick_params[param] = value
        return self

    def configure(self):
        self.ax.tick_params(**self.tick_params)


def styleFigureDark(fig, ax, axisDateFormatter=None):
    fig.patch.set_facecolor(COLORS['dark-grey'])
    # ax.set_facecolor('xkcd:salmon')
    ax.set_facecolor(COLORS['light-grey'])
    if axisDateFormatter:
        ax.xaxis.set_major_formatter(axisDateFormatter)

    # ax.tick_params(axis='x', colors=(.9, .9, .91))
    AxConfigBuilder(ax)\
        .withAxis('x')\
        .withTickColour(COLORS['tainted-white'])\
        .configure()

    AxConfigBuilder(ax) \
        .withAxis('y') \
        .withTickColour(COLORS['tainted-white']) \
        .configure()


