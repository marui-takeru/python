#モジュールのインポート
import numpy as np

#integerの定義（Pythonでは必要ないけど。）
i = 0
j = 0


Tsunami_Data = np.empty((0, 3), dtype=float)#Numpy用の空のリストを用意＊正確には何も入っていない２次元配列を作成

#インデックスの作成（時間がなかったので手動で挿入）
Tsunami_Data = ["ID_START", "ID_GOAL", "DISTANCE"]

#0から170までの３次元行列の作成
for i in range(171):
    for j in range(171):
        Tsunami_Data = np.vstack((Tsunami_Data, np.array([i, j, 20])))

print(Tsunami_Data)

np.savetxt("/Users/moriwakiryou/Desktop/EachSceneDistances.csv", Tsunami_Data, delimiter = ",", fmt = '% s')
print("Finished")
