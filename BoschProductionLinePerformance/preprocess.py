import os
import pandas as pd
import numpy as np

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
        '''

        self.train_categorical_file = self.data_path + 'train_categorical_int.csv'

        if not os.path.isfile(self.train_categorical_file):
            os.system("sed 's/T//g' "+self.train_catorig_file+" > "+self.train_categorical_file)

        nrows_skip = 0
        nrows_read = nrows_bundle
        while nrows_read == nrows_bundle:
            # use skiprows = range(...)
            tmp = pd.read_csv(self.train_categorical_file, nrows=nrows_bundle, skiprows=np.arange(nrows_skip-1)+1)
            nrows_read = tmp.shape[0]
            nrows_skip += nrows_read
            print "Read "+str(nrows_read)+' lines'

            tmp[tmp < -2147480000] += 2147480000
            tmp = tmp.fillna( self.missval )

            features = tmp.columns.delete(0) # here remove 'Id' column

            if nrows_skip == nrows_read:
                df_cat = tmp[features].astype(np.int16)
            else:
                df_cat.append(tmp[features].astype(np.int16), ignore_index=True)

        return df_cat

            
