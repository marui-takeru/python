# 必要なモジュールの宣言
import os
import re
import numpy as np
import pandas as pd

# 速度を計算する関数
def calculate_and_add_velocity_columns(csv_file):
    column_names = ['time', 'positionX', 'positionY', 'positionZ',
                    'RotationX', 'rotationY', 'rotationZ', 'rotationW', 'hint']
    df = pd.read_csv(csv_file, sep=',', header=None, names=column_names)
    df['Vx'] = (df['positionX'] - df['positionX'].shift(1)) / (df['time'] - df['time'].shift(1))
    df['Vy'] = (df['positionY'] - df['positionY'].shift(1)) / (df['time'] - df['time'].shift(1))
    df['Vz'] = (df['positionZ'] - df['positionZ'].shift(1)) / (df['time'] - df['time'].shift(1))
    # x座標とz座標をもとに作成した２Dの速度の大きさ
    df['2DVelocityMagnitude'] = np.sqrt(df['Vx']**2 + df['Vz']**2)
    # x座標とy座標とz座標をもとに作成した3Dの速度の大きさ
    df['3DVelocityMagnitude'] = np.sqrt(df['Vx']**2 + df['Vy']**2 + df['Vz']**2)
    return df

def interpolate_missing_values(df):
    time_diff = df['time'] - df['time'].shift(1)
    interpolated_rows = []

    for index, diff in enumerate(time_diff):
        if diff >= 2:
            num_interpolations = int(diff) - 1
            for i in range(1, num_interpolations + 1):
                new_time = df['time'].iloc[index] + i
                interpolation = (df.iloc[index] * (num_interpolations + 1 - i) + df.iloc[index + 1] * i) / (num_interpolations + 1)
                interpolation['time'] = new_time
                interpolated_rows.append(interpolation)

    if interpolated_rows:
        interpolated_df = pd.DataFrame(interpolated_rows)
        df = pd.concat([df, interpolated_df], ignore_index=True)

    return df

# メイン関数
def process_csv_files(csv_files):
    # csvファイルの名称から取得する情報
    file_data_mapping1 = {} # １つ目の文字列=日付
    file_data_mapping2 = {} # ２つ目の文字列=プレイヤー名
    file_data_mapping3 = {} # ３つ目の文字列=シーン名

    branch_number = 1 #枝番
    merged_df = pd.DataFrame() #merged_dfのデータフレームの中身を空にしておく

    for file in csv_files:
        # １つ目の文字列の取得
        match1 = re.search(r'_(.*?)_', file)
        extracted_string1 = match1.group(1) if match1 else None
        file_data_mapping1[file] = extracted_string1

        # ２つ目の文字列の取得
        match2 = re.search(r'_.*?_(.*?)_', file)
        extracted_string2 = match2.group(1) if match2 else "Unknown"
        file_data_mapping2[file] = extracted_string2

        # ３つ目の文字列の取得
        match3 = re.search(r'(\d+)\.csv$', file)
        extracted_string3 = match3.group(1) if match3 else None
        file_data_mapping3[file] = extracted_string3

    # １つ目の文字列を参照してcsvファイルを昇順に並び替える
    sorted_csv_filenames1 = sorted(
        file_data_mapping1.keys(), key=lambda x: file_data_mapping1[x])

    # １つ前の
    prev_extracted_string2 = None
    merged_filename = None  # 初期値を設定

    for file in sorted_csv_filenames1:
        try:
            df_with_velocities = calculate_and_add_velocity_columns(file)
            df_with_velocities = interpolate_missing_values(df_with_velocities)
            df_with_velocities["sceneNum"] = file_data_mapping3[file] # シーン名の列を新たに加える
            extracted_string2 = file_data_mapping2[file]

            # 1つ前のcsvファイルのプレイヤー名が今読んでいるプレイヤー名と異なる場合の処理
            # ->結合しない
            if prev_extracted_string2 is not None and extracted_string2 != prev_extracted_string2:
                merged_filename = f"merged_{prev_extracted_string2}_{branch_number}.csv"
                df_with_velocities.to_csv(merged_filename, index=False, header=True)
                print(f"前後のCSVファイルのプレイヤー名が異なっていたため、CSVファイルを結合しませんでした: {merged_filename}")
                branch_number += 1
                merged_df = pd.DataFrame()

            # １つ前のcsvファイルの第１列（time）の最後の値が
            # 今読んでいるcsvファイルの第１列（time）より時間が経過していた場合の処理
            # ->結合しない
            if not merged_df.empty:
                prev_time = merged_df['time'].iloc[-1]
                current_time = df_with_velocities['time'].iloc[1]
                if current_time < prev_time:
                    merged_filename = f"merged_{prev_extracted_string2}_{branch_number}.csv"
                    df_with_velocities.to_csv(merged_filename, index=False, header=True)
                    print(
                        f"１つ前のCSVの最終時間よりこのCSVファイルの開始時間が早かったため、CSVファイルを結合しませんでした: {merged_filename}")
                    branch_number += 1
                    merged_df = pd.DataFrame()

            merged_df = pd.concat([merged_df, df_with_velocities], axis=0, ignore_index=True)
            prev_extracted_string2 = extracted_string2

        except Exception as e:
            print(f"{file} の処理中にエラーが発生しました: {e}") #エラーの詳細を吐く

    if not merged_df.empty: # 最後のCSVファイルの処理
        merged_filename = f"merged_{prev_extracted_string2}_{branch_number}.csv"
        merged_df.to_csv(merged_filename, index=False, header=True)
        print(f"最後のCSVファイルを保存しました: {merged_filename}")
        print("===============================================================================================")
        print("")
        print(f"CHECK!!!: 読み込んだcsvファイルの数: {len(csv_files)} >= 結合後のcsvファイルの数: {branch_number}")
        print("")
        print("===============================================================================================")

if __name__ == "__main__": #　プログラムスタート
    # このpyファイルと同じディレクトリにあるcsvファイルを見つけ、読み込む。
    # その際に、".csv.meta"と"merged_"は読み込まない
    csv_files = [file for file in os.listdir()
                 if file.endswith(".csv") and
                 not file.endswith(".csv.meta") and
                 not file.startswith("merged_")]
    print(f"読み込んだcsvファイルの数: {len(csv_files)}")
    print("===================================================================================================")
    process_csv_files(csv_files)
