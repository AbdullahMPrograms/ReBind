from ahkunwrapped import *
import json

def get_remap_keys():
    try:
        with open('Python/data/remap_keys.json', 'r') as file:
            remap_keys = json.load(file)
    except FileNotFoundError:
        remap_keys = {"original_keys": {}, "remapped_keys": {"global": {}}}
    return remap_keys

def generate_ahk_core():
    # Load the existing JSON file
    remap_keys = get_remap_keys()

    ahk_core = ""
    for program, layers in remap_keys["remapped_keys"].items():
        focus_yes = ""
        focus_no = ""
        for layer, modifiers in layers.items():
            for modifier, keys in modifiers.items():
                if isinstance(keys, dict) and "key" in keys:
                    remapped_key = keys.get("key")
                    focus_modifier = keys.get("focus_modifier", "No")
                    if focus_modifier == "Yes":
                        focus_yes += f'{modifier}::{remapped_key}\n'
                    else:
                        focus_no += f'{modifier}::{remapped_key}\n'
                else:
                    for key, key_info in keys.items():
                        if isinstance(key_info, dict) and "key" in key_info:
                            remapped_key = key_info.get("key")
                            focus_modifier = key_info.get("focus_modifier", "No")
                            if focus_modifier == "Yes":
                                focus_yes += f'{modifier} & {key}::{remapped_key}\n'
                            else:
                                focus_no += f'{modifier} & {key}::{remapped_key}\n'
        if focus_no:
            ahk_core += f'\nProgram: {program} (Focus: No)\n' + focus_no
        if focus_yes:
            ahk_core += f'\nProgram: {program} (Focus: Yes)\n' + focus_yes

    return ahk_core

print(generate_ahk_core())