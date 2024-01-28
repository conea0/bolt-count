#!/usr/bin/env python3
#!/usr/bin/env python

import cv2
import os
import numpy as np

def process_camera_images(crop_coordinates,i):
    # カメラにアクセス
    cap = cv2.VideoCapture(0)  # カメラ番号（0番目のカメラを使用）

    while True:

        # カメラからフレームを読み込む
        ret, frame = cap.read()

        # カメラからの読み込みが成功した場合
        if ret:
            # 切り抜き座標で画像を切り抜く

            x, y, w, h = crop_coordinates
            cropped_frame = frame[y:y+h, x:x+w]

            # 画像をグレースケールに変換
            cropped_gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

            # ネジの平均比率を計算するためのリスト
            #MedianList = []

            # ネジの平均比率を計算
            #count_neji(cropped_gray, MedianList)

            # ネジの平均比率を計算
            #average_ratio = np.mean(MedianList)
            #print(average_ratio)
            
            #nejinokoyuti
            if i == 1:
                average_ratio = 19.75


            # ネジの総数を計算
            screw_count,ret = calculate_total_screws(cropped_gray, average_ratio)
            #float->int
            screw_count = round(screw_count)

            # screw_count > 16
            if screw_count >= 16:
                screw_count = "Error"

            # ネジの数を切り取られた範囲の映像上に表示
            cv2.putText(cropped_frame, f"Screws: {screw_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # 画面に処理されたフレームを表示
            cv2.imshow('Screw Count', cropped_frame)

            # キー入力を待ち、'q'が押されたらループを抜ける
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # カメラを解放してウィンドウを閉じる
    cap.release()
    cv2.destroyAllWindows()

def count_neji(frame, MedianList):
    # 2値化
    ret, dst = cv2.threshold(frame, 115, 255, cv2.THRESH_BINARY_INV)
    bolt_num =15
    # 黒と白の比から、ネジ一本当たりの比の平均を計算する。
    black_pixels = np.sum(dst == 0)  # 黒いピクセルの数
    white_pixels = np.sum(dst == 255)  # 白いピクセルの数

    if white_pixels == 0:
        ratio = 0
    else:
        ratio = white_pixels / bolt_num

    MedianList.append(ratio)

def calculate_total_screws(frame, average_ratio):
    # 画像内のネジの総数を計算する
    # 2値化
    ret, dst = cv2.threshold(frame, 115, 255, cv2.THRESH_BINARY_INV)

    white_pixels = np.sum(dst == 255)  # 白いピクセルの数
    screw_count = white_pixels / average_ratio
    return screw_count , dst

# メイン関数
if __name__ == '__main__':
    
    i = int(input())
    
    # 切り抜き座標を指定 (x, y, width, height)
    crop_coordinates = (250, 200, 136, 100)

    # リアルタイムのカメラ映像を処理
    process_camera_images(crop_coordinates,i)
