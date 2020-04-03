#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : keycode.py
# @Time    : 2020/4/2 17:48
# @Author  : Kelvin.Ye
from enum import unique, Enum


@unique
class KeyCode(Enum):
    home = 'home'
    back = 'back'
    left = 'left'
    right = 'right'
    up = 'up'
    down = 'down'
    center = 'center'
    menu = 'menu'
    search = 'search'
    enter = 'enter'
    delete = 'delete'
    recent = 'recent'  # Show all apps
    volume_up = 'volume_up'
    volume_down = 'volume_down'
    volume_mute = 'volume_mute'
    camera = 'camera'
    power = 'power'
    alt_left = '0x00000039'  # 57
    alt_right = '0x0000003a'  # 58
    caps_lock = '0x00000073'  # 115 Caps Lock key
    clear = '0x0000001c'  # 28 Clear key
    copy = '0x00000116'  # 278
    cut = '0x00000115'  # 277
    ctrl_left = '0x00000071'  # 113
    ctrl_right = '0x00000072'  # 114
    left_bracket = '0x00000047'  # 71 [
    page_up = '0x0000005c'  # 92
    page_down = '0x0000005d'  # 93
    plus = '0x00000051'  # 81 +
    pound = '0x00000012'  # 18 #
    at = '0x0000004d'  # 77 @
    comma = '0x00000037'  # 55 ,
    equals = '0x00000046'  # 70 =
    space = '0x0000003e'  # 62
    semicolon = '0x0000004a'  # 74 ;
    shift_left = '0x0000003b'  # 59
    shift_right = '0x0000003c'  # 60
    slash = '0x0000004c'  # 76 /
    STAR = '0x00000011'  # 17 *
    tab = '0x0000003d'  # 61

    key_0 = '0x00000007'  # 7
    key_1 = '0x00000008'  # 8
    key_2 = '0x00000009'  # 9
    key_3 = '0x0000000a'  # 10
    key_4 = '0x0000000b'  # 11
    key_5 = '0x0000000c'  # 11
    key_6 = '0x0000000d'  # 11
    key_7 = '0x0000000e'  # 11
    key_8 = '0x0000000f'  # 11
    key_9 = '0x00000010'  # 11

    key_a = '0x0000001d'  # 29
    key_b = '0x0000001e'  # 30
    key_c = '0x0000001f'  # 31
    key_d = '0x00000020'  # 32
    key_e = '0x00000021'  # 33
    key_f = '0x00000022'  # 34
    key_g = '0x00000023'  # 35
    key_h = '0x00000024'  # 36
    key_i = '0x00000025'  # 37
    key_j = '0x00000026'  # 38
    key_k = '0x00000027'  # 39
    key_l = '0x00000028'  # 40
    key_m = '0x00000029'  # 41
    key_n = '0x0000002a'  # 42
    key_o = '0x0000002b'  # 43
    key_p = '0x0000002c'  # 44
    key_q = '0x0000002d'  # 45
    key_r = '0x0000002e'  # 46
    key_s = '0x0000002f'  # 47
    key_t = '0x00000030'  # 48
    key_u = '0x00000031'  # 49
    key_v = '0x00000032'  # 50
    key_w = '0x00000033'  # 51
    key_x = '0x00000034'  # 52
    key_y = '0x00000035'  # 53
    key_z = '0x00000036'  # 54

    key_f1 = '0x00000083'  # 131
    key_f2 = '0x00000084'  # 132
    key_f3 = '0x00000085'  # 133
    key_f4 = '0x00000086'  # 134
    key_f5 = '0x00000087'  # 135
    key_f6 = '0x00000088'  # 136
    key_f7 = '0x00000089'  # 137
    key_f8 = '0x0000008a'  # 138
    key_f9 = '0x0000008b'  # 139
    key_f10 = '0x0000008c'  # 140
    key_f11 = '0x0000008d'  # 141
    key_f12 = '0x0000008e'  # 142
