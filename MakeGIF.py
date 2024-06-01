import os
import imageio
from PIL import Image

def create_gif_from_jpegs(folder_path, output_path, duration=0.5):
    # フォルダ内のJPEG画像ファイルのリストを取得
    images = []
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith('.jpeg') or file_name.endswith('.jpg'):
            file_path = os.path.join(folder_path, file_name)
            image = Image.open(file_path)
            images.append(image)

    # 画像を結合してGIFを作成
    imageio.mimsave(output_path, [imageio.imread(img.filename) for img in images], duration=duration)

# 使用例
folder_path = 'Photos'  # JPEG画像が格納されているフォルダのパス
output_path = 'yuki.gif'  # 出力するGIFファイルのパス
duration = 0.1  # 各フレームの表示時間（秒）

create_gif_from_jpegs(folder_path, output_path, duration)
