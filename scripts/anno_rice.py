#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-26 22:53:15
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

########## purpose: ################
# anno rice with ara anno
# 
#
#

########## thoughts: ################
# 
# 
#
#

import re
import os
import sys
import argparse

# 去除转录本标记，就是.后面的数字
def remove_tag(args):
	with open(args.gene_pair_file,'r') as gene_pair,open(args.gene_pair_out,'w') as out:
		gene_pair_lst_pre=gene_pair.readlines()
		gene_pair_lst=[i.strip() for i in gene_pair_lst_pre]

		pat=re.compile('\.(\d*)')
		gene_pair_final=[re.sub(pat,'',j)+'\t'+j  for j in gene_pair_lst]

		out.write('\n'.join(gene_pair_final))
		out.write('\n')

# remove_tag(gene_pair_file,out_file)

def write_dic_file(dic,out_file):
	with open(out_file,'w') as out:
		for k,v in dic.items():
			out.write(k+'\t')
			out_s='\t'.join(v)
			out.write(out_s)
			out.write('\n')

def remove_anno_dup(args):
	with open(args.anno_dup_file,'r') as anno_dup:
		anno_dup_line=anno_dup.readline().strip()
		anno_dup_dic={}
		while anno_dup_line:
			# set filed sep \t
			anno_dup_list=anno_dup_line.split('\t')
			if anno_dup_list[0] in anno_dup_dic.keys():
				if anno_dup_dic[anno_dup_list[0]][0] == 'NA':
					anno_dup_dic[anno_dup_list[0]]=anno_dup_list[1:]
			else:
				anno_dup_dic[anno_dup_list[0]]=anno_dup_list[1:]
			anno_dup_line=anno_dup.readline().strip()

		write_dic_file(anno_dup_dic,args.anno_dedup_file)

def construct_dic(in_file):
	with open(in_file,'r') as in_line:
		in_lines=in_line.readlines()
		pre_list=[i.strip().split() for i in in_lines]
		out_dic={}
		for i in pre_list:
			out_dic[i[0]]=i[1:]
	return out_dic

def merge_anno(args):
	# construct dict
	gene_pair_dic=construct_dic(args.gene_pair_out)
	anno_dic=construct_dic(args.anno_dedup_file)

	for k,v in gene_pair_dic.items():
		if k in anno_dic.keys():
			raw_lst=v
			raw_lst.extend(anno_dic[k])
			gene_pair_dic[k]=raw_lst

	write_dic_file(gene_pair_dic,args.out_file)


# def set_work_path(args):
# 	os.chdir(os.path.dirname(args.path))


def main():
	parser = argparse.ArgumentParser(description='anno rice with ara anno')

	parser.add_argument('--gene_pair_file','-i', type=str ,help='input gene pair file')
	parser.add_argument('--gene_pair_out','-I', type=str, help='input gene pair file')


	parser.add_argument('--anno_dup_file','-d', type=str ,help='anno dup file')  
	parser.add_argument('--anno_dedup_file','-D', type=str ,help='anno uniq file')

	parser.add_argument('--out_file','-o', type=str ,help='output files--gene pairs')
	parser.add_argument('--path','-p', type=str ,help='the working path',default='./')

	args = parser.parse_args()

	# set_work_path(args)

	# remove tags in gene_pair
	remove_tag(args)

	# remove anno dup
	remove_anno_dup(args)

	# out merge ano
	merge_anno(args)

if __name__ == '__main__':
    main()
