# วิธีการรัน

## สร้าง Python Environment

``` shell
> virtualenv env
```

## ติดตั้ง Python Package

``` shell
> pip install -f requirements.txt
```

## รันทดสอบได้สองวิธีคือ

- ใช้ Terminal
``` shell
> (env) py dot_render.py
```

- ใช้ vscode
เปิด vscode แล้วกดปุ่ม run บน Python Cell

# อธิบายเพิ่มเติม

ตัวแปร `workflow` คือข้อมูลของผังงาน
``` python
workflow = [
    {
        "node_id" : "drafter",
        "node_label" : "ผู้ร่างเอกสาร",
        "actions": [
            { "action": "submit", "action_label": "Submit", "next_node_id": "supervisor" },
            { "action": "cancel", "action_label": "Cancel", "next_node_id": "end_process" }
        ]
    },
    ...
]
```

และถ้าหากมีการดำเนินการตามขั้นตอน โดยงานจะไหลไปตาม Node ต่าง ๆ ซึ่ง เกิดจากการกระทำ (action) ของผู้อยู่ใน Node เราอาจเก็บประวัติเอาไว้ แบบนี้

``` python
sample_steps = [
    {"node_id": "drafter", "action": "submit", "resolved_node_id": "supervisor"},
    ...
]
```

เป้าหมายของเราในโปรเจคนี้คือเขียนชุดคำสั่งเพื่อ วาดกราฟออกมาเป็นภาพเคลื่อนไหว ตามการไหลของงานได้ ซึ่งก็คือ function ที่เขียนไว้ใต้ตัวแปร `sample_steps` นั่นเอง