from tech.models import MlModel
MlModel(mdl="回帰分析", code="Regression").save()
MlModel(mdl="ロジスティック回帰", code="Logistic_classification").save()
MlModel(mdl="NN回帰",code="NN_regression").save()
MlModel(mdl="NN分類",code="NN_classification").save()