#!/usr/bin/python3

from dataclasses import dataclass, field

@dataclass
class FormField:
    offset: int
    name: str
    default: int | None = None
    values: dict[int, str] = field(default_factory=dict)
    data_type: str = "int32"
    elem: str | None = None

SHORTCUTS = {
    0x73: "None",
    0x2A: "Backspace",
    0x39: "Caps Lock",
    0x2B: "Tab",
    0x46: "Print Screen",
    0x47: "Scroll Lock",
    0x53: "Num Lock",
    }

STATUS_ = [
    FormField(78, "Running FW version", None, {}, "uint16", elem="uint16"),
    FormField(79, "Running FW checksum", None, {}, "uint32", elem="hex_info"),
]

CONFIG_ = [
    FormField(1001, "Mouse", elem="label"),
    FormField(71, "Force Mouse Boot Mode", None, {}, "uint8", "checkbox"),

    FormField(1002, "Keyboard", elem="label"),
    FormField(72, "Force KBD Boot Protocol", None, {}, "uint8", "checkbox"),
    FormField(73, "KBD LED as Indicator", None, {}, "uint8", "checkbox"),

    FormField(76, "Enforce Ports", None, {}, "uint8", "checkbox"),
]

OUTPUT_ = [
    FormField(6, "Operating System", 1, {1: "Linux", 2: "MacOS", 3: "Windows", 4: "Android", 255: "Other"}, "uint8"),
    FormField(8, "Cursor Park Position", 0, {0: "Top", 1: "Bottom", 3: "Previous"}, "uint8"),
    FormField(1003, "Screensaver", elem="label"),
    FormField(9, "Mode", 0, {0: "Disabled", 1: "Pong", 2: "Jitter"}, "uint8"),
    FormField(10, "Only If Inactive", None, {}, "uint8", "checkbox"),
    FormField(11, "Idle Time (μs)", None, {}, "uint64"),
    FormField(12, "Max Time (μs)", None, {}, "uint64"),
]

def generate_output(base, data):
    output = [
        {
            "name": field.name,
            "key": base + field.offset,
            "default": field.default,
            "values": field.values,
            "type": field.data_type,
            "elem": field.elem,
        }
        for field in data
    ]
    return output

def output_A(base=10):
    return generate_output(base, data=OUTPUT_)

def output_B(base=40):
    return generate_output(base, data=OUTPUT_)

def output_status():
    return generate_output(0, data=STATUS_)

def output_config():
    return generate_output(0, data=CONFIG_)
