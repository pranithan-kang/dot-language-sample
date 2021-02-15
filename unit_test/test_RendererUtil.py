from util.RendererUtil import *

def test_render_entire_graph():
    workflow = [
        {
            "node_id" : "node_1",
            "node_label" : "node_1",
            "actions": [
                { "action": "go", "action_label": "go", "next_node_id": "node_2" },
                { "action": "cancel", "action_label": "cancel", "next_node_id": "end_process" }
            ]
        },
        {
            "node_id" : "node_2",
            "node_label" : "node_2",
            "actions": [
                { "action": "revise", "action_label": "revise", "next_node_id": "node_1" },
                { "action": "go", "action_label": "go", "next_node_id": "node_3" },
                { "action": "cancel", "action_label": "cancel", "next_node_id": "end_process" }
            ]
        },
        {
            "node_id" : "node_3",
            "node_label" : "node_3",
            "actions": [
                { "action": "revise", "action_label": "revise", "next_node_id": "node_2" },
                { "action": "go", "action_label": "go", "next_node_id": "end_process" },
                { "action": "cancel", "action_label": "cancel", "next_node_id": "end_process" }
            ]
        },
        {
            "node_id" : "end_process",
            "node_label" : "end_process"
        }
    ]

    def plain_node_renderer(dot, node):
        dot.node(node["node_id"], node["node_label"])

    def plain_edge_renderer(dot, node, action):
        dot.edge(node["node_id"], action["next_node_id"], label=action["action_label"])

    def plain_graph_renderer(dot):
        assert dot.source == 'digraph workflow {\n\tnode [fontname="TH SarabunPSK"]\n\tedge [fontname="TH SarabunPSK"]\n\tnode_1 [label=node_1]\n\tnode_2 [label=node_2]\n\tnode_3 [label=node_3]\n\tend_process [label=end_process]\n\tnode_1 -> node_2 [label=go]\n\tnode_1 -> end_process [label=cancel]\n\tnode_2 -> node_1 [label=revise]\n\tnode_2 -> node_3 [label=go]\n\tnode_2 -> end_process [label=cancel]\n\tnode_3 -> node_2 [label=revise]\n\tnode_3 -> end_process [label=go]\n\tnode_3 -> end_process [label=cancel]\n}'

    render_entire_graph(workflow, plain_node_renderer, plain_edge_renderer, plain_graph_renderer)