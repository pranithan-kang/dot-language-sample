from util.AnimationUtil import AnimationUtil

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

AnimationUtil(output_file).render_animated_steps(workflow, sample_steps)
