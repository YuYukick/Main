#! /usr/bin/env python
# coding: utf-8
# coding=utf-8
# -*- coding: utf-8 -*-
# vim: fileencoding=utf-8

### GamePad
## LogicoolのF310を使用
## ゲームパッド入力確認完了 1209
## 左アナログスティック，バンパーの入力確認完了 1209
## 軸の対応を合わせた 1209
## トリガ値の表示と確認 1210

import pygame
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

UP_J = 0 #
DOWN_J = 1
LEFT_J = 2
RIGHT_J = 3
J_R = 0 #
J_L = 1
BMPR = 2
BUMPER_R = -1
BUMPER_L = 0
J_L_X = 0 #
J_L_Y = 1
J_R_X = 3
J_R_Y = 4
B_L = 2
B_R = 5

UP_L    = 0
DOWN_L  = 1 
LEFT_L  = 2 
RIGHT_L = 3 
UP_R    = 4 #
DOWN_R  = 5 
LEFT_R  = 6 
RIGHT_R = 7 
R_BUMPER = 8
L_BUMPER = 9 

incri = 0
JOY_LIMI = 0.8  #0.8:縦横のみ 0.7:シビアに斜め 0.6-5:斜め
BUN_LIMI = 0.6

MeasureMode = False #True:measurement mode False:manual control mode 

#入力トリガ
JOYSTICK_TRIG = [] #0:up 1:down 2:right 3:left, 0-3:RIGHT_J 4-7:LEFT_J 8:Bumper_R 8:Bumper_L
BUTTON_TRIG = [] #
for incri in range(11):
    BUTTON_TRIG.append(False)
    # print BUTTON
    if incri < 10:
        JOYSTICK_TRIG.append(False)

pygame.joystick.init()

try:
    j = pygame.joystick.Joystick(0) # create a joystick instance
    j.init() # init instance
    print "使用状態:" + str(j.get_init())   #
    print "ID:" + str(j.get_id())   # 
    print 'Joystickの名称: ' + j.get_name()    # ゲームパッドの名前
    print 'ボタン数 : ' + str(j.get_numbuttons())   # ゲームパッドにボタンはいくつあるの？ => 11軸
    print "軸の数(axis):" + str(j.get_numaxes())   # ゲームパッドに軸はいくつあるの？ => 6軸
    print "BUTTON_TRIG" + str(BUTTON_TRIG)  #ボタン押したかのトリガ
    print "JOYSTICK_TRIG" + str(JOYSTICK_TRIG)  #ジョイスティックのトリガ

except pygame.error:
    print 'Joystickが見つかりませんでした。'

def mask_process(inpt, j_stick, U__R):
    if j_stick != BMPR:
        if inpt > JOY_LIMI:#0.8
            JOYSTICK_TRIG[U__R + (j_stick*4 + 1)] = True
        elif inpt < (JOY_LIMI*(-1)):#-0.8
            JOYSTICK_TRIG[U__R + j_stick*4] = True
        else:
            JOYSTICK_TRIG[U__R + j_stick*4] = False
            JOYSTICK_TRIG[U__R + (j_stick*4 + 1)] = False
    elif j_stick == BMPR:
        if inpt > BUN_LIMI:
            JOYSTICK_TRIG[U__R + (j_stick*4 + 1)] = True
        else:
            JOYSTICK_TRIG[U__R + (j_stick*4 + 1)] = False

def main():
    pygame.init()
    screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) ) # 画面を作る
    pygame.display.set_caption('Joystick') # タイトル
    pygame.display.flip() # 画面を反映

    # i = 0

    while True:
        # print i #whileループが止まっていないかを確認したかった
        # i = i+1

        for e in pygame.event.get(): # イベントチェック
            if e.type == QUIT: # 終了が押された？
                return
            if (e.type == KEYDOWN and
                e.key  == K_ESCAPE): # ESCが押された？
                return
            # Joystick関連のイベントチェック
            if e.type == pygame.locals.JOYAXISMOTION: # 7
                # x , y = j.get_axis(0), j.get_axis(1)
                # x1 , y1 = j.get_axis(3), j.get_axis(4)
                # x2 , y2 = j.get_axis(2), j.get_axis(5)
                x , y = j.get_axis(J_L_X), j.get_axis(J_L_Y)
                x1 , y1 = j.get_axis(J_R_X), j.get_axis(J_R_Y)
                x2 , y2 = j.get_axis(B_L), j.get_axis(B_R)

                # print 'x and y : ' + str(x) +' , '+ str(y)
                # print ('x and y : {0:>8.5f} {1:>8.5f}, x1 and y1 : {2:>8.5f} {3:>8.5f}, x2 and y2 : {4:>8.5f} {5:>8.5f}'.format(x , y, x1 , y1, x2 , y2))
                # print type(x) #float
                
                mask_process(j.get_axis(J_L_X), J_L, LEFT_J)
                mask_process(j.get_axis(J_L_Y), J_L, UP_J)
                mask_process(j.get_axis(J_R_X), J_R, LEFT_J)
                mask_process(j.get_axis(J_R_Y), J_R, UP_J)
                mask_process(j.get_axis(B_L), BMPR, BUMPER_L)
                mask_process(j.get_axis(B_R), BMPR, BUMPER_R)
                # print "JOYSTICK:" + str(JOYSTICK_TRIG)

            elif e.type == pygame.locals.JOYBALLMOTION: # 8
                print 'ball motion'
            elif e.type == pygame.locals.JOYHATMOTION: # 9
                # print 'hat motion ： ' + str(j.get_numhats())
                print ('hat motion ： {0:d}'.format(j.get_numhats()))
                # hat = j.get_numhats()

            elif e.type == pygame.locals.JOYBUTTONDOWN: # 10
                BUTTON_TRIG[e.button] = True
                # print str(e.button)+'番目のボタンが押された'
                # print BUTTON_TRIG[e.button]
                print "BUTTON:" + str(BUTTON_TRIG)

            elif e.type == pygame.locals.JOYBUTTONUP: # 11
                BUTTON_TRIG[e.button] = False
                # print str(e.button)+'番目のボタンが離された'
                # print BUTTON_TRIG[e.button]
                # print type(e.button) #int
                print "BUTTON:" + str(BUTTON_TRIG)


        # if(BUTTON_TRIG[8] == True):
        #     ~MeasureMode
        #     print ~MeasureMode


        # if(BUTTON_TRIG[9] == True):
        #     if(BUTTON_TRIG[] == True)

if __name__ == '__main__': main() #モジュール化を考えたテスト的な処理の書き方
# end of file