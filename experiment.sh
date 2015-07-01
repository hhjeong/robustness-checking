# !/bin/bash

EXE="../../MINA/bin/MINA"
SAM_PATH="sampling-data"
RES_PATH="result"

for((i=10;i<100;i+=10))
do
    for((j=0;j<100;++j))
    do
	CMD="$EXE -ip ${SAM_PATH}/$i/RandomDataSet${j}_mRNA.txt";
   	CMD+=" -ip ${SAM_PATH}/$i/RandomDataSet${j}_CNA.txt"
   	CMD+=" -ip ${SAM_PATH}/$i/RandomDataSet${j}_METH.txt"
   	CMD+=" -o ${RES_PATH}/mina/$i/"
	CMD+=" dist"
   	CMD+=" -s ${SAM_PATH}/target_gene.txt"
   	CMD+=" -io ${SAM_PATH}/$i/RandomDataSet${j}_clinical.txt"
	CMD+=" -dhi 0.3"
	echo $CMD
	$CMD;
    done
done
