#!/usr/local/bin python
# coding:utf-8

# encoding=utf-8
# author:yangyuji
# github:yangyuji12
# date:20171017
# fuction:得到老友记中每一集中出现的雅思单词和他们的出现时刻

import sys
import re
import os
import os.path


#
def getPureWords():
    file_in = open("/Users/yangyuji/Documents/Coding/PycharmProjects/Friends_IELTS_Match/IELTS_WORDS.txt", 'r')
    file_out = open("/Users/yangyuji/Documents/Coding/PycharmProjects/Friends_IELTS_Match/IELTS_PURE_WORDS.txt", 'w')

    for line in file_in:
        components = line.replace("\n", "").split(" ")
        print components[0]
        file_out.write(components[0].replace("*", "") + "\n")
    # break
    # print(line)
    file_in.close()
    file_out.close()


def getMarks(FRIENDS_PATH, IELTS_WORDS_FILE, FRIENDS_NEW_PATH):
    if not os.path.exists(FRIENDS_NEW_PATH):
        os.makedirs(FRIENDS_NEW_PATH)

    file_in = open(IELTS_WORDS_FILE, 'r')
    words_list = []
    words_dict = {}
    for line in file_in:
        words_list.append(line.replace("\n", ""))
        words_dict[line.replace("\n", "")] = 0
    print len(words_list)

    pathDir = os.listdir(FRIENDS_PATH)
    for season in pathDir:
        new_season_dir = FRIENDS_NEW_PATH + os.path.sep + season
        if os.path.isdir(FRIENDS_PATH + season):  # 解决mac上.DS_Store（或其他隐藏文件）的异常
            if not os.path.exists(new_season_dir):
                os.makedirs(new_season_dir)
            print season

            for file in os.listdir(FRIENDS_PATH + season):
                new_episode_file = open(new_season_dir + os.path.sep + file, 'w')
                file_episode = open(FRIENDS_PATH + season + os.path.sep + file, 'r')
                # print file
                num_line = ""
                time_line = ""
                english_line = ""
                chinese_line = ""
                word_contained_list = []

                for line_episode in file_episode:
                    print len(line_episode)
                    # 空行的len是2；数字行的len大于等于3小于8；时间行中有:,英文字幕行中以a-z开头
                    if len(line_episode) >= 3 and len(line_episode) < 8 and re.search(r'^[0-9]', line_episode):
                        num_line = line_episode
                        print num_line
                    elif '00:' in line_episode:
                        time_line = line_episode
                        print time_line
                    elif re.search(r'^[a-zA-Z]', line_episode):
                        english_line = line_episode

                        english_words = re.compile(r'[,\n\r.?!:]').sub('', line_episode).split(" ")
                        print english_words
                        for word in words_list:

                            if word in english_words:
                                word_contained_list.append(word)
                                words_dict[word] = 1;

                    elif re.search(r'^[^0-9A-Za-z]', line_episode) and len(line_episode) > 2:
                        chinese_line = line_episode
                        print chinese_line
                    elif len(line_episode) == 2:
                        if len(word_contained_list) > 0:
                            new_episode_file.write(num_line)
                            new_episode_file.write(time_line)
                            new_episode_file.write(english_line)
                            new_episode_file.write("IELTS WORDS: ")
                            for word in word_contained_list:
                                new_episode_file.write(word + "\t")
                            new_episode_file.write("\n")
                            new_episode_file.write(chinese_line)
                            new_episode_file.write("\n")

                        num_line = ""
                        time_line = ""
                        english_line = ""
                        chinese_line = ""
                        word_contained_list = []
                new_episode_file.close()
                file_episode.close()

                # print file
                # break
    count = 0;
    for word in words_dict:
        if words_dict[word] == 0:
            count += 1
            print word
    print count


def main():
    FRIENDS_PATH = "/Users/yangyuji/Documents/Coding/PycharmProjects/Friends_IELTS_Match/House.of.Cards/"

    IELTS_WORDS_FILE = "/Users/yangyuji/Documents/Coding/PycharmProjects/Friends_IELTS_Match/IELTS_LEARNING_WORDS.txt"
    FRIENDS_NEW_PATH = "/Users/yangyuji/Documents/Coding/PycharmProjects/Friends_IELTS_Match/House.of.Cards_new/"
    getMarks(FRIENDS_PATH, IELTS_WORDS_FILE, FRIENDS_NEW_PATH)


if __name__ == '__main__':
    main()
