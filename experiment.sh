# !/bin/bash

for((i=0;i<100;++i));
do
    ../../MINA/bin/MINA -ip mRNA_filtered_random$i.txt -ip CNA_filtered_random$i.txt -ip METH_filtered_random$i.txt -o output/$i/ dist -s target_gene.txt -io clinical$i.txt -dhi 0.3;
done