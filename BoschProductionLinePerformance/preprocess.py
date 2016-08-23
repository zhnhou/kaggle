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

        #self.missval = np.iinfo(np.int16).min
        self.missval = 0

    def convert_categorical_int(self):
        '''
        We remove "T" from the csv file, using int number to identify categories.
        Just a simple sed command to do this job
        I have checked that there is no "T" in column names
        '''

        self.train_categorical_file = self.data_path + 'train_categorical_int.csv'

        if not os.path.isfile(self.train_categorical_file):
            os.system("sed 's/T//g' "+self.train_catorig_file+" > "+self.train_categorical_file)

        self.train_catneg_file = self.data_path + 'train_categorical_negative.csv'

        if not os.path.isfile(self.train_catneg_file):
            os.system("head -n 1 "+self.train_catorig_file+" > "+self.train_catneg_file)
            os.system("grep - "+self.train_categorical_file+" >> "+self.train_catneg_file)

    def check_values_categorical(self):

        ## first check negative values ##
        tmp = pd.read_csv(self.train_catneg_file)

        ## there is no 0 labeled category, so we fill N/A by 0
        tmp = tmp.fillna(0)
        
        print np.unique(tmp[tmp<0].values.astype(np.float64))
        print np.unique(tmp[tmp>0].values.astype(np.float64))

        '''
        negative elements
        [-2147483648 -2147483647 -2147483646 -2147482944 -2147482816 -2147482688
         -2147482432 -2147482176 -2147481664   -21474872   -21474825   -21474819
         -18748192]
        '''
        

    def process_categorical(self, nrows_bundle=100000):

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
            tmp[((tmp > -21474873) & (tmp < 0))] += 21474800
             
            tmp = tmp.fillna( self.missval )

            features = tmp.columns.delete(0) # here remove 'Id' column

            df_cat = df_cat.append(tmp[features].astype(np.int16), ignore_index=True)

        return df_cat
'''
np.unique(df_cat.values)
array([-32640, -28544, -25904, -24592, -23824, -23592, -23568, -23312,
       -23056, -22544, -18350, -17296, -16960, -10112,  -1920,    -72,
          -24,    -20,      0,      1,      2,      3,      4,      5,
            6,      7,      8,      9,     16,     24,     32,     48,
           52,     56,     64,     96,     97,     98,    128,    143,
          145,    256,    340,    492,    512,    514,    768,    917,
         1024,   1132,   1152,   1310,   1372,   2212,   2516,   3968,
         6553,   8768,   9174,  16384,  16512,  18352,  18436,  21216,
        23504,  26228,  26808,  28032,  28800,  30576], dtype=int16)
'''
            
