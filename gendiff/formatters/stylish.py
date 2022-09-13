from gendiff.consts import MARKS, TAB_SPACE, ADDED, DELETD
from gendiff.diff_tree import is_nested, is_updated


# Функция формирует отступ для вывода, согласно
# глубине вложенности и ключу изменения параметра
def spacer(indent, mark=''):
    res_str = TAB_SPACE * indent
    pos = len(res_str) - 2
    if mark not in MARKS:
        return res_str
    else:
        return res_str[:pos] + mark + res_str[pos + 1:]


def print_dict(d, deep=1):
    res = '{\n'
    for k, v in d.items():
        if isinstance(v, dict):
            res += TAB_SPACE * deep + k + ': ' + print_dict(v, deep + 1) + '\n'
        else:
            res += TAB_SPACE * deep + k + ': ' + str(v) + '\n'
    res += TAB_SPACE * (deep - 1) + '}'
    return res


def print_prop(prop, deep=1):
    if isinstance(prop, dict):
        return print_dict(prop, deep)
    return str(prop)


# Функция формирует строку вывода диффа в формате stylish
def stylish(diff, indent=0):
    res = '{\n'
    for key, val in diff.items():
        if is_nested(val):
            res += spacer(indent + 1)
            res += f'{key}: ' + stylish(val['prop'], indent + 1) + '\n'
        elif is_updated(val):
            old_val = val['prop'][0]
            new_val = val['prop'][1]
            res += spacer(indent + 1, DELETD)\
                + f'{key}: {print_prop(old_val, indent + 2)}\n'
            res += spacer(indent + 1, ADDED)\
                + f'{key}: {print_prop(new_val, indent + 2)}\n'
        else:
            new_val = val['prop']
            res += spacer(indent + 1, val['state'])\
                + f'{key}: {print_prop(new_val, indent + 2)}\n'
    res = res + spacer(indent) + '}'
    return res


def format(diff):
    return stylish(diff)
