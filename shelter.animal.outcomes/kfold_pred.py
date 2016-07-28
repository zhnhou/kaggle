from sklearn.cross_validation import KFold
import numpy as np
import xgboost

class kfold_xgb_pred(object):

    def __init__(self, train, target, test, n_fold=5, n_estimators=None, max_depth=None, min_child_weight=None, gamma=None, 
                 subsample=None, colsample_bytree=None, reg_alpha=None, reg_lambda=None, learning_rate=None, 
                 seed=None, missing=None):
        self.train = train
        self.target = target
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

        self.seed = seed
        self.missing = missing

        self.xgboost = xgboost.XGBClassifier(missing=self.missing, objective='multi:softprob', seed=self.seed, 
        max_depth=self.max_depth, min_child_weight=self.min_child_weight, gamma=self.gamma, subsample=self.subsample, 
        colsample_bytree=self.colsample_bytree, reg_alpha=self.reg_alpha, reg_lambda=self.reg_lambda,
        learning_rate=self.learning_rate)

    def kfold_train_predict(self):

        n_examples = self.train.shape[0]

        kf = KFold(n_examples, n_folds=self.n_fold, shuffle=False)
        
        for train_index, test_index in kf:
            X_train = self.train.loc[train_idx]
            y_train = self.target.loc[train_idx]

            X_holdout = self.train.loc[test_idx]

            xgb_train = self.xgboost.fit(X_train, y_train)
            y_predict = xgb_train.predict_proba(X_holdout)
            test_predict = xgb.train.predict_proba(self.test)



