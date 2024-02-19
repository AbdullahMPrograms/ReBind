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
        for layer, modifiers in layers.items():
            for modifier, keys in modifiers.items():
                for key, key_info in keys.items():
                    if isinstance(key_info, dict):
                        remapped_key = key_info.get("key")
                        if program == "global":
                            ahk_core += f'{key}::{remapped_key}\n'
                        elif modifier:
                            ahk_core += f'{modifier} & {key}::{remapped_key}\n'
                        else:
                            ahk_core += f'{key}::Sendkey({remapped_key})\n'
                    else:
                        if program == "global":
                            ahk_core += f'{key}::{key_info}\n'
                        elif modifier:
                            ahk_core += f'{modifier} & {key}::{key_info}\n'
                        else:
                            ahk_core += f'{key}::Sendkey({key_info})\n'

    return ahk_core

print(generate_ahk_core())