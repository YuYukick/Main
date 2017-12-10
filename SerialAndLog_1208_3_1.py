# coding: utf-8 

###11/27
## 4つのセンサからの値の取得が完了
##　取得したデータのリスト化が完了
##　取得値の正負判別
## list型からstr型への変換ができてない，時間の取得ができるようになった
## list型→str型→float型への変換が完了
## 開設ポートの確認ができる
## 書き方汚いけど4ch分の出力値を確認できた

# ------------------------
#   モジュールインポート
# ------------------------
# GPIOモジュールインポート
import RPi.GPIO as GPIO
# timeモジュールインポート
import time
#
import serial
# # SPIモジュール
# import wiringpi2 as wipi
from datetime import datetime


# # ----------------------------
# #   SPI動作環境の設定
# # ----------------------------
# # SPI channel (0 or 1)
# SPI_CH = 0
# # SPI speed (1MHz)
# SPI_SPEED = 1000000

# # setup
# wiri.wiringPiSPISetup (SPI_CH, SPI_SPEED)
# wiri.wiringPiSetupGpio()
# wiri.pinMode(LED_PIN, wiri.GPIO.OUTPUT)


# ----------------------------
#   シリアルの設定
# ----------------------------
# USB-Serialを使用する場合、ttyUSB0
# GPIOピンを使用する場合、ttyAMA0
#msr_serial = serial.Serial('/dev/ttyUSB0', 19200, serial.PARITY_NONE = 0, serial.STOPBITS_ONE = 1, serial.EIGHTBITS = 8, timeout = 10)	#ポートオープン
msr_serial = serial.Serial('/dev/ttyUSB0', 19200, timeout= 5)
msr_serial.setByteSize(8)
msr_serial.setStopbits(2)
#msr_serial.setParity(0)

#msr_serial.open()
print  "serial port open..."

# msr_serial = serial.Serial(
# 				port ='/dev/ttyUSB0',
# 				baundrate = 19200,
# 				parity = serial.PARITY_NONE,
# 				stopbits = serial.STOPBITS_ONE,
# 				bytesize = serial.EIGHTBITS,
# 				timeout=10
# 				)
#msr_serial = serial.Serial('/dev/ttyAMA0', 19200, timeout=10)
print  msr_serial.portstr	#使用ポートの表示


# ----------------------------
#   GPIO番号の定義(GPIO番号)
# ----------------------------
# GPIOの番号の定義
# 出力
pinOUT = {
	'pls_x'	:	14,
	'pls_z'	:	15,
	'dir_x'	:	 4,
	'dir_z'	:	17,
	'stp_x'	:	22,
	'stp_z'	:	27,
	'mod_tp':	 5
}

# 入力
pinIN = {
	'up'	:	 6,
	'down'	:	13,
	'right'	:	19,
	'left'	:	26,
	'rdy_x'	:	18,
	'rdy_z'	:	23,
	'alt_x'	:	20,
	'alt_z'	:	21,
	'mode01':	24,
	'mode02':	25,
}

# ------------------
#   GPIOモード設定
# ------------------
#GPIOの指定 お好みの方を選択
GPIO.setmode(GPIO.BCM)   # GPIO番号指定
# GPIO.setmode(GPIO.BOARD)   # ボードピン番号指定

#ピンモード設定
## 出力
gpioOUT = pinOUT.values()
GPIO.setup(gpioOUT, GPIO.OUT)

## 入力
gpioIN = pinIN.values()
GPIO.setup(gpioIN, GPIO.IN)


# -------------------------
#   マクロ定義
# -------------------------
FREQ = 1000	#パルス周波数
PLSWIDTH = 0.001	#1msec
CW = 0
CCW = 1

#CR = (13).to_bytes(1, byteorder = 'big')
#LF = (10).to_bytes(1, byteorder = 'big')

# コマンド #
GET_VAL 	= "GA"	#測定値出力命令
CNG_IDCT 	= "CN"	#インジケータ表示切替
ZERO_SET	= "CR"	#ゼロセット
ERROR_CLR	= "CS"	#エラークリア

# ピン再定義
# 出力
PLS_X = 14	#パルス出力ピン
PLS_Z = 15	#パルス出力ピン

DIR_X =  4	#dir出力ピン
DIR_Z = 17	#dir出力ピン
STP_X = 22	#stop出力ピン
STP_Z = 27	#stop出力ピン
IND01 =  5	#マシン状態表示

# 入力
UP 		=  6
DOWN	= 13
RIGHT	= 19
LEFT	= 26
RDY_X	= 18
RDY_Z	= 23
ALT_X	= 20
ALT_Z	= 21
MD_01	= 24
MD_02	= 25

# -------------------------
#   関数定義	
# -------------------------
#def GetData(header, ch)
def GetData(ch):
	#com = header + str(ch) + "\n\r"	#送信コマンド
	com = GET_VAL + str(ch) + "\r\n"

	return com

def IndicateChange(ch):
	#com = header + str(ch) + "\n\r"	#送信コマンド
	com = CNG_IDCT + str(ch) + "\r\n"

	return com

def ZeroSet(ch):
	#com = header + str(ch) + "\n\r"	#送信コマンド
	com = ZERO_SET + str(ch) + "\r\n"

	return com

def ErrorClear(ch):
	#com = header + str(ch) + "\n\r"	#送信コマンド
	com = ERROR_CLR + str(ch) + "\r\n"

	return com

# -------------------------
#   メインの処理
# -------------------------

#通信自体はできてそう，タイムアウトに引っかかってない．受信かシリアルの設定に問題がありそう


try:#
	#システムの起動待ち時間(念のため(^3^))
	time.sleep(2)
	print "Hellow　my master. I wake up. "

	tag = "Measure value:"

	print msr_serial.getPort()
	print msr_serial.getBaudrate()
	print msr_serial.getByteSize()
	print msr_serial.getParity()
	print msr_serial.getStopbits()
	print msr_serial.getTimeout()
	print msr_serial.__repr__()

	while True:
		#print "Please mode select... "
		#print msr_serial.isOpen()

		#msr_serial.write("CS00\r\n")
		#print "Error cancel ...  CS00\r\n"		
		#value = msr_serial.readline()

		#time.sleep(1.5)

###########################################################
		value_data = ['0'];
		ch = "01"
		value_str = ' ';
		if(msr_serial.writable()):
			msr_serial.write(GetData(ch))
		if(msr_serial.readable()):
			value_ch1 = msr_serial.readline()
			# print value_ch1 
			# print type(value_ch1)
			l_ch1 = list(value_ch1)	#str型のlist型化
			
			# #取得値の判別
			# if(l_ch1[5] == '-'):
			# 	print 'moge'
			# elif(l_ch1[5] == '+'):
			# 	print 'hoge'
			
			# for i in range(len(l_ch1)):#リストの内容全部表示
			# 	print l_ch1[i]
			for i in range(len(l_ch1)-6):#
				value_data.append(l_ch1[i+6])
			# for i in range(len(value_data)):#
			# 	print value_data[i]
			# 	# print type(value_data[i])#str
			for x in value_data:
				value_str += x
			# print value_str
			# print type(value_str)
			# print float(value_str)
			# print type(float(value_str))

			ch01_val = float(value_str)	
			# print ch01_val

			# print datetime.now()#データ取得時間の記録

			#####
			# print 'str型変換1'
			# print .join(value_data)
			# print 'float型変換2'
			# print float(''.join(value_data))
###########################################################
###########################################################
		value_data = ['0'];
		ch = "02"
		value_str = ' ';
		if(msr_serial.writable()):
			msr_serial.write(GetData(ch))
		if(msr_serial.readable()):
			value_ch1 = msr_serial.readline()
			# print value_ch1 
			# print type(value_ch1)
			l_ch1 = list(value_ch1)	#str型のlist型化
			
			# #取得値の判別
			# if(l_ch1[5] == '-'):
			# 	print 'moge'
			# elif(l_ch1[5] == '+'):
			# 	print 'hoge'
			
			# for i in range(len(l_ch1)):#リストの内容全部表示
			# 	print l_ch1[i]
			for i in range(len(l_ch1)-6):#
				value_data.append(l_ch1[i+6])
			# for i in range(len(value_data)):#
			# 	print value_data[i]
			# 	# print type(value_data[i])#str
			for x in value_data:
				value_str += x
			# print value_str
			# print type(value_str)
			# print float(value_str)
			# print type(float(value_str))

			ch02_val = float(value_str)			
			# print ch02_val

			# print datetime.now()#データ取得時間の記録

			#####
			# print 'str型変換1'
			# print .join(value_data)
			# print 'float型変換2'
			# print float(''.join(value_data))
###########################################################
###########################################################
		value_data = ['0'];
		ch = "03"
		value_str = ' ';
		if(msr_serial.writable()):
			msr_serial.write(GetData(ch))
		if(msr_serial.readable()):
			value_ch1 = msr_serial.readline()
			# print value_ch1 
			# print type(value_ch1)
			l_ch1 = list(value_ch1)	#str型のlist型化
			
			#取得値の判別
			# if(l_ch1[5] == '-'):
			# 	print 'moge'
			# elif(l_ch1[5] == '+'):
			# 	print 'hoge'

			# for i in range(len(l_ch1)):#リストの内容全部表示
			# 	print l_ch1[i]
			for i in range(len(l_ch1)-6):#
				value_data.append(l_ch1[i+6])
			# for i in range(len(value_data)):#
			# 	print value_data[i]
			# 	# print type(value_data[i])#str
			for x in value_data:
				value_str += x
			# print value_str
			# print type(value_str)
			# print float(value_str)
			# print type(float(value_str))
	
			ch03_val = float(value_str)		
			# print ch03_val

			# print datetime.now()#データ取得時間の記録

			#####
			# print 'str型変換1'
			# print .join(value_data)
			# print 'float型変換2'
			# print float(''.join(value_data))
###########################################################
###########################################################
		value_data = ['0'];
		ch = "04"
		value_str = ' ';
		if(msr_serial.writable()):
			msr_serial.write(GetData(ch))
		if(msr_serial.readable()):
			value_ch1 = msr_serial.readline()
			# print value_ch1 
			# print type(value_ch1)
			l_ch1 = list(value_ch1)	#str型のlist型化
			
			# #取得値の判別
			# if(l_ch1[5] == '-'):
			# 	print 'moge'
			# elif(l_ch1[5] == '+'):
			# 	print 'hoge'
			
			# for i in range(len(l_ch1)):#リストの内容全部表示
			# 	print l_ch1[i]
			for i in range(len(l_ch1)-6):#
				value_data.append(l_ch1[i+6])
			# for i in range(len(value_data)):#
			# 	print value_data[i]
			# 	# print type(value_data[i])#str
			for x in value_data:
				value_str += x
			# print value_str
			# print type(value_str)
			# print float(value_str)
			# print type(float(value_str))
			
			ch04_val = float(value_str)
			# print ch04_val

			#####
			# print 'str型変換1'
			# print .join(value_data)
			# print 'float型変換2'
			# print float(''.join(value_data))
###########################################################
		print('ch01:{0} ,ch02:{1} ,ch03:{2} ,ch04:{3}'.format(ch01_val, ch02_val, ch03_val, ch04_val))

		# print datetime.now()#データ取得時間の記録

		#print "haha..."
		#GPIO入出力
		# GPIO.output(ピン番号, 1)   # ピンの出力を3.3Vにする
		# GPIO.output(ピン番号, 0)   # ピンの出力を0Vにする
		# GPIO.input(ピン番号)   # ピンの電圧状態読み取る

		# print 表示したいもの	#コンソールへの表示

		# for 変数 in range(範囲):
			# 処理1
			# 処理2

finally:#try処理の例外の場合，終了時
	# GPIO設定をリセット
	GPIO.cleanup()
	
	print "\n"
	print "Closed GPIO port ..."
	msr_serial.close()
	print "Closed USB0 serial port ..."
	print "\n"
