#! /usr/bin/python3

# 此程序模板与原始程序不同，此程序用于生成人社模板且只能生成2+2模式
# 执行转换前预先将英文逗号转换成中文逗号

# import re
import regex as re
import csv
import time
import random

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
    # print(data)
    return data

# 试题生成
def generate_questions(item):
    # print(item)
    global border_left
    global border_right
    global split_mark
    global mark
    global result
    global tof_buff
    # 序号/试题代码
    id = item[1]
    id_name = item[2]
    pattern = border_left + "[\s\S]*" + border_right
    question = item[3]
    key = item[4]
    if not (mark == id):
        # 创建新知识点
        l = id + split_mark + id_name + split_mark + "1"
        result.append(l)
        mark = id
        # 创建单选题
        l = split_mark + "单选题" + split_mark
        result.append(l)
    choices = [item[4], item[5], item[6], item[7]]
    random.shuffle(choices)
    _i = 0
    _key = "N"
    for i in choices:
        if not i == key: 
            _i += 1
        else:
            l = ["（A）", "（B）", "（C）", "（D）"]
            _key = l[_i]
            break
    # choice_question = re.sub(pattern, _key, question)
    choice_question = question.replace("（）", _key)
    result.append(split_mark + choice_question + split_mark + "1")
    # 选项
    l = "（A）" + choices[0] + "（B）" + choices[1] + "（C）" + choices[2] + "（D）" + choices[3]
    result.append(split_mark + l + split_mark)

    # 判断题并加入缓存
    l = item[random.randint(4, 7)]
    # tof_question = re.sub(pattern, l, question)
    tof_question = question.replace("（）", l)
    if l == key:
        tof = "（√）"
    else:
        tof = "（×）"
    tof_buff.append(split_mark + tof_question + tof + split_mark + "1")

    if (len(tof_buff) == 2):
        # 创建判断题
        l = split_mark + "判断题" + split_mark
        result.append(l)
        for i in tof_buff:
            result.append(i)
        # 清空缓存
        tof_buff = []


def write2file():
    global header_choice
    global result
    # 写出选择题
    with open('questions.csv', 'w') as fp:
        if not fp.writable():
            print("!! Failed to write choice questions to a file")
        # 每行加回车
        for i in range(0, len(result)):
            result[i] = result[i] + "\n"
        fp.writelines(header_choice + "\n")
        fp.writelines(result)


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
    header_choice = "试题代码" + split_mark + "试题" + split_mark + "分数"
    header_lines = 1

    # 进度存储
    global mark
    mark = "0"
    # 题目存储
    global result
    result = []
    # 存储判断题的缓冲区
    global tof_buff
    tof_buff = []
 
    # 读取原始文件
    print("任务开始，正在读取文件", end="\r")
    origin_questions = readfile()
    # 计数
    for i in range(0, len(origin_questions)):
        print("正在处理：", str((i + 1)), "/", str(len(origin_questions)), end="\r")
        item = xtrim(origin_questions[i])
        generate_questions(item)
    write2file() 
    # print("本次任务共导入：" + str(len(origin_questions)) + "题")
    # print("本次任务共生成选择题：" + str(len(q_choice)) + "题")
    # print("本次任务共生成单选题：" + str(len(q_tof)) + "题")

