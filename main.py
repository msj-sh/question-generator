#! /usr/bin/python3

import re
import csv
import time

# 读取原始文件
def readfile(filename = 'q.csv'):
    global header_lines
    c = csv.reader(open(filename, 'r'))
    origin_questions = []
    for i in c:
        origin_questions.append(i)
    # 去除表头
    return origin_questions[header_lines:]

# 文字清洗
def xtrim(data):
    # 去除头尾空白符
    for i in range(0, 7):
        data[i] = data[i].strip()
    print(data)
    return data

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
    global split_mark
    id = item[0]
    question = item[1]
    key = item[2]
    pattern = border_left + "[\s\S]*" + border_right
    # 对3-7列内容进行处理
    for i in range(2,7):
        # 减少题量
        #if (i == 3 or i ==4 or i == 5):
        #    continue
        # 防止 \S 转义
        repl = item[i].replace("\\", "\\\\")
        d = id + split_mark + re.sub(pattern, repl, question) + split_mark + is_key(item[i], key)
        q_tof.append(d)

# 单选题生成器
def generate_choice(item):
    global border_left
    global border_right
    global q_choice
    global split_mark
    id = item[0]
    question = item[1]
    key = item[2]
    # 345
    d = id + split_mark + question + split_mark + key + split_mark + item[3] + split_mark + item[4] + split_mark + item[5]
    q_choice.append(d)
    # 346
    d = id + split_mark + question + split_mark + key + split_mark + item[3] + split_mark + item[4] + split_mark + item[6]
    q_choice.append(d)
    # 356
    d = id + split_mark + question + split_mark + key + split_mark + item[3] + split_mark + item[5] + split_mark + item[6]
    q_choice.append(d)
    # 456
    d = id + split_mark + question + split_mark + key + split_mark + item[4] + split_mark + item[5] + split_mark + item[6]
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
            t = q_tof[i]
            # 删除选择题中的特定词
            t = t.replace("下列", "")
            t = t.replace("以下", "")
            q_tof[i] = t + "\n"
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
    origin_questions = []

    # 分隔符
    global split_mark
    split_mark = ","

    # 填空符
    global border_left
    global border_right
    border_left = "（"
    border_right = "）"

    # 表头信息
    global header_choice
    global header_lines
    global header_tof
    header_choice = "识别号"+split_mark+"题面"+split_mark+"选项1（答案）"+split_mark+"选项2"+split_mark+"选项3"+split_mark+"选项4"
    header_lines = 1
    header_tof = "识别号" +split_mark+ "题面" +split_mark+ "答案"

    # 题目存储
    global q_choice
    global q_tof
    q_choice = []
    q_tof = []

    # 读取原始文件
    print("任务开始，正在读取文件", end="\r")
    origin_questions = readfile()
    # 计数
    for i in range(0, len(origin_questions)):
        print("正在处理：", str((i + 1)), "/", str(len(origin_questions)), end="\r")
        item = xtrim(origin_questions[i])
        generate_tof_questions(item)
        generate_choice(item)
    write2file()
    print("本次任务共导入：" + str(len(origin_questions)) + "题")
    print("本次任务共生成选择题：" + str(len(q_choice)) + "题")
    print("本次任务共生成单选题：" + str(len(q_tof)) + "题")

