#!/bin/bash

home_folder=`pwd`
scripts_folder=${home_folder}/scripts
protein_data_folder=${home_folder}/protein_data
de_protein_data_folder=${home_folder}/de_protein_data
mkdir -p ${de_protein_data_folder}

if [ -f "$scripts_folder/de_pid.txt" ];then
	rm $scripts_folder/de_pid.txt
fi

for i in "arabidopsis" "rice"
do
	nohup python ${scripts_folder}/de_redundancy.py ${protein_data_folder}/${i}.fasta ${de_protein_data_folder}/${i}_de.fasta >\
		 ${scripts_folder}/${i}.log 2>&1 &
	echo $! >>$scripts_folder/de_pid.txt
done

if [ -f "$scripts_folder/de_job_status" ];then
	rm $scripts_folder/de_job_status
fi

while read read
do
	wait $read
	if [ $? -eq 0 ];then
		echo "$read executed success!" >>$scripts_folder/de_job_status
	else
		echo "$read executed fail!" >>$scripts_folder/de_job_status
		exit 1
	fi
done < $scripts_folder/de_pid.txt

for i in "arabidopsis" "rice"
do
	db_folder=${home_folder}/${i}_db
	mkdir -p ${db_folder}
	makeblastdb -in ${de_protein_data_folder}/${i}_de.fasta -dbtype prot -parse_seqids -out ${db_folder}/${i}_de_db
done

result_folder=${home_folder}/results_add_hsp_evalue4
mkdir -p ${result_folder}

blastp -query ${de_protein_data_folder}/arabidopsis_de.fasta -db ${home_folder}/rice_db/rice_de_db -evalue 1e-4 -outfmt 6 \
		-max_target_seqs 1 -max_hsps 1 -out ${result_folder}/arabidopsis_de_blastp -num_threads 16

blastp -query ${de_protein_data_folder}/rice_de.fasta -db ${home_folder}/arabidopsis_db/arabidopsis_de_db -evalue 1e-4 -outfmt 6 \
		-max_target_seqs 1 -max_hsps 1 -out ${result_folder}/rice_de_blastp -num_threads 16

python ${scripts_folder}/extract_pair.py -p "/orth/results_add_hsp_evalue4" -i "arabidopsis_de_blastp" "rice_de_blastp" -o "gene_pairs"

