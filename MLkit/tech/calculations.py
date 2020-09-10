#MLモデルの計算をさせるpythonファイル
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from .models import results

class Regression():
    """回帰を行う時に使うクラス
    csvファイルを受け取り、一列目を、それ以外の列から予測するクラス。
    そのうち、訓練用のcsvとテスト用のcsvを受け取って学習とテストを出来るようにするかもしれない。
    暫くは、もらったcsvファイルを訓練：テスト=7:3で分けて学習する。
    学習後は、R二乗誤差を計算して、models.pyのresults に格納する。
    """

    def __init__(self, data):
        data         = pd.read_csv(data)
        self.columns =  data.columns
        self.y       = data.iloc[:,0]
        self.X       = data.drop(columns=self.columns[0] )
        self.random  = 1

        self.X_train, \
        self.X_test,  \
        self.y_train, \
        self.y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=self.random )

    def learning(self):
        reg         = LinearRegression().fit(self.X_train, self.y_train)
        pred        = reg.predict(self.X_test)
        score       = r2_score(self.y_test ,pred)
        round_score = round(score, 2 )
        R           = results(title="R^2 score", loss=str(score) )
        R.save()
        #return f"R^2 スコアは、 {round_score} です。"
        

