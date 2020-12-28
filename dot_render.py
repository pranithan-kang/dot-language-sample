# %%
from graphviz import render, Source

src = Source.from_file("render_pdf/test.gv", engine="neato")

src.render()

# %%
from graphviz import Digraph, render
import glob
from PIL import Image

workflow = [
    {
        "node_id" : "drafter",
        "node_label" : "ผู้ร่างเอกสาร",
        "actions": [
            { "action": "submit", "action_label": "Submit", "next_node_id": "supervisor" },
            { "action": "cancel", "action_label": "Cancel", "next_node_id": "end_process" }
        ]
    },
    {
        "node_id" : "supervisor",
        "node_label" : "หัวหน้า",
        "actions": [
            { "action": "revise", "action_label": "Revise", "next_node_id": "drafter" },
            { "action": "approve_low_budget", "action_label": "Approve\\n(low budget)", "next_node_id": "end_process" },
            { "action": "approve_medium_budget", "action_label": "Approve\\n(medium budget)", "next_node_id": "department_manager" }
        ]
    },
    {
        "node_id" : "department_manager",
        "node_label" : "ผู้จัดการแผนก",
        "actions": [
            { "action": "revise", "action_label": "Revise", "next_node_id": "supervisor" },
            { "action": "approve", "action_label": "Approve", "next_node_id": "end_process" },
            { "action": "approve_high_budget", "action_label": "Approve\\n(high budget)", "next_node_id": "management_director" }
        ]
    },
    {
        "node_id" : "management_director",
        "node_label" : "ผู้อำนวยการฝ่ายบริหาร",
        "actions": [
            { "action": "revise", "action_label": "Revise", "next_node_id": "department_manager" },
            { "action": "approve", "action_label": "Approve", "next_node_id": "end_process" },
            { "action": "approve_high_budget_with_high_credit_risk)", "action_label": "approve\n(high budget with high credit risk)", "next_node_id": "ceo" }
        ]
    },
    {
        "node_id" : "ceo",
        "node_label" : "ประธานกรรมการบริหาร",
        "actions": [
            { "action": "revise", "action_label": "Revise", "next_node_id": "management_director" },
            { "action": "approve", "action_label": "Approve", "next_node_id": "end_process" }
        ]
    },
    {
        "node_id" : "end_process",
        "node_label" : "จบกระบวนการ"
    },
]

sample_steps = [
    {"node_id": "drafter", "action": "submit", "resolved_node_id": "supervisor"},
    {"node_id": "supervisor", "action": "approve", "resolved_node_id": "department_manager"},
    {"node_id": "department_manager", "action": "revise", "resolved_node_id": "supervisor"},
    {"node_id": "supervisor", "action": "approve", "resolved_node_id": "department_manager"},
    {"node_id": "department_manager", "action": "approve", "resolved_node_id": "management_director"},
    {"node_id": "management_director", "action": "approve", "resolved_node_id": "end_process"},
]

output_file = "output/workflow"

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

def plain_node_renderer(dot, node):
    dot.node(node["node_id"], node["node_label"])

def plain_edge_renderer(dot, node, action):
    dot.edge(node["node_id"], action["next_node_id"], label=action["action_label"])

def plain_graph_renderer(dot):
    dot.render(f"{output_file}", format="png")

# render_entire_graph(workflow, plain_node_renderer, plain_edge_renderer, plain_graph_renderer)

def render_animated_steps(workflow, steps):
    passing_step = []
    current_step = None
    step_cnt = None

    def stepping_node_renderer(dot, node):
        attrs = {}
        # Node ปัจจุบันเป็นสีฟ้า
        if node["node_id"] == current_step["resolved_node_id"]:
            attrs = {
                "color": "blue",
                "fontcolor": "blue",
            }
        else:
            for ps in passing_step:
                # Node ที่เคยผ่านมาแล้ว ให้เป็นสีเทา
                if node["node_id"] == ps["node_id"]:
                    attrs = {
                        "color": "grey",
                        "fontcolor": "grey",
                    }
                    break
        dot.node(node["node_id"], node["node_label"], **attrs)

    def stepping_edge_renderer(dot, node, action):
        attrs = {}
        # เส้นทางสุดท้ายที่จะมาถึง Node ปัจจุบัน ให้เป็นสีแดง
        if  node["node_id"] ==           current_step["node_id"] and \
            action["action"].startswith( current_step["action"]) and \
            action["next_node_id"] ==    current_step["resolved_node_id"]:
                attrs = {
                    "color": "red",
                    "fontcolor": "red",
                }
        else:
            for ps in passing_step:
                # เส้นทางที่เคยผ่านมาแล้ว ให้เป็นสีเทา
                if  node["node_id"] ==           ps["node_id"] and \
                    action["action"].startswith( ps["action"]) and \
                    action["next_node_id"] ==    ps["resolved_node_id"]:
                    attrs = {
                        "color": "grey",
                        "fontcolor": "grey",
                    }
                    break
        dot.edge(node["node_id"], action["next_node_id"], label=action["action_label"], **attrs)

    def stepping_graph_renderer(dot):
        dot.render(f"{output_file}{step_cnt}", format="png")

    for i, s in enumerate(steps):
        passing_step.append(s)
        current_step = s
        step_cnt = i
        render_entire_graph(workflow, stepping_node_renderer, stepping_edge_renderer, stepping_graph_renderer)
    # สร้างไฟล์ gif
    fp_in = f"{output_file}*.png"
    fp_out = f"{output_file}.gif"

    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
            save_all=True, duration=1500, loop=1)

render_animated_steps(workflow, sample_steps)

# %%
