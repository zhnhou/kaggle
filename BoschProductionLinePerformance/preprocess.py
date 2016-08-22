import os
import pandas as pd

class BPLP_PreProcess(object):
    def __init__(self):
        self.name = 'BoschProductionLinePerformance'
        self.data_path = os.environ('HOME')+'/data_'+os.environ('ENV_HOSTNAME')+'/projects/kaggle/'+self.name+'/'

        self.train_numeric_file = self.data_path + 'train_numeric.csv'
        self.train_catorig_file = self.data_path + 'train_categorical.csv'
        self.train_date_file    = self.data_path + 'train_date.csv'

    def process_categorical(self, nrows_bundle=100000):
        '''
        We remove "T" from the csv file, using int number to identify categories.
        Just a simple sed command to do this job
        '''

        self.train_categorical_file = self.data_path + 'train_categorical_int.csv'

        if not os.path.isfile(self.train_categorical_file):
            os.system("sed 's/T//g' "+self.train_catorig_file+" > "+self.train_categorical_file)

        nrows_read = nrows_bundle
        while nrows_read == nrows_bundle
            tmp = pd.read_csv(self.train_categorical_file, nrows=nrows_bundle)
            nrow_read = tmp.shape[0]
            print "Read "+str(nrow_read)+' lines'

            tmp[tmp < -2147480000] += 2147480000

        
