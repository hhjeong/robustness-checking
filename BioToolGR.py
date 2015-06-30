# Made by Garam Factory

# This program is made for ease of data access on python environment.
# Users are recommended to run this program on ipython

import pandas as pd
import numpy as np
import random
from pandas import DataFrame

class BioToolGR:
    # This function parses a raw file from UC SANTA CRUZ("https://genome-cancer.ucsc.edu")
    # The format of files from UC SANTA CRUZ is usually text file
    # that numbers are separated by '\t' character.
    # Therefore, if you have a raw file not separted by '\t',
    # this function might not be useful.
    def parse(self,filename,header=None,index_col=None):
        return pd.read_csv(open(filename),sep='\t',index_col = index_col,header=header)
           
    # This function drops rows whose column name is parameter "name",
    # if the value of the column is NaN.
    def dropnabycolumn(self,data,name):
        return data[data[name].notnull()]


    # This function filters out gene data which is not in "target_gene"
    # Input *****
    # original : gene list - original data
    # target_gene : target gene list to filter out
    def build_target_kernel(self,kernel,original,target_gene):
        filtered_kernel = pd.DataFrame()
        
        k = 0
        for index,row in original.iterrows():
            if not row.values[0] == target_gene.loc[k].values[0]:
                continue

            filtered_kernel = filtered_kernel.append(kernel.loc[index])
            k += 1
            if k == len(target_gene):
                break
            
        return filtered_kernel
    
    def write_csv(self,dataframe,filename):
        dataframe.to_csv(filename,sep='\t')


    # This function extracts k number of rows randomly.
    # If "duplicated" is set, rows already in the list  will be added.
    def pick_random_columns(self,kernel,outcome,k,duplicated=True):
        num = 0
        bucket = []
        new_kernel = pd.DataFrame()
        new_outcome = pd.DataFrame(dtype=int)
        column_len = len(kernel)
        
        while num < k:
            r = random.randint(0,column_len-1)
            if not duplicated:
                if r in bucket:
                    continue
                bucket.append(r)
            new_kernel = new_kernel.append(kernel.iloc[:,r])
            new_outcome = new_outcome.append(outcome.iloc[r])
            num += 1
        
        return new_kernel,new_outcome

    # This function extracts rows whose value is "outcome_value"
    def pick_columns_outcome(self,kernel,outcome,outcome_value):
        num = 0
        new_kernel = pd.DataFrame()
        new_outcome = pd.DataFrame(dtype=int)
        column_len = len(kernel.columns)

        for i,v in kernel.transpose().iterrows():
            if outcome.loc[i][0] == outcome_value:
                new_kernel = new_kernel.append(v)
                new_outcome = new_outcome.append(outcome.loc[i])
        
        return new_kernel,new_outcome


    # This function builds dataset for the program 'Net-Cox' 
    # 'genomicMatrix' and 'clinical_data' files are required for this function call
    # Data, SampleName,and GeneName are extracted from the file 'genomicMatrix'
    # d, and Times are extracted from the file 'clinical_data'
    # Also, the rows whose deviation is 0 are removed
    def build_netcox_dataset(self,output):
        data = self.parse('genomicMatrix')
        SampleName = data.columns[1:]
        GeneName = data['sample']
        Data = data.drop('sample',1)

        data = self.parse('clinical_data')

        d = []
        Times = []
        s = SampleName
        for i in s:
            k = data[data['sampleID'] == i]
            if np.isnan(k['_OS_IND'].values[0]) or np.isnan(k['_TIME_TO_EVENT'].values[0]):
                Data = Data.drop(i,1)
                SampleName = SampleName.drop(i)
            else:
                d.append(k['_OS_IND'].values[0])
                Times.append((k['_TIME_TO_EVENT'].values[0])/30)

        Data = Data[Data.std(1) > 0.0]

        Times = DataFrame(Times,index=SampleName)
        d = DataFrame(d,index=SampleName)
        
        # Sorting GenemicMatrix in order of Times
        Data = Data.append(Times.T,ignore_index=True)
        Data = Data.append(d.T,ignore_index=True)
        Data = Data.T
        Data = Data.sort_index(by=[len(Data.columns) - 1])
        Data = Data.T

        d = Data[-1:]
        d = d.T
        
        Data = Data[0:-1]

        Times = Data[-1:]
        Times = Times.T

        Data = Data[0:-1]

        SampleName = Data.columns
 
        import scipy.io 
        scipy.io.savemat(output,mdict={'Data':np.array(Data), 'GeneName':np.array(GeneName),'SampleName':np.array(SampleName), 'Times': np.array(Times), 'd': np.array(d)})
        return [Data,GeneName,SampleName,Times,d]
    #------------------------------------------------------------------------------


    # This is the process of what I have done for the Hyun-Hwan's order.
    # 2015-1-27
    def HyunOrder1(self,data):
        t = self.parse('clinical_data','sampleID')
        self.dropnabycolumn(t,'_OS_IND')
        data = data[((data['_OS_IND'] == 0) & (data['_OS'] > 1080)) | (data['_OS_IND'] == 1)]

    # This is the process of what I have done for the Hyun-Hwan's order.
    # 2015 2-23
    # This is the process of what I have done for the Hyun-Hwan's order.
    # Dataset is the file genomicMatrix from UC SANTA CRUZ("https://genome-cancer.ucsc.edu")
    # The purpose of this function is to build the dataset for fitting in 'Net-Cox' Program
    # 'Net-Cox' is Matlab Program, which requires a .mat file containing
    # m*n genomic matrix in the name of 'Data',
    # m*1 matrix of gene names in the name of 'GeneName',
    # n*1 matrix of sample names in the name of 'SampleName',
    # n*1 matrix of survival times in the name of 'Times',
    # n*1 matrix of survival indicator in the name of 'd',
    # In the .mat file, all the given variables must be set to run the program.
    # Therefore, HyunOrder2 builds the appropriate file with the dataset from
    # UC SANTA CRUZ.
    # And run the Net-Cox Program with the file
    def HyunOrder2(self,output):
        self.build_nextcox_set(output)

    # 2015 6-17
    def HyunOrder4(self):
        METH = self.parse('original-data/METH.txt')
        CNA = self.parse('original-data/CNA.txt')
        mRNA = self.parse('original-data/mRNA.txt')
        sym = self.parse('original-data/sym.txt')
        target_gene = self.parse('original-data/target_gene.txt')
        
        METH_filtered = self.build_target_kernel(METH,sym,target_gene)
        CNA_filtered = self.build_target_kernel(CNA,sym,target_gene)
        mRNA_filtered = self.build_target_kernel(mRNA,sym,target_gene)

        METH_name = "sampling-data/METH_filtered"
        CNA_name = "sampling-data/CNA_filtered"
        mRNA_name = "sampling-data/mRNA_filtered"

        METH_filtered.to_csv(METH_name+'.txt',sep='\t',index=False,header=False)
        CNA_filtered = CNA_filtered.astype(int)
        CNA_filtered.to_csv(CNA_name+'.txt',sep='\t',index=False,header=False)
        mRNA_filtered.to_csv(mRNA_name+'.txt',sep='\t',index=False,header=False)
        
    # 2015 6-8
    def HyunOrder3(self):
        METH = self.parse('METH.txt')
        CNA = self.parse('CNA.txt')
        mRNA = self.parse('mRNA.txt')
        sym = self.parse('sym.txt')
        target_gene = self.parse('target_gene.txt')
        outcome = pd.read_csv('clinical.txt',header=None)
        
        METH_filtered = self.build_target_kernel(METH,sym,target_gene)
        CNA_filtered = self.build_target_kernel(CNA,sym,target_gene)
        mRNA_filtered = self.build_target_kernel(mRNA,sym,target_gene)

        METH_name = "METH_filtered_random"
        CNA_name = "CNA_filtered_random"
        mRNA_name = "mRNA_filtered_random"
        clinical_name = "clinical"
        for i in range(100):
            METH_filtered_random,new_outcome = self.pick_random_columns(METH_filtered,outcome,int(len(CNA.columns)*9/10.0),False)
            CNA_filtered_random,new_outcome = self.pick_random_columns(CNA_filtered,outcome,int(len(CNA_filtered.columns)*9/10.0),False)
            mRNA_filtered_random,new_outcome = self.pick_random_columns(mRNA_filtered,outcome,int(len(mRNA_filtered.columns)*9/10.0),False)

            METH_filtered_random = METH_filtered_random.transpose()
            CNA_filtered_random = CNA_filtered_random.transpose()
            mRNA_filtered_random = mRNA_filtered_random.transpose()
        
            METH_filtered_random.to_csv(METH_name + str(i) + '.txt',sep='\t',index=False,header=False)
            CNA_filtered_random = CNA_filtered_random.astype(int)
            CNA_filtered_random.to_csv(CNA_name + str(i) + '.txt',sep='\t',index=False,header=False)
            mRNA_filtered_random.to_csv(mRNA_name + str(i) + '.txt',sep='\t',index=False,header=False)
        
            new_outcome = new_outcome.astype(int)
            new_outcome.to_csv(clinical_name + str(i) + '.txt',index=False,header=False)

    # June 30 2015
    # Extracting k percentage of data from the original dataset
    # Save in the name of "filename"
    def HynOrder5(self,filename,k):
        METH = self.parse('original-data/METH.txt')
        CNA = self.parse('original-data/CNA.txt')
        mRNA = self.parse('original-data/mRNA.txt')
        sym = self.parse('original-data/sym.txt')
        target_gene = self.parse('original-data/target_gene.txt')
        outcome = pd.read_csv('original-data/clinical.txt',header=None)
        l = len(outcome)

        METH_filtered = self.build_target_kernel(METH,sym,target_gene)
        CNA_filtered = self.build_target_kernel(CNA,sym,target_gene)
        mRNA_filtered = self.build_target_kernel(mRNA,sym,target_gene)


        # Extracts outcome-guided result
        METH_0,METH_0_outcome = self.pick_columns_outcome(METH_filtered,outcome,0)
        METH_1,METH_1_outcome = self.pick_columns_outcome(METH_filtered,outcome,1)

        CNA_0,CNA_0_outcome = self.pick_columns_outcome(CNA_filtered,outcome,0)
        CNA_1,CNA_1_outcome = self.pick_columns_outcome(CNA_filtered,outcome,1)

        mRNA_0,mRNA_0_outcome = self.pick_columns_outcome(mRNA_filtered,outcome,0)
        mRNA_1,mRNA_1_outcome = self.pick_columns_outcome(mRNA_filtered,outcome,1)

        # Extracts k percentage of data with replacement, where 0 <= k <= 1. 

        M0,dummy = self.pick_random_columns(METH_0,METH_0_outcome,int(k*l),duplicated=True)
        M1,dummy = self.pick_random_columns(METH_1,METH_1_outcome,int(k*l),duplicated=True)
        
        C0,dummy = self.pick_random_columns(CNA_0,CNA_0_outcome,int(k*l),duplicated=True)
        C1,dummy = self.pick_random_columns(CNA_1,CNA_1_outcome,int(k*l),duplicated=True)
        
        R0,dummy = self.pick_random_columns(mRNA_0,mRNA_0_outcome,int(k*l),duplicated=True)
        R1,dummy = self.pick_random_columns(mRNA_1,mRNA_1_outcome,int(k*l),duplicated=True)

        print "DONE WITH PROCESSING...."

        M0.to_csv(filename + str("_METH0.txt"),sep='\t',index=False,header=False)
        M1.to_csv(filename + str("_METH1.txt"),sep='\t',index=False,header=False)

        C0.to_csv(filename + str("_CNA0.txt"),sep='\t',index=False,header=False)
        C1.to_csv(filename + str("_CNA1.txt"),sep='\t',index=False,header=False)

        R0.to_csv(filename + str("_mRNA0.txt"),sep='\t',index=False,header=False)
        R1.to_csv(filename + str("_mRNA1.txt"),sep='\t',index=False,header=False)
