#!/usr/bin python
# coding=utf-8
""" 
Created on 2017-07-06 @author: yangyuji
得到网站的动物名称
"""

import os
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import csv
import Queue

chromedriver = "/Users/yangyuji/shell/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

wait = ui.WebDriverWait(driver, 1)


# Get the infobox
# file_out = open('animal.txt', 'w')


def config_code():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')


def load_queue(words_file):
    q = Queue.Queue()
    csvfile = file(words_file, 'r')
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        q.put(row[0])
    csvfile.close()
    return q


def load_vacabular(vocabulary_file):
    vacabular = set("")
    csv_reader = open(vocabulary_file, 'r')
    for line in csv_reader:
        vacabular.add(line.replace("\n", ""))
    csv_reader.close()
    return vacabular


def one_layer_search(q, vacabular, output_file):
    url_base = "http://dict.cn/"
    file_out = open(output_file,'a')
    try:
        while not q.empty():
            word_data = q.get()
            print word_data
            if word_data in vacabular:
                print "词库中已存在：" + word_data
            else:
                # try:
                print "正在查询:" + word_data  # +" "+str(row_number)
                # 将这个单词存到词汇表中
                vacabular.add(word_data)
                # 将词汇表更新

                # 开始去网页上寻找单词相关的信息
                url_string = url_base + word_data
                driver.get(url_string)
                elem_value = driver.find_elements_by_xpath("//div[@class='shape']/span/a")
                file_out.write(word_data)

                # elem_value = driver.find_elements_by_xpath("//div[@class='hd_if']/a")

                for value in elem_value:
                    print value.text
                    file_out.write("\t"+value.text)
                file_out.write("\n")

    except:
        file_except = open("error_words.txt", 'a')
        file_except.write(word_data + "\n")
        file_except.close()
    file_out.close()


def main():
    words_file = "/Users/yangyuji/Documents/Coding/PycharmProjects/Friends_IELTS_Match/IELTS_LEARNING_WORDS.txt"

    exist_words_file = "/Users/yangyuji/Documents/Coding/PycharmProjects/Friends_IELTS_Match/EXISTING_WORDS.txt"
    output_file = "/Users/yangyuji/Documents/Coding/PycharmProjects/Friends_IELTS_Match/SCRAW_WORDS.txt"

    config_code()
    queue = load_queue(words_file)
    vacabular = load_vacabular(exist_words_file)

    one_layer_search(queue, vacabular, output_file)


if __name__ == '__main__':
    main()
