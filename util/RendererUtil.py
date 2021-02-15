from graphviz import Digraph
import glob
from PIL import Image

from graphviz import Digraph

def render_entire_graph(workflow, node_renderer, edge_renderer, output_renderer):
    dot = Digraph("workflow")
    dot.node_attr = { "fontname": "TH SarabunPSK"}
    dot.edge_attr = { "fontname": "TH SarabunPSK"}

    for n in workflow:
        node_renderer(dot, n)

    # an : Nodes with actions
    for n in [an for an in workflow if "actions" in an.keys()]: 
        for a in n["actions"]:
            edge_renderer(dot, n, a)
    output_renderer(dot)