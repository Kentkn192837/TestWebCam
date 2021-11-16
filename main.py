import numpy as np
import cv2
import datetime

WIDTH = 800
HEIGHT = 600

def play(cap):
    ret, frame = cap.read()
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', WIDTH, HEIGHT)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('s'):
        dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%f')
        cv2.imwrite('D:\Images\{}.jpg'.format(dt), frame)
        print('保存先: D:\Images\{}.jpg'.format(dt), 'に保存しました')

def run(portnumber):
    cap = cv2.VideoCapture(portnumber)
    if cap.isOpened() == False:
        print("動画ファイルのパスが間違っているか、そのポートにはカメラが接続されていません")
        return

    while True:
        play(cap)

    cap.release()
    cv2.destroyAllWindows()

def main():
    print('カメラのポート番号を指定してください')
    portnumber = int(input())
    run(portnumber)

if __name__ == '__main__':
    main()
