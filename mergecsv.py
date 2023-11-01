import os
import pandas as pd
import re

# カラム名のリスト
column_names = ['time', 'positionX', 'positionY', 'positionZ',
                'RotationX', 'rotationY', 'rotationZ', 'rotationW', 'hint']

# データを保持するための空のデータフレームを作成
merged_df = pd.DataFrame(columns=column_names)

# プレイヤー名を保持するための辞書を作成
file_data_mapping2 = {}
# シーン名を保持するための辞書を作成
file_data_mapping3 = {}

# カレントディレクトリ内の.csvファイルを検索し、ファイル名でソート
csv_files = [file for file in os.listdir() if file.endswith(".csv") and not file.startswith("merged_")]
csv_files.sort()  # ファイル名の照準でソート

for file in csv_files:
    # 2つ目の文字列を取得
    match2 = re.search(r'_.*?_(.*?)_', file)
    extracted_string2 = match2.group(1) if match2 else None
    file_data_mapping2[file] = extracted_string2
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

    # プレイヤー名の列を新たに加える
    df['PlayerName'] = file_data_mapping2[file]
    # シーン名の列を新たに加える
    df['SceneNum'] = file_data_mapping3[file]

    # 読み込んだデータを結合
    merged_df = pd.concat([merged_df, df], ignore_index=True)

# 結合したデータを新しいCSVファイルに保存
merged_df.to_csv('merged_data.csv', index=False)

# CSVファイルを読み込みます
data = pd.read_csv('merged_data.csv')

# 新しいファイルのカウンターを初期化します
file_counter = 1

# 前の行の値を保持する変数を初期化します
previous_value = None

# 新しいファイルに書き込むためのファイルオブジェクトを初期化します
new_file = None

# データをループしてファイルを分割します
for index, row in data.iterrows():
    current_value = row.iloc[0]  # 1列目の値を取得
    value_to_include = row.iloc[12]  # 13列目の値を取得

    # 初めての行または現在の値が前の値より小さい場合、新しいファイルを作成します
    if previous_value is None or current_value < previous_value:
        if new_file:
            new_file.close()  # 前のファイルを閉じます

        # 新しいファイル名を生成します
        new_file_name = f'{value_to_include}_{file_counter}.csv'
        file_counter += 1

        # 新しいファイルを作成し、ヘッダーを書き込みます
        new_file = open(new_file_name, 'w')
        new_file.write(','.join(map(str, row)) + '\n')

    else:
        # 現在の行を既存のファイルに追加します
        new_file.write(','.join(map(str, row)) + '\n')

    # 前の値を更新します
    previous_value = current_value

# 最後のファイルを閉じます
if new_file:
    new_file.close()

print("分割が完了しました。")

