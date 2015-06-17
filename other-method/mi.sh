# !/bin/bash

EXE="./mi.py"
SAM_PATH="../sampling-data"
RES_PATH="../result/mi"

for((i=0;i<100;++i))
do
	echo $i-th run
	$EXE $SAM_PATH/mRNA_filtered_random$i.txt $RES_PATH/mRNA_filtered_random$i.txt
	$EXE $SAM_PATH/CNA_filtered_random$i.txt $RES_PATH/CNA_filtered_random$i.txt discrete
	$EXE $SAM_PATH/METH_filtered_random$i.txt $RES_PATH/METH_filtered_random$i.txt
done
