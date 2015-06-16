# !/bin/bash

EXE="../MINA/bin/MINA"
SAM_PATH="sampling-data"
RES_PATH="result"

for((i=0;i<100;++i))
do
    CMD="$EXE -ip ${SAM_PATH}/mRNA_filtered_random$i.txt";
   	CMD+=" -ip ${SAM_PATH}/CNA_filtered_random$i.txt"
   	CMD+=" -ip ${SAM_PATH}/METH_filtered_random$i.txt"
   	CMD+=" -o ${RES_PATH}/"
	CMD+=" dist"
   	CMD+=" -s ${SAM_PATH}/target_gene.txt"
   	CMD+=" -io ${SAM_PATH}/clinical$i.txt"
	CMD+=" -dhi 0.3"
	echo $CMD
	$CMD;
done
