"""
Noise Plugin

This plugin replaces a percentage of text defined in NOISE_PERCENT to random ascii letters, digits, puctuation, and space characters

Usage:
    spikee generate --plugins noise

Parameters:
    text (str): The input text to be transformed.

Returns:
    str: The transformed text with noise.
"""

import random
import string 
import re
from typing import List

NOISE_PERCENT = 0.2

def transform(text: str, exclude_patterns: List[str] = None) -> str:
    chunks = []
    result_chunks = []
    modify_flags = []
    if exclude_patterns:
        compound = "(" + "|".join(exclude_patterns) + ")"
        chunks = re.split(compound, text)
        compound_re = re.compile(compound)

        for chunk in chunks:
            modify_flag = compound_re and compound_re.fullmatch(chunk)
            result_chunks += [ chr for chr in chunk ]
            modify_flags += [0 if modify_flag else 1] * len(chunk)
    else:
        result_chunks = list(text)
        modify_flags = [1] * len(result_chunks)

    one_indices = [i for i, val in enumerate(modify_flags) if val == 1]
    chars_to_typo = int(len(one_indices) * (1 - (1-NOISE_PERCENT)))
    indices_to_flip = random.sample(one_indices, chars_to_typo)

    for i in indices_to_flip:
        modify_flags[i] = 2

    replacement_chars = string.ascii_letters + string.digits + string.punctuation + ' '

    result = "".join([
        random.choice(replacement_chars) if val == 2 else char
        for val, char in zip(modify_flags, result_chunks)
    ])
    
    print(result)
    return result
