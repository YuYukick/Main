# coding: utf-8

###SerialAndLog
## 4つのセンサからの値の取得が完了 11/27
##　取得したデータのリスト化が完了 11/27
##　取得値の正負判別 11/27
## list型からstr型への変換ができてない，時間の取得ができるようになった 11/27
## list型→str型→float型への変換が完了 11/28
## 開設ポートの確認ができる 12/07
## 書き方汚いけど4ch分の出力値を確認できた 12/08
###SerialComArduinoRasp
## Arduinoからの通信を確認 12/08

####SerialCommunicationSystem
## SerialAndLogとSerialComArduinoRaspの統合 12/08
## SerialAndLogの動作確認済み 12/08
## 出力値の表示を整えた 12/08
## 一応通信はできているがすぐ止まる．通信同士の干渉．バッファオーバー等が考えられる．サブプロセス，通信速度変更などが考えられる 12/08

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

# -------------------------
#   マクロ定義
# -------------------------
FREQ = 1000	#パルス周波数
PLSWIDTH = 0.001	#1msec
CW = 0
CCW = 1
# コマンド #
GET_VAL 	= "GA"	#測定値出力命令
CNG_IDCT 	= "CN"	#インジケータ表示切替
ZERO_SET	= "CR"	#ゼロセット
ERROR_CLR	= "CS"	#エラークリア


# ----------------------------
#   シリアル通信の設定
# ----------------------------
# USB-Serialを使用する場合、ttyUSB0
# GPIOピンを使用する場合、ttyAMA0
msr_serial = serial.Serial('/dev/ttyUSB0', 19200, timeout= 5)
msr_serial.setByteSize(8)
msr_serial.setStopbits(2)
#msr_serial.setParity(0)

# arduino = serial.Serial('/dev/ttyACM0', 9600)
# arduino.setByteSize(8)	#ここ二つ認識されないから保留
# arduino.setStopbits(1)

# ----------------------------
#   GPIO番号の定義(GPIO番号)
# ----------------------------
# GPIOの番号の定義
# 出力
pinOUT = {
	'pls_x'	:	14,
}

# 入力
pinIN = {
	'up'	:	 6,
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

#システムの起動待ち時間
time.sleep(2)

print  "serial port open..."
print  "Measurement tool is "	#使用ポートの表示
print msr_serial.portstr

# print  "Arduino is "	#使用ポートの表示
# print arduino.portstr

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

try:
	#システムの起動待ち時間(念のため)
	time.sleep(2)
	print "Hellow, I wake up. I start measuring..."

	print "Measurement tool port..."
	print msr_serial.getPort()
	print msr_serial.getBaudrate()
	print msr_serial.getByteSize()
	print msr_serial.getParity()
	print msr_serial.getStopbits()
	print msr_serial.getTimeout()
	print msr_serial.__repr__()

	# print "Arduino port..."
	# print arduino.getPort()
	# print arduino.getBaudrate()
	# print arduino.getByteSize()
	# print arduino.getParity()
	# print arduino.getStopbits()
	# print arduino.getTimeout()
	# print arduino.__repr__()

	while True:

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

			#取得値の判別
			if(l_ch1[5] == '-'):
				# print 'moge'
				ch01_val *= -1
			# elif(l_ch1[5] == '+'):
			# 	print 'hoge'

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

			#取得値の判別
			if(l_ch1[5] == '-'):
				# print 'moge'
				ch02_val *= -1

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

			#取得値の判別
			if(l_ch1[5] == '-'):
				# print 'moge'
				ch03_val *= -1

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

			#取得値の判別
			if(l_ch1[5] == '-'):
				# print 'moge'
				ch04_val *= -1

			#####
			# print 'str型変換1'
			# print .join(value_data)
			# print 'float型変換2'
			# print float(''.join(value_data))
###########################################################
		print('ch01:{0:>8.4f} ,ch02:{1:>8.4f} ,ch03:{2:>8.4f} ,ch04:{3:>8.4f}, timestamp:{4}'.format(ch01_val, ch02_val, ch03_val, ch04_val, datetime.now()))

		# print type(datetime.now())#データ取得時間の記録
		# print datetime.now()#データ取得時間の記録

###########################################################
		# if(arduino.writable()):
		# 	arduino.write("ON\n")
		# 	# print "ON\n"
		# 	# value_ch1 = arduino.readline()
		# 	# print value_ch1 
		# 	# print "OFF\n"
		# 	# value_ch1 = arduino.readline()
		# 	# print value_ch1 

		# if(arduino.readable()):
		# 	value_ch1 = arduino.readline()
		# 	print value_ch1 
		# 	# print datetime.now()#データ取得時間の記録
###########################################################
		
		# #バッファクリア
		# msr_serial.reset_input_buffer()
		# arduino.reset_input_buffer()

finally:#try処理の例外の場合，終了時
	# GPIO設定をリセット
	GPIO.cleanup()
	
	print "\nClosed GPIO port ..."
	msr_serial.close()
	print "Closed USB0 serial port ...\n\n"

	# arduino.close()
	# print "Closed ACM0 serial port ...\n"