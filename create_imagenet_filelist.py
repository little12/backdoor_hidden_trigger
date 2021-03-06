'''
This scripts partitions the ImageNet train and val data into poison_generation, finetune and val data
to run our backdoor attacks. It creates file lists.

Author: Aniruddha Saha
Date: 02/02/2020
'''


import configparser
import glob
import os
import sys
import random
import pdb
#import tqdm

random.seed(10)
config = configparser.ConfigParser()
config.read(sys.argv[1])# 读取配置文件dataset.cfg

#得到字典options：data_dir=dataset/imagenet_nfs1，poison_generation=200，finetune=800，test=50
options = {}
for key, value in config['dataset'].items():
	key, value = key.strip(), value.strip() #strip()去掉空格
	options[key] = value

#creat dir
if not os.path.exists("ImageNet_data_list/poison_generation"):
	os.makedirs("ImageNet_data_list/poison_generation")
if not os.path.exists("ImageNet_data_list/finetune"):
	os.makedirs("ImageNet_data_list/finetune")
if not os.path.exists("ImageNet_data_list/test"):
	os.makedirs("ImageNet_data_list/test")

#DATA_DIR=dataset/imagenet_nfs1
DATA_DIR = options["data_dir"]

dir_list = sorted(glob.glob(DATA_DIR + "/train/*")) #对train下的所有文件排序
# max_list = 0
# min_list = 1300

for i, dir_name in enumerate(dir_list):
	if i%50==0:
		print(i)
	filelist = sorted(glob.glob(dir_name + "/*")) #glob.glob()匹配所有的符合条件的文件，并将其以list的形式返回
	random.shuffle(filelist)

	# max_list = max(max_list, len(filelist))
	# min_list = min(min_list, len(filelist))
	with open("ImageNet_data_list/poison_generation/" + os.path.basename(dir_name) + ".txt", "w") as f:
		for ctr in range(int(options["poison_generation"])):
			f.write(filelist[ctr].split("/")[-2] + "/" + filelist[ctr].split("/")[-1] + "\n")
	with open("ImageNet_data_list/finetune/" + os.path.basename(dir_name) + ".txt", "w") as f:
		for ctr in range(int(options["poison_generation"]), len(filelist)):
			f.write(filelist[ctr].split("/")[-2] + "/" + filelist[ctr].split("/")[-1] + "\n")

dir_list = sorted(glob.glob(DATA_DIR + "/val/*"))

for i, dir_name in enumerate(dir_list):
	if i%50==0:
		print(i)
	filelist = sorted(glob.glob(dir_name + "/*"))
	with open("ImageNet_data_list/test/" + os.path.basename(dir_name) + ".txt", "w") as f:
		for ctr in range(int(options["test"])):
			f.write(filelist[ctr].split("/")[-2] + "/" + filelist[ctr].split("/")[-1] + "\n")


# print(max_list, min_list)
