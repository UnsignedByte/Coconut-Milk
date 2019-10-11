# @Author: Edmund Lam <edl>
# @Date:   15:30:46, 04-Nov-2018
# @Filename: fileutils.py
# @Last modified by:   edl
# @Last modified time: 00:01:08, 11-Oct-2019

import os
import pickle
from shutil import copyfile
import bot.handlers
import os

def load_data():
    if not os.path.exists("data/backup/"):
        os.makedirs("data/backup/")
    dat = {}
    if os.path.isfile('data/data.txt'):
        with open('data/data.txt', 'rb') as f:
            dat = pickle.load(f)
    else:
        with open('data/data.txt', 'wb') as f:
            pickle.dump(dat, f)
    copyfile('data/data.txt', 'data/data_backup.txt')
    return dat

def save_data():
    if os.path.isfile('data/data.txt'):
        copyfile('data/data.txt', 'data/data_backup.txt')
    with open('data/data.txt', 'wb') as f:
        pickle.dump(get_data(), f)

def nested_set(value, *keys):
    dic = get_data()
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def nested_pop(*keys):
    nested_get(*keys[:-1]).pop(keys[-1], None)


def alt_pop(key, *keys):
    nested_get(*keys).pop(key)

def nested_get(*keys, default={}}):
    print(keys)
    dic = get_data()
    for key in keys:
        print(type(key))
        dic=dic.setdefault( key, {} )
        print(dic)
    if not dic:
        dic=default
    return dic


def nested_append(value, *keys):
    v = nested_get(*keys)
    if v:
        v.append(value)
    else:
        nested_set([value], *keys)

def nested_extend(value, *keys):
    v = nested_get(*keys)
    if v:
        v.extend(value)
    else:
        nested_set([value], *keys)

def nested_addition(to_add, *keys, default=0):
    nested_set(nested_get(*keys, default=default)+to_add, *keys)

def nested_multiplication(to_mult, *keys, default=0):
    nested_set(nested_get(*keys, default=default)*to_mult, *keys)

def nested_remove(value, *keys, **kwargs):
    kwargs['func'] = kwargs.get('func', None)
    v = nested_get(*keys)
    if not v:
        return
    try:
        if not kwargs['func']:
            v.remove(value)
        else:
            for x in v:
                if kwargs['func'](x, value):
                    v.remove(x)
                    break
    except ValueError:
        return

def get_data():
    return bot.handlers.get_data()

def set_data(data):
    bot.handlers.set_data(data)
