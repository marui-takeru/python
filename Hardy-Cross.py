import numpy as np # 使用するモジュールの定義

g = 9.8 # 重力加速度の定義

# ===========================
#        関数群の定義
# ===========================

def hardy_cross_k(f, L, D): # [h = kQ^2] における"k"の定義
    return 8.0 * f * L / (g * np.power(np.pi, 2.0) * np.power(D, 5.0))

def hardy_cross_numerator(k, Q): # [ΣkQ^2]（ΔQの分子）の定義
    return k * np.power(Q, 2.0)

def hardy_cross_denominator(k, Q): # [2ΣkQ]（ΔQの分母）の定義
    return np.absolute(k) * np.absolute(Q) # 両方絶対値を取る

def hardy_cross_flow_correction(numerator, denominator): # ΔQの定義
    return (-1.0 * numerator) / (2.0 * denominator)

def hardy_cross_loop_iteration(f, L, D, k, Q, pipes_name=None): # ループする関数の定義

    delta_Q = 10.0 # ΔQの初期値を10に設定
    modify_count = 0 # 補正回数のカウント

    # |ΔQ|が0.008以下になるまで繰り返す
    while np.absolute(delta_Q) > 0.008: # 条件値を0.007以下にするとoverflow（発散）してしまう

        numerator_sum = 0.0 # [ΣkQ^2]（ΔQの分子）を0にリセット
        denominator_sum = 0.0 # [2ΣkQ]（ΔQの分母）を0にリセット

        for i in range(len(D)):
            k.append(hardy_cross_k(f[i], L[i], D[i])) # kの作成
            # print("The value of k is %f" % k[i]) # ←確認用
            # print("Given f=%f, L=%f, D=%f, thus k=%f" % (f[i], L[i], D[i], k[i])) # ←確認用

            if Q[i] < 0: # 仮定した流量がマイナス成分の時
                k[i] = (-1.0) * k[i] # kの値を-1倍する

            numerator_sum += hardy_cross_numerator(k[i], Q[i]) # 分子のΣ計算
            denominator_sum += hardy_cross_denominator(k[i], Q[i]) # 分母のΣ計算
            # print(numerator_sum) # ←確認用
            # print(denominator_sum) # ←確認用

        for i in range(len(D)):
            delta_Q = hardy_cross_flow_correction(numerator_sum, denominator_sum) # ΔQを求める
            # print(delta_Q) # ←確認用

            Q[i] += delta_Q # ←流量Qの補正
            # print("The flow in pipe %s is %f" % (pipes_name[i], Q[i])) # ←確認用

        modify_count += 1 # 補正回数 +1

    print("補正回数：", modify_count)

    return Q # 流量Qを返り値とする

def main(): # メイン関数の定義

    # ===========================
    #        　初期条件
    # ===========================

    # =======管路Ⅰの条件=======

    # 管路の名前
    name_1_array = ['AB', 'BE', 'EF', 'FA']
    # 管径(m)
    D1 = [0.4, 0.27, 0.4, 0.3]
    # 管長(m)
    L1 = [300.0, 495.2, 300.0, 500.0]
    # 摩擦損失係数
    f1 = [0.0285, 0.0326, 0.0285, 0.0314]
    # 仮定した流量Q
    guess_Q1 = [-0.35, -0.1, 0.35, 0.15]
    # [h=kQ^2]:比例定数"k"
    k1 = []

    # =======管路Ⅱの条件=======

    # 管路の名前
    name_2_array = ['BCD', 'DE', 'BE']
    # 管径(m)
    D2 = [0.3, 0.3, 0.27]
    # 管長(m)
    L2 = [700.0, 200.0, 495.2]
    # 摩擦損失係数
    f2 = [0.0314, 0.0314, 0.0326]
    # 仮定した流量Q
    guess_Q2 = [-0.25, 0.45, 0.1]
    # [h=kQ^2]:比例定数"k"
    k2 = []

    # ===========================
    #        　実行開始
    # ===========================

    print("管路Ⅰ") # 管路Ⅰの場合

    Q1 = hardy_cross_loop_iteration(f1, L1, D1, k1, guess_Q1, name_1_array)
    for i in range(len(Q1)):
        print(name_1_array[i], "を流れる流量：", Q1[i])

    print("============")

    print("管路Ⅱ")# 管路Ⅱの場合

    Q2 = hardy_cross_loop_iteration(f2, L2, D2, k2, guess_Q2, name_2_array)
    for i in range(len(Q2)):
        print(name_2_array[i], "を流れる流量：", Q2[i])

if __name__ == "__main__":
    main()
