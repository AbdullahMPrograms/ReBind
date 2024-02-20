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
        ahk_core += f'\nProgram: {program}\n'
        for layer, modifiers in layers.items():
            for modifier, keys in modifiers.items():
                if isinstance(keys, dict) and "key" in keys:  # We're at the key level without a modifier
                    remapped_key = keys.get("key")
                    ahk_core += f'{modifier}::{remapped_key}\n'
                else:  # We're at the modifier level or key level with a modifier
                    for key, key_info in keys.items():
                        if isinstance(key_info, dict) and "key" in key_info:
                            remapped_key = key_info.get("key")
                            ahk_core += f'{modifier} & {key}::{remapped_key}\n'

    return ahk_core

print(generate_ahk_core())