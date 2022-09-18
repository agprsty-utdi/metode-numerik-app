#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

def safe_int(data, default=0)->int:
    '''safely cast variable value to integer'''
    try:
        data = int(data)
    except (ValueError, TypeError):
        data = default

    return data

def safe_float(data, default=0)->float:
    '''safely cast variable value to float with 9 digits after comma'''
    try:
        to_float = float(data)
        data = round(to_float, 9)
    except (ValueError, TypeError):
        data = default

    return data

def generate_random_string(size)->str:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return '' . join(random.choice(chars) for x in range(size))
