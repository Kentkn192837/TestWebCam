import numpy as np
import cv2

def main():
    portnumber = int(input())
    capture = cv2.VideoCapture(portnumber)

    while(True):
        ret, frame = capture.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    