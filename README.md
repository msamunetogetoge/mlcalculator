# 使い方
docker build -t gunicorn:latest .
docker-compose up -d

# 更新履歴
2020/9/13 ver0.1 回帰分析だけ出来るバージョン。

2020/9/18 ver0.2 ロジスティック回帰も出来るバージョンヘルプページも追加された

2020/9/28 Material-kit を使用してみた目を整えた

2020/10/5 NNを使えるようにした

2020/10/13 テストを書き、github actionでpush毎に実行されるようにした

2020/10/19 docker image にする用のdocker file を置いた

2020/10/23 nginx + gunicorn で動くようにdockerfile などを編集した
