from graphviz import Digraph
import glob
from PIL import Image
from util.RendererUtil import render_entire_graph

class AnimationUtil:
    passing_step = []
    current_step = None
    step_cnt = None
    output_file = None

    def __init__(self, output_file):
        self.output_file = output_file

    def stepping_node_renderer(self, dot, node):
        attrs = {}
        # Node ปัจจุบันเป็นสีฟ้า
        if node["node_id"] == self.current_step["resolved_node_id"]:
            attrs = {
                "color": "blue",
                "fontcolor": "blue",
            }
        else:
            for ps in self.passing_step:
                # Node ที่เคยผ่านมาแล้ว ให้เป็นสีเทา
                if node["node_id"] == ps["node_id"]:
                    attrs = {
                        "color": "grey",
                        "fontcolor": "grey",
                    }
                    break
        dot.node(node["node_id"], node["node_label"], **attrs)

    def stepping_edge_renderer(self, dot, node, action):
        attrs = {}
        # เส้นทางสุดท้ายที่จะมาถึง Node ปัจจุบัน ให้เป็นสีแดง
        if (
            node["node_id"] == self.current_step["node_id"]
            and action["action"].startswith(self.current_step["action"])
            and action["next_node_id"] == self.current_step["resolved_node_id"]
        ):
            attrs = {
                "color": "red",
                "fontcolor": "red",
            }
        else:
            for ps in self.passing_step:
                # เส้นทางที่เคยผ่านมาแล้ว ให้เป็นสีเทา
                if (
                    node["node_id"] == ps["node_id"]
                    and action["action"].startswith(ps["action"])
                    and action["next_node_id"] == ps["resolved_node_id"]
                ):
                    attrs = {
                        "color": "grey",
                        "fontcolor": "grey",
                    }
                    break
        dot.edge(
            node["node_id"],
            action["next_node_id"],
            label=action["action_label"],
            **attrs,
        )

    def stepping_graph_renderer(self, dot):
        dot.render(f"{self.output_file}{self.step_cnt}", format="png")

    def generate_gif(self):
        # สร้างไฟล์ gif
        fp_in = f"{self.output_file}*.png"
        fp_out = f"{self.output_file}.gif"

        img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
        img.save(
            fp=fp_out,
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=1500,
            loop=1,
        )

    def render_animated_steps(self, workflow, steps):
        for i, s in enumerate(steps):
            self.passing_step.append(s)
            self.current_step = s
            self.step_cnt = i
            render_entire_graph(
                workflow,
                self.stepping_node_renderer,
                self.stepping_edge_renderer,
                self.stepping_graph_renderer,
            )
        
        self.generate_gif()

        
