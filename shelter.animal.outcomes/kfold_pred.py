from sklearn.cross_validation import KFold
import numpy as np

class kfold_xgb_pred(object):

    def __init__(self, train, test, n_fold=5, n_estimators=None, max_depth=None, min_child_weight=None, gamma=None, 
                 subsample=None, colsample_bytree=None, reg_alpha=None, reg_lambda=None, learning_rate=None):
        self.train = train
        self.test  = test

        self.n_fold = n_fold
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_child_weight = min_child_weight
        self.gamma = gamma
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.learning_rate = learning_rate

    def xgb_train(self, train_set, test_set):

