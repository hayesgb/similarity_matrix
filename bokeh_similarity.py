import numpy as np
from operator import itemgetter
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

class SimilarityMatrix:
    '''
    This class accepts a dictionary of lists called "data" that contains two lists, with keys "nodes" and "links".
    The "nodes" list is itself a dictionary with keys of "name" and "group"
    The "links" list is itself a dictionary with keys "source", "value", and "target"
    '''

    colormap = ["#444444", "#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f",
                "#ff7f00", "#cab2d6", "#6a3d9a"]

    def __init__(self, data):
        self._nodes = data.get('nodes')
        self._links = data.get('links')
        self._xname = []
        self._yname = []
        self._color = []
        self._alpha = []

    def get_nodes(self):
        return(self._nodes)

    def set_column_variables(self):
        N = len(self._nodes)
        self._names = [node['name'] for node in sorted(self._nodes, key=itemgetter('group'))]
        self._counts = np.zeros((N, N))
        for link in self._links:
            self._counts[link['source'], link['target']] = link['value']
            self._counts[link['target'], link['source']] = link['value']
        for i, node1 in enumerate(self._nodes):
            for j, node2 in enumerate(self._nodes):
                self._xname.append(node1['name'])
                self._yname.append(node2['name'])
                self._alpha.append(min(self._counts[i,j]/4.0, 0.9) + 0.1)
                if node1['group'] == node2['group']:
                    self._color.append(self.colormap[node1['group']])
                else:
                    self._color.append('lightgrey')
        return self._xname, self._yname, self._color, self._alpha, self._names

    def get_column_source_data(self):
        self._source = ColumnDataSource(data=dict(xname=self._xname,
                                                  yname=self._yname,
                                                  colors = self._color,
                                                  alphas = self._alpha,
                                                  count = self._counts.flatten()))
        return self._source

    def create_plot(self):
        p = figure(title='Title', x_axis_location='above', tools='hover, save, box_zoom, reset', x_range=list(reversed(self._names)),
                   y_range=self._names)
        p.plot_width = 800
        p.plot_height = 800
        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.axis.major_label_text_font_size = "5pt"
        p.axis.major_label_standoff = 0
        p.xaxis.major_label_orientation = np.pi/3
        p.rect('xname', 'yname', 0.9, 0.9, source=self._source, color='colors', alpha='alphas', line_color=None,
               hover_line_color='black', hover_color='colors')
        output_file('test.html')
        show(p)

def main():
    from bokeh.sampledata.les_mis import data
    plot = SimilarityMatrix(data=data)
    print(plot.get_nodes())
    plot.set_column_variables()
    print(plot.set_column_variables())
    plot.get_column_source_data()
    plot.create_plot()


if __name__ == '__main__':  main()
