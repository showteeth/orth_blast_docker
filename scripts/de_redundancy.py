#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-18 11:30:35
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
import re
from collections import defaultdict

def judge_last_line(in_file,line_num):
	with open(in_file,'r') as judge_file:
		pre_total_lines=judge_file.readlines()
		total_lines=[i.strip() for i in pre_total_lines]
		total_line_num=len(total_lines)
		if line_num==total_line_num:
			tag=1
		else:
			tag=0
	return tag

def get_ids_length(in_file):
	with open(in_file,'r') as fasta:
		test_fasta_line=fasta.readline().strip()
		id_list=[]
		id_dic=defaultdict(list)
		final_dic=defaultdict(list)
		id_str=pre_id=now_id=''
		line_num=1
		id_title=[]
		pattern=re.compile('^>(.*?)\.')
		while test_fasta_line:
			tag=judge_last_line(in_file,line_num)
			if test_fasta_line[0]==">":
				id_title.append(re.search(pattern,test_fasta_line).group(1))
				now_id=test_fasta_line
				if id_str:
					id_length=len(id_str)
					id_dic[pre_id].append(id_str)
					id_dic[pre_id].append(id_length)
				id_str=''
			elif tag:
				pre_id=now_id
				id_str+=test_fasta_line
				id_length=len(id_str)
				id_dic[pre_id].append(id_str)
				id_dic[pre_id].append(id_length)
			else:
				id_str+=test_fasta_line
				pre_id=now_id
			test_fasta_line=fasta.readline().strip()
			line_num+=1
	return id_dic,list(set(id_title))

def get_max_seq(id_dic,id_title):
    maxlength_dic={}
    max_li=[]
    result_dic={}
    for i in id_title:
        max_li=[]
        maxlength=0
        max_key=maxseq=''
        for key,value in id_dic.items():
            if i in key and value[1]>maxlength:
                max_key=key
                maxlength=value[1]
                maxseq=value[0]
        max_li.append(max_key);max_li.append(maxlength);max_li.append(maxseq)
        maxlength_dic[i]=max_li
        result_dic[max_key]=maxseq
    return result_dic

def write_wrapped(string, every=60):
	return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

def write_dic_file(dic,out_file):
	with open(out_file,'w') as out:
		for k,v in dic.items():
			out.write(k+'\n')
			out_s=write_wrapped(v, every=60)
			out.write(out_s)
			out.write('\n')


def main():
	fasta_file=sys.argv[1]
	out_file=sys.argv[2]
	id_dic,id_title=get_ids_length(fasta_file)
	result_dic=get_max_seq(id_dic,id_title)
	write_dic_file(result_dic,out_file)

if __name__ == '__main__':
	main()