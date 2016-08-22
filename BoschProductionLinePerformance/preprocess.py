import os
import pandas as pd
import numpy as np

'''
We need to check the maximum/minimum value of the negative/positive categories!
'''

class BPLP_PreProcess(object):
    def __init__(self):
        self.name = 'BoschProductionLinePerformance'
        self.data_path = os.environ['HOME']+'/data_'+os.environ['ENV_HOSTNAME']+'/projects/kaggle/'+self.name+'/'

        self.train_numeric_file = self.data_path + 'train_numeric.csv'
        self.train_catorig_file = self.data_path + 'train_categorical.csv'
        self.train_date_file    = self.data_path + 'train_date.csv'

        self.missval = np.iinfo(np.int16).min

    def process_categorical(self, nrows_bundle=100000):
        '''
        We remove "T" from the csv file, using int number to identify categories.
        Just a simple sed command to do this job
        I have checked that there is no "T" in column names
        '''

        self.train_categorical_file = self.data_path + 'train_categorical_int.csv'

        if not os.path.isfile(self.train_categorical_file):
            os.system("sed 's/T//g' "+self.train_catorig_file+" > "+self.train_categorical_file)

        nrows_skip = 0
        nrows_read = nrows_bundle
        df_cat = pd.DataFrame([])
        while nrows_read == nrows_bundle:
            # use skiprows = range(...)
            skiprows = np.arange(nrows_skip)+1
            tmp = pd.read_csv(self.train_categorical_file, nrows=nrows_bundle, skiprows=skiprows, dtype=np.float32)
            nrows_read = tmp.shape[0]
            nrows_skip += nrows_read

            if nrows_skip == nrows_read:
                line_start = 1
            else:
                line_start = skiprows[-1]+1

            line_end = line_start + nrows_read - 1
            print "Read "+str(nrows_read)+" lines, from "+str(line_start)+" to "+str(line_end)

            tmp[tmp < -2147480000] += 2147480000
            tmp = tmp.fillna( self.missval )

            features = tmp.columns.delete(0) # here remove 'Id' column

            df_cat = df_cat.append(tmp[features].astype(np.int16), ignore_index=True)

        return df_cat

            
