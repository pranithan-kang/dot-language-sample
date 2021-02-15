from util.AnimationUtil import *
import pytest
import unittest.mock as utm
from unittest.mock import patch
import pytest_mock as ptm

@pytest.fixture(autouse=True)
def before_each():
    pytest.workflow = [
        {
            "node_id": "node_1",
            "node_label": "node_1",
            "actions": [
                {"action": "go", "action_label": "go", "next_node_id": "node_2"},
                {"action": "cancel", "action_label": "cancel",
                    "next_node_id": "end_process"}
            ]
        },
        {
            "node_id": "node_2",
            "node_label": "node_2",
            "actions": [
                {"action": "revise", "action_label": "revise",
                    "next_node_id": "node_1"},
                {"action": "go", "action_label": "go", "next_node_id": "node_3"},
                {"action": "cancel", "action_label": "cancel",
                    "next_node_id": "end_process"}
            ]
        },
        {
            "node_id": "node_3",
            "node_label": "node_3",
            "actions": [
                {"action": "revise", "action_label": "revise",
                    "next_node_id": "node_2"},
                {"action": "go", "action_label": "go",
                    "next_node_id": "end_process"},
                {"action": "cancel", "action_label": "cancel",
                    "next_node_id": "end_process"}
            ]
        },
        {
            "node_id": "end_process",
            "node_label": "end_process"
        }
    ]

    pytest.steps = [
        {"node_id": "node_1", "action": "go", "resolved_node_id": "node_2"},
        {"node_id": "node_2", "action": "go", "resolved_node_id": "node_3"},
    ]

    pytest.animation_util = AnimationUtil(None)


def test_stepping_node_renderer():
    animation_util: AnimationUtil = pytest.animation_util

    animation_util.passing_step = [pytest.steps[0]]
    animation_util.current_step = pytest.steps[1]

    dot = Digraph("TestGraph")
    node = pytest.workflow[0]
    animation_util.stepping_node_renderer(dot, node)

    assert dot.source == 'digraph TestGraph {\n\tnode_1 [label=node_1 color=grey fontcolor=grey]\n}'

    dot = Digraph("TestGraph")
    node = pytest.workflow[1]
    animation_util.stepping_node_renderer(dot, node)

    assert dot.source == 'digraph TestGraph {\n\tnode_2 [label=node_2]\n}'

    dot = Digraph("TestGraph")
    node = pytest.workflow[2]
    animation_util.stepping_node_renderer(dot, node)

    assert dot.source == 'digraph TestGraph {\n\tnode_3 [label=node_3 color=blue fontcolor=blue]\n}'


def test_stepping_edge_renderer():
    animation_util = pytest.animation_util

    animation_util.passing_step = [pytest.steps[0]]
    animation_util.current_step = pytest.steps[1]

    dot = Digraph("TestGraph")
    node = pytest.workflow[0]
    animation_util.stepping_edge_renderer(dot, node, node["actions"][0])

    assert dot.source == 'digraph TestGraph {\n\tnode_1 -> node_2 [label=go color=grey fontcolor=grey]\n}'

    dot = Digraph("TestGraph")
    node = pytest.workflow[0]
    animation_util.stepping_edge_renderer(dot, node, node["actions"][1])

    assert dot.source == 'digraph TestGraph {\n\tnode_1 -> end_process [label=cancel]\n}'

    dot = Digraph("TestGraph")
    node = pytest.workflow[1]
    animation_util.stepping_edge_renderer(dot, node, node["actions"][0])

    assert dot.source == 'digraph TestGraph {\n\tnode_2 -> node_1 [label=revise]\n}'

    dot = Digraph("TestGraph")
    node = pytest.workflow[1]
    animation_util.stepping_edge_renderer(dot, node, node["actions"][1])

    assert dot.source == 'digraph TestGraph {\n\tnode_2 -> node_3 [label=go color=red fontcolor=red]\n}'

    dot = Digraph("TestGraph")
    node = pytest.workflow[2]
    animation_util.stepping_edge_renderer(dot, node, node["actions"][0])

    assert dot.source == 'digraph TestGraph {\n\tnode_3 -> node_2 [label=revise]\n}'

    dot = Digraph("TestGraph")
    node = pytest.workflow[2]
    animation_util.stepping_edge_renderer(dot, node, node["actions"][1])

    assert dot.source == 'digraph TestGraph {\n\tnode_3 -> end_process [label=go]\n}'

def test_render_entire_graph(mocker):
    animation_util: AnimationUtil = pytest.animation_util
    render_entire_graph = mocker.patch("util.AnimationUtil.render_entire_graph")
    generate_gif = mocker.patch("util.AnimationUtil.AnimationUtil.generate_gif")
    animation_util.render_animated_steps(pytest.workflow, pytest.steps)
    generate_gif.assert_called_once()
    assert 2 == render_entire_graph.call_count