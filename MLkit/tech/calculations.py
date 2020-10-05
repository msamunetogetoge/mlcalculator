#MLモデルの計算をさせるpythonファイル
import pandas as pd
import numpy as np
import os
from pathlib import Path

from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.metrics import r2_score, log_loss, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier, MLPRegressor

from .models import results
BASE_DIR         = Path(__file__).resolve(strict=True).parent.parent
MEDIA_URL        = '/media/'
MEDIA_ROOT       = os.path.join(BASE_DIR, 'media')
results_path     = os.path.join(MEDIA_ROOT,"results.csv")

class Regression():
    """回帰を行う時に使うクラス
    csvファイルを受け取り、一列目を、それ以外の列から予測するクラス。
    そのうち、訓練用のcsvとテスト用のcsvを受け取って学習とテストを出来るようにするかもしれない。
    暫くは、もらったcsvファイルを訓練：テスト=7:3で分けて学習する。
    学習後は、R二乗誤差を計算して、models.pyのresults に格納する。
    R^2 score は1に近い程良い
    """

    def __init__(self, data):
        data              = pd.read_csv(data).dropna()
        self.columns      = data.columns
        self.y            = data.iloc[:,0]
        self.X            = data.drop(columns=self.columns[0] )
        self.random       = 1

        self.X_train, \
        self.X_test,  \
        self.y_train, \
        self.y_test       = train_test_split(self.X, self.y, test_size=0.3, random_state=self.random )

    def learning(self):
        reg               = LinearRegression().fit(self.X_train, self.y_train)
        self.train_pred   = reg.predict(self.X_train)
        self.pred         = reg.predict(self.X_test)
        train_score       = r2_score(self.y_train ,self.train_pred)
        round_train_score = round(train_score, 2 )
        test_score        = r2_score(self.y_test ,self.pred)
        round_test_score  = round(test_score, 2 )
        R                 = results(title="R^2 score", loss_train=str(round_train_score),loss_test=str(round_test_score), description="1に近い程良い" )
        R.save()
        
    
    def results(self):
        """
        train/test の目印、予測値、元データのように列名を指定して、media root に結果を保存する
        """
        Xs               = pd.concat([self.X_train, self.X_test], axis=0, ignore_index=True)
        ys               = pd.DataFrame(data = np.append(self.y_train, self.y_test), columns = [self.columns[0]])
        preds            = pd.DataFrame(data = np.append(self.train_pred, self.pred), columns=["predict"])
        mask_train       = ["train"]*len(self.y_train)
        mask_test        = ["test"]*len(self.y_test)
        mask             = pd.DataFrame(data = np.append(mask_train, mask_test), columns = ["train_or_test"])
        results          = pd.concat([mask, preds, ys, Xs], axis = 1)
        return results
        

class Logistic():
    """ロジスティック回帰を行う時に使うクラス
    csvファイルを受け取り、一列目を、それ以外の列から予測するクラス。
    そのうち、訓練用のcsvとテスト用のcsvを受け取って学習とテストを出来るようにするかもしれない。
    暫くは、もらったcsvファイルを訓練：テスト=7:3で分けて学習する。
    学習後は、loglossを計算して、models.pyのresults に格納する。
    log_loss は0に近い程良い
    """

    def __init__(self, data):
        self.le           =LabelEncoder()
        data              = pd.read_csv(data).dropna()
        self.columns      = data.columns
        self.y            = data.iloc[:,0]
        self.le           = self.le.fit(self.y)
        self.X            = data.drop(columns=self.columns[0] )
        self.random       = 1
        self.X_train, \
        self.X_test,  \
        self.y_train, \
        self.y_test       = train_test_split(self.X, self.y, test_size=0.3, random_state=self.random )

    def learning(self):
        reg               = LogisticRegression().fit(self.X_train, self.y_train)
        self.train_pred   = reg.predict(self.X_train)
        self.pred         = reg.predict(self.X_test)
        y_train_label     = self.le.transform(self.y_train)
        y_test_label      = self.le.transform(self.y_test)
        train_pred_label  = self.le.transform(self.train_pred)
        pred_label        = self.le.transform(self.pred)  
        train_score       = log_loss(y_train_label ,train_pred_label)
        round_train_score = round(train_score, 2 )
        test_score        = log_loss(y_test_label ,pred_label)
        round_test_score  = round(test_score, 2 )
        R                 = results(title="Log Loss", loss_train=str(round_train_score),loss_test=str(round_test_score), description="0に近い程良い" )
        R.save()
    
    def results(self):
        """
        train/test の目印、予測値、元データのように列名を指定して、media root に結果を保存する
        
        """
        Xs               = pd.concat([self.X_train, self.X_test], axis=0, ignore_index=True)
        ys               = pd.DataFrame(data = np.append(self.y_train, self.y_test), columns = [self.columns[0]])
        preds            = pd.DataFrame(data = np.append(self.train_pred, self.pred), columns=["predict"])
        mask_train       = ["train"]*len(self.y_train)
        mask_test        = ["test"]*len(self.y_test)
        mask             = pd.DataFrame(data = np.append(mask_train, mask_test), columns = ["train_or_test"])
        results          = pd.concat([mask, preds, ys, Xs], axis = 1)
        return results
        
        
class NN_regression():
    """
    ニューラルネットワークで分類を行う時に使うクラス
    csvファイルを受け取り、一列目を、それ以外の列から予測するクラス。
    そのうち、訓練用のcsvとテスト用のcsvを受け取って学習とテストを出来るようにするかもしれない。
    暫くは、もらったcsvファイルを訓練：テスト=7:3で分けて学習する。
    学習後は、Accuracyを計算して、models.pyのresults に格納する。
    計算を楽にするために、sklearn のやつを使う
    """
    def __init__(self, data, layers):
        self.le           = LabelEncoder()
        self.layers       = layers
        data              = pd.read_csv(data).dropna()
        self.columns      = data.columns
        self.y            = data.iloc[:,0]
        self.X            = data.drop(columns=self.columns[0] )
        self.random       = 1
        self.X_train, \
        self.X_test,  \
        self.y_train, \
        self.y_test       = train_test_split(
                            self.X, self.y, test_size=0.3,
                            random_state=self.random )

    def learning(self):
        num_of_features         = self.X.shape[1]
        clf = MLPRegressor(hidden_layer_sizes=self.layers, random_state=1, verbose=False,max_iter=1000,early_stopping=True )
        clf.fit(self.X_train, self.y_train)
        
        self.train_pred         = clf.predict(self.X_train)
        self.pred               = clf.predict(self.X_test)
        train_score             = mean_squared_error(self.y_train, self.train_pred, squared=False)
        test_score              = mean_squared_error(self.y_test, self.pred, squared=False )
        round_train_score       = np.round(train_score,2)
        round_test_score        = np.round(test_score,2)
        R                       = results(title="RMSE", loss_train=str(round_train_score),loss_test=str(round_test_score),description="0に近い程良い" )
        R.save()

    
    def get_results(self):
        """
        train/test の目印、予測値、元データのように列名を指定して、media root に結果を保存する
        """
        Xs                      = pd.concat([self.X_train, self.X_test], axis=0, ignore_index=True)
        
        ys                      = pd.DataFrame(data = np.append(self.y_train, self.y_test), columns = [self.columns[0]])
        preds                   = pd.DataFrame(data = np.append(self.train_pred, self.pred), columns=["predict"])
        mask_train              = ["train"]*len(self.y_train)
        mask_test               = ["test"]*len(self.y_test)
        mask                    = pd.DataFrame(data = np.append(mask_train, mask_test), columns = ["train_or_test"])
        results                 = pd.concat([mask, preds, ys, Xs], axis = 1)
        return results


class NN_classification():
    """
    ニューラルネットワークで分類を行う時に使うクラス
    csvファイルを受け取り、一列目を、それ以外の列から予測するクラス。
    そのうち、訓練用のcsvとテスト用のcsvを受け取って学習とテストを出来るようにするかもしれない。
    暫くは、もらったcsvファイルを訓練：テスト=7:3で分けて学習する。
    学習後は、正解率を計算して、models.pyのresults に格納する。
    コードを楽にするために、sklearn のやつを使う
    """
    def __init__(self, data, layers):
        self.le           = LabelEncoder()
        self.layers       = layers
        data              = pd.read_csv(data).dropna()
        self.columns      = data.columns
        self.y            = data.iloc[:,0]
        self.le           = self.le.fit(self.y)
        self.X            = data.drop(columns=self.columns[0] )
        self.random       = 1
        self.X_train, \
        self.X_test,  \
        self.y_train, \
        self.y_test       = train_test_split(
                            self.X, self.y, test_size=0.3,
                            random_state=self.random )

    def learning(self):
        num_of_features         = self.X.shape[1]
        num_of_class            = len(set(self.le.transform(self.y)))
        y_train_label           = self.le.transform(self.y_train)
        y_test_label            = self.le.transform(self.y_test)
        clf = MLPClassifier(hidden_layer_sizes=self.layers, random_state=1, verbose=False,max_iter=1000,early_stopping=True )
        clf.fit(self.X_train, y_train_label)
        
        self.train_pred         = clf.predict(self.X_train)
        self.pred               = clf.predict(self.X_test)
        train_score             = clf.score(self.X_train, y_train_label)
        test_score              = clf.score(self.X_test, y_test_label )
        round_train_score       = np.round(train_score,2)
        round_test_score        = np.round(test_score,2)
        R                       = results(title="Accuracy", loss_train=str(round_train_score),loss_test=str(round_test_score), description="1に近い程良い" )
        R.save()

    
    def get_results(self):
        """
        train/test の目印、予測値、元データのように列名を指定して、media root に結果を保存する
        """
        Xs                      = pd.concat([self.X_train, self.X_test], axis=0, ignore_index=True)
        ys                      = pd.DataFrame(data = np.append(self.y_train, self.y_test), columns = [self.columns[0]])
        train_preds_label       = self.le.inverse_transform(self.train_pred)
        preds_label             = self.le.inverse_transform((self.pred))
        preds                   = pd.DataFrame(data = np.append(train_preds_label, preds_label), columns=["predict"])
        mask_train              = ["train"]*len(self.y_train)
        mask_test               = ["test"]*len(self.y_test)
        mask                    = pd.DataFrame(data = np.append(mask_train, mask_test), columns = ["train_or_test"])
        results                 = pd.concat([mask, preds, ys, Xs], axis = 1)
        return results


        
