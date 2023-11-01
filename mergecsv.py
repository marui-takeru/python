import os
import pandas as pd
import re

# カラム名のリスト
column_names = ['time', 'positionX', 'positionY', 'positionZ',
                'RotationX', 'rotationY', 'rotationZ', 'rotationW', 'hint']

# データを保持するための空のデータフレームを作成
merged_df = pd.DataFrame(columns=column_names)

# シーン名を保持するための辞書を作成
file_data_mapping3 = {}

# カレントディレクトリ内の.csvファイルを検索し、ファイル名でソート
csv_files = [file for file in os.listdir() if file.endswith(".csv") and not file.startswith("merged_")]
csv_files.sort()  # ファイル名の照準でソート

for file in csv_files:
    # ３つ目の文字列の取得
    match3 = re.search(r'(\d+)\.csv$', file)
    extracted_string3 = match3.group(1) if match3 else None
    file_data_mapping3[file] = extracted_string3

    # 各CSVファイルを読み込み
    df = pd.read_csv(file, names=column_names, header=None)

    # 速度 (Vx、Vy、Vz) を計算
    df['Vx'] = (df['positionX'] - df['positionX'].shift(1)) / (df['time'] - df['time'].shift(1))
    df['Vy'] = (df['positionY'] - df['positionY'].shift(1)) / (df['time'] - df['time'].shift(1))
    df['Vz'] = (df['positionZ'] - df['positionZ'].shift(1)) / (df['time'] - df['time'].shift(1))

    # シーン名の列を新たに加える
    df['sceneNum'] = file_data_mapping3[file]

    # 読み込んだデータを結合
    merged_df = pd.concat([merged_df, df], ignore_index=True)

# 結合したデータを新しいCSVファイルに保存
merged_df.to_csv('merged_data.csv', index=False)
