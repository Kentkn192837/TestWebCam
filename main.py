import sys
import os
import cv2
import datetime
import numpy as np

class MotiondetectionCamera:
    count = -1                  # 差分の計算を行うフレームが揃うまで計算をスキップするための変数
    frame = None                # カメラからの最新の映像情報を記録する変数
    pre_frame = None            # 1フレーム前のカメラからの映像情報を記録する変数
    pre_diff = None             # 計算した差分の結果を記録しておく変数
    cap = False                 # cv2.VideoCaptureの戻り値を代入する変数
    shutter_event_flag = False  # 撮影を行うかどうかのフラグ

    def __init__(self, portnumber):
        self.cap = cv2.VideoCapture(portnumber)
        self.__run()
    
    def __frame_format(self, frame):
        frame = cv2.resize(frame, dsize=(6000, 4000))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame
    
    def __motion_judge(self, diff_value):
        threshold = 5000 # どれくらいの動きを検知するかはこの値を修正する
        if self.count <= 1:
            self.pre_diff = diff_value
            print("モーション判定処理の準備中です")
            return
        if self.count > 2:
            print("差分:", abs(diff_value - self.pre_diff))
        
        # 指定した閾値によって撮影フラグを立てる処理
        if abs(diff_value - self.pre_diff) > threshold:
            print("物体が動きました")
            self.shutter_event_flag = True
        else:
            print("動いている物体はありません")
            if self.shutter_event_flag:
                self.__shutter() # 撮影
            self.shutter_event_flag = False
        self.pre_diff = diff_value
    
    # 取得した映像の変化量を計算
    def __calcSubtraction(self, frame):
        pre_frame = self.__frame_format(self.pre_frame)
        frame = self.__frame_format(frame)
        frame_absdiff = cv2.absdiff(frame, pre_frame)
        diff_value = int(frame_absdiff.sum() / 10000)
        return diff_value
    
    # 画像撮影処理
    def __shutter(self):
        # 保存する画像サイズを指定
        frame = cv2.resize(self.frame, dsize=(6000, 4000))

        # 保存するファイル名の指定
        dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%f')
        dir_list = ['D:\\', datetime.datetime.now().strftime('%Y-%m-%d'), '{}.jpg'.format(dt)]
        file_name = os.path.join(*dir_list)
        print('保存先: {}'.format(file_name))
        cv2.imwrite(file_name, frame)
        print("撮影しました")
  
    def __play(self):
        _, frame = self.cap.read()
        self.frame = frame      # 現在のフレームを取得
        if self.count >= 0 :
            diff = self.__calcSubtraction(frame)
            self.__motion_judge(diff)
        
        # ウインドウ描画処理
        cv2.namedWindow('video', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('video', 6000, 4000)
        cv2.imshow('video', frame)

        # 1フレーム前のフレームを記録
        self.pre_frame = frame
        self.count += 1
    
    def __run(self):
        if self.cap.isOpened() == False:
            print("動画ファイルのパスが間違っているか、そのポートにはカメラが接続されていません")
            return

        # メインループ
        while True:
            self.__play()
            if cv2.waitKey(1) & 0xFF == ord('q'): # qキー押下でプログラムを終了する
                break

        cv2.destroyAllWindows()
        sys.exit(0)

if __name__ == '__main__':
    while True:
        print("内蔵カメラを使う場合は0を入力")
        MotiondetectionCamera(int(input()))
