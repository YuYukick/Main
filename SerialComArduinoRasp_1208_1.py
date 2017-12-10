# coding: utf-8 

#Go well serial communication

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

# ----------------------------
#   シリアルの設定
# ----------------------------
# USB-Serialを使用する場合、ttyUSB0
# GPIOピンを使用する場合、ttyAMA0
#arduino = serial.Serial('/dev/ttyUSB0', 19200, serial.PARITY_NONE = 0, serial.STOPBITS_ONE = 1, serial.EIGHTBITS = 8, timeout = 10)	#ポートオープン
arduino = serial.Serial('/dev/ttyACM0', 19200)
# arduino.setByteSize(8)
# arduino.setStopbits(1)
# arduino.setParity(0)

#arduino.open()
print  "serial port open..."

# arduino = serial.Serial(
# 				port ='/dev/ttyUSB0',
# 				baundrate = 19200,
# 				parity = serial.PARITY_NONE,
# 				stopbits = serial.STOPBITS_ONE,
# 				bytesize = serial.EIGHTBITS,
# 				timeout=10
# 				)
#arduino = serial.Serial('/dev/ttyAMA0', 19200, timeout=10)
print  arduino.portstr	#使用ポートの表示

# -------------------------
#   メインの処理
# -------------------------
#通信自体はできてそう，タイムアウトに引っかかってない．受信かシリアルの設定に問題がありそう
try:#
	#システムの起動待ち時間(念のため(^3^))
	time.sleep(2)
	print "Hellow　my master. I wake up. "

	tag = "Measure value:"

	# print arduino.getPort()
	# print arduino.getBaudrate()
	# print arduino.getByteSize()
	# print arduino.getParity()
	# print arduino.getStopbits()
	# print arduino.getTimeout()
	# print arduino.__repr__()

	while True:
		#print "Please mode select... "
		#print arduino.isOpen()

		#arduino.write("CS00\r\n")
		#print "Error cancel ...  CS00\r\n"		
		#value = arduino.readline()

		#time.sleep(1.5)

#####

		if(arduino.writable()):
			arduino.write("ON\n")
			print "ON\n"
			value_ch1 = arduino.readline()
			print value_ch1 

		if(arduino.readable()):
			value_ch1 = arduino.readline()
			print value_ch1 
			print datetime.now()#データ取得時間の記録

		# print value_ch1

finally:#try処理の例外の場合，終了時
	# GPIO設定をリセット
	GPIO.cleanup()
	
	print "\n"
	print "Closed GPIO port ..."
	arduino.close()
	print "Closed USB0 serial port ..."
	print "\n"
