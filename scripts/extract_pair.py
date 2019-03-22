#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-20 10:21:03
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


import os
import sys
import argparse

def trans_to_set(process_file):
	with open(process_file,'r') as process:
		process_line=process.readline().strip()
		final_li=[]
		while process_line:
			process_lst=process_line.split()
			if process_lst[0][0:2]=='AT':
				process_ele='|'.join(process_lst[0:2])
				final_li.append(process_ele)
			else:
				process_ele=process_lst[1] + '|' + process_lst[0]
				final_li.append(process_ele)
			process_line=process.readline().strip()

	return final_li

def get_list_sect(li_1,li_2):
	set_1=set(li_1)
	set_2=set(li_2)
	final_set=set.intersection(set_1,set_2)

	result_li=list(final_set)

	return result_li

def decode_result(li,out_file):
	with open(out_file,'w') as out:
		for i in li:
			str_1=i.split('|')[0]
			str_2=i.split('|')[1]
			out_line=str_1+'\t'+str_2+'\n'
			out.write(out_line)

def main():
	parser = argparse.ArgumentParser(description='extract gene pairs')

	parser.add_argument('--input_file','-i', type=str, nargs=2 ,help='input files--blastp results')
	parser.add_argument('--out_file','-o', type=str ,help='output files--gene pairs')
	parser.add_argument('--path','-p', type=str ,help='the working path')

	args = parser.parse_args()

	in_file_1=args.path+'/'+args.input_file[0]
	in_file_2=args.path+'/'+args.input_file[1]

	out_file=args.path+'/'+args.out_file

	li_1=trans_to_set(in_file_1)
	li_2=trans_to_set(in_file_2)

	result_li=get_list_sect(li_1,li_2)

	decode_result(result_li,out_file)

if __name__ == '__main__':
    main()



