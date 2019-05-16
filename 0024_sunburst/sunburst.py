import matplotlib.pyplot as plt
import numpy as np


def sunburst(nodes, total=np.pi * 2, offset=0, level=0, ax=None):
    ax = ax or plt.subplot(111, projection='polar')

    if level == 0 and len(nodes) == 1:
        label, value, subnodes = nodes[0]
        ax.bar([0], [0.5], [np.pi * 2])
        ax.text(0, 0, label, ha='center', va='center')
        sunburst(subnodes, total=value, level=level + 1, ax=ax)
    elif nodes:
        d = np.pi * 2 / total
        labels = []
        widths = []
        local_offset = offset
        for label, value, subnodes in nodes:
            label = '{}:({})'.format(label, value)
            labels.append(label)
            widths.append(value * d)
            sunburst(subnodes, total=total, offset=local_offset,
                     level=level + 1, ax=ax)
            local_offset += value
        values = np.cumsum([offset * d] + widths[:-1])
        heights = [1] * len(nodes)
        bottoms = np.zeros(len(nodes)) + level - 0.5
        rects = ax.bar(values, heights, widths, bottoms, linewidth=1,
                       edgecolor='white', align='edge')
        for rect, label in zip(rects, labels):
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + rect.get_height() / 2
            rotation = (90 + (360 - np.degrees(x) % 180)) % 360
            ax.text(x, y, label, rotation=rotation, ha='center', va='center')

    if level == 0:
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')
        ax.set_axis_off()


def split_df(df, current_layer):
    dfs = {}
    for value in df[current_layer].unique():
        dfs[value] = df.loc[df[current_layer] == value]

    return dfs


def fill_info(info, sub_dfs, layers):
    if layers:
        current_layer = layers[0]
    else:
        current_layer = None

    left_layers = layers[1:]

    for value, sub_df in sub_dfs.items():
        sub_info = (value, len(sub_df), [])

        if current_layer is not None:
            new_sub_dfs = split_df(sub_df, current_layer)

            fill_info(sub_info, new_sub_dfs, left_layers)

        info[2].append(sub_info)

    return info


class HierarchicalSample:
    def __init__(self, df, minimun=10000):
        self.df = df
        self.minimun = minimun

    def get_size(self, layers):
        size_info = []

        current_layer = layers[0]
        left_layers = layers[1:]

        sub_dfs = split_df(self.df, current_layer)

        info = ('all', len(self.df), [])
        fill_info(info, sub_dfs, left_layers)

        return [info]


def visualize(df, layers, output_path):
    h = HierarchicalSample(df)
    nodes = h.get_size(layers)

    f = plt.figure(figsize=(50, 50))

    sunburst(nodes)

    f.savefig(output_path)
