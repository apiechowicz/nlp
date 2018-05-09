from os import getcwd, makedirs
from os.path import join, isdir
from typing import Dict, Tuple

from matplotlib import pylab
from networkx import draw_networkx_edge_labels, DiGraph, draw_networkx, circular_layout

OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)


def save_data(data: str, file_name: str) -> None:
    create_output_dir(OUTPUT_DIRECTORY_PATH)
    with open(join(OUTPUT_DIRECTORY_PATH, file_name), 'w') as file:
        file.write(data)


def create_output_dir(path: str) -> None:
    if not isdir(path):
        makedirs(path)


def save_graph(data: DiGraph, edge_labels: Dict[Tuple[str, str], str], file_name: str) -> None:
    create_output_dir(OUTPUT_DIRECTORY_PATH)
    pylab.figure(figsize=(16, 12), dpi=72)
    pylab.axis('off')
    pos = circular_layout(data)
    node_sizes = [250 * len(node) for node in data.nodes._nodes.keys()]
    draw_networkx(data, pos, node_size=node_sizes, node_color='c')
    draw_networkx_edge_labels(data, pos, edge_labels=edge_labels)
    pylab.savefig(join(OUTPUT_DIRECTORY_PATH, file_name))
