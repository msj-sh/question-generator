#! /usr/bin/python3

import re

# 读取原始文件
def readfile(filename = 'q.csv'):
    global header_lines
    with open(filename, 'r') as fp:
        origin_questions = fp.readlines()

    # 去除表头
    return origin_questions[header_lines:]

# 切割字符串
def split(data, split_mark = ','):
    res = data.split(split_mark, -1)

    # 去除头尾空白符
    for i in range(0, 7):
        res[i] = res[i].strip()
    # print(res)
    return res

def is_key(str, key):
    if str == key:
        return "T"
    else:
        return "F"

# 判断题生成器
def generate_tof_questions(item):
    global border_left
    global border_right
    global q_tof
    id = item[0]
    question = item[1]
    key = item[2]
    pattern = border_left + "[\s\S]*" + border_right
    for i in range(2,7):
        d = id + "," + re.sub(pattern, item[i], question) + "," + is_key(item[i], key)
        q_tof.append(d)

# 单选题生成器
def generate_choice(item):
    global border_left
    global border_right
    global q_choice
    id = item[0]
    question = item[1]
    key = item[2]
    pattern = border_left + "[\s\S]*" + border_right
    d = id + "," + question + "," + key + "," + item[3] + "," + item[4] + "," + item[5]
    q_choice.append(d)
    d = id + "," + question + "," + key + "," + item[3] + "," + item[4] + "," + item[6]
    q_choice.append(d)
    d = id + "," + question + "," + key + "," + item[3] + "," + item[5] + "," + item[6]
    q_choice.append(d)
    d = id + "," + question + "," + key + "," + item[4] + "," + item[5] + "," + item[6]
    q_choice.append(d)

def write2file():
    global q_choice
    global q_tof
    global header_choice
    global header_tof
    # 写出判断题
    with open('判断题.csv', 'w') as fp:
        if not fp.writable():
            print("!! Failed to write TOF questions to a file")
        # 每行加回车
        for i in range(0, len(q_tof)):
            q_tof[i] = q_tof[i] + "\n"
        fp.write(header_tof + "\n")
        fp.writelines(q_tof)
    # 写出选择题
    with open('选择题.csv', 'w') as fp:
        if not fp.writable():
            print("!! Failed to write choice questions to a file")
        # 每行加回车
        for i in range(0, len(q_choice)):
            q_choice[i] = q_choice[i] + "\n"
        fp.writelines(header_choice + "\n")
        fp.writelines(q_choice)


if __name__ == "__main__":
    # 全局变量声明

    # 原始数据存储
    global origin_questions

    # 分隔符
    global split_mark

    # 填空符
    global border_left
    global border_right

    # 表头信息
    global header_choice
    global header_lines
    global header_tof

    # 题目存储
    global q_choice
    global q_tof

    # 初始化变量
    origin_questions = []
    split_mark = ","
    border_left = "（"
    border_right = "）"
    header_lines = 1
    header_tof = "识别号,题面,答案"
    header_choice = "识别号,题面,选项1（答案）,选项2,选项3,选项4"
    q_choice = []
    q_tof = []

    # 读取原始文件
    origin_questions = readfile()
    for i in range(0, len(origin_questions)):
        item = split(origin_questions[i])
        generate_tof_questions(item)
        generate_choice(item)
    write2file()

