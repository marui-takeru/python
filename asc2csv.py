#モジュールのインポート
import glob
import numpy as np
from natsort import natsorted

i = 0
Tsunami =[]#空リストの用意
Tsunami_Data = np.empty((0, 2), dtype=float)#Numpy用の空のリストを用意＊正確には何も入っていない２次元配列を作成

print("今から読み込みます")
for file in natsorted(glob.glob("/Users/moriwakiryou/Desktop/case11_10-03_Ze/*")):
    print(file)
    f = open(file)
    s = f.read(170).split(' ')#1から170文字まで読み込み
    Tsunami = s[14]#数値が入っていたリストを代表として抽出
    Tsunami_Data = np.vstack((Tsunami_Data, np.array([i, Tsunami])))
    i += 1
    print(i, Tsunami)
    
print(Tsunami_Data)
np.savetxt("/Users/moriwakiryou/Desktop/Tsunami.csv", Tsunami_Data, delimiter = ",", fmt = '% s')    
print("完了です")