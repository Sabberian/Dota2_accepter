import wx
from time import sleep

import cv2
import numpy as np
import pyautogui as pg
from PIL import ImageGrab

lang = int(input('Русский - 1, Английский - 0: '))

def normalize_template(path):
    try:
        return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
    except:
        return None

def normalize_screen(sc):
    return cv2.cvtColor(sc, cv2.COLOR_BGR2GRAY)
try:
    app = wx.App(False)
    S_WIDTH, S_HEIGHT = wx.GetDisplaySize()
    ACCEPT_BOX = ((S_WIDTH//3),(S_HEIGHT//3),S_WIDTH-(S_WIDTH//3),S_HEIGHT-(S_HEIGHT//3))
    RU_ACCEPT_TEMPLATE = normalize_template('accept.png')
    ENG_ACCEPT_TEMPLATE = normalize_template('accept_eng.png')
    RU_SIZE = ENG_ACCEPT_TEMPLATE.shape[::-1]
    EN_SIZE = ENG_ACCEPT_TEMPLATE.shape[::-1]
    IS_SCREEN_WORKING = True
except Exception as e:
    print('1, ', e)
    sleep(10)

def grab_screen(bbox):
    global IS_SCREEN_WORKING
    screen = None
    try:
        screen = ImageGrab.grab(bbox=bbox)
        IS_SCREEN_WORKING = True
    except:
        IS_SCREEN_WORKING = False
    return screen


if __name__ == '__main__':
    try:
        while True:
            s = grab_screen(ACCEPT_BOX)
            if IS_SCREEN_WORKING:
                s.save('screen.png')
                screen = normalize_template('screen.png')
                if lang == 1:
                    res = cv2.matchTemplate(screen, RU_ACCEPT_TEMPLATE, cv2.TM_CCOEFF_NORMED)
                else:
                    res = cv2.matchTemplate(screen, ENG_ACCEPT_TEMPLATE, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res>=0.8)
                x, y = loc[0], loc[1]
                if len(x) > 0:
                    pg.click(S_WIDTH//3 + x[-1] + RU_SIZE[0]//2, S_HEIGHT//3+y[-1] + RU_SIZE[1]//2)
                sleep(0.01)
    except Exception as e:
        print('2, ', e)
        sleep(10)