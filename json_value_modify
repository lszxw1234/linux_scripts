"""
This is tool is used for update json configurate file.
Example:
python json_value_modify.py a.b.c 999 example.json

This sample will update the key which is "a.b.c" and set it value to 999. 
"""
import os, sys
import json


def get_new_json(filepath, key, value):
    key_ = key.split(".")
    key_length = len(key_)
    with open(filepath, 'rb') as f:
        json_data = json.load(f)
        i = 0
        a = json_data
        while i < key_length:
            if i + 1 == key_length:
                if 1 == len(a):
                    dic = a[0]
                    dic[key_[i]] = value
                    a[0] = dic
                    break
            else:
                a = a[key_[i]]
                i = i + 1
    f.close()
    return json_data


def rewrite_json_file(filepath, json_data):
    with open(filepath, 'w') as f:
        json.dump(json_data, f)
    f.close()


if __name__ == '__main__':
    key = sys.argv[1]
    value = sys.argv[2]
    json_path = sys.argv[3]
    m_json_data = get_new_json(json_path, key, value)
    rewrite_json_file(json_path, m_json_data)
