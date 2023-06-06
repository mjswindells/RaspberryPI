import os
import face_recognition
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 23
GPIO_ECHO    = 24
GPIO_LED     = 18

GPIO.setup(GPIO_LED,GPIO.OUT)
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
GPIO.output(GPIO_TRIGGER, False)
	
#GPIO.cleanup()

def on_message(client, userdata, message):
	temp = str(message.payload.decode("utf-8"))
	if temp == "1":
		for i in range(10):
			print("start maesure")
			distance = measure()
			print("finish maesure")
			if distance <= 30 :
				print("start picture")
				p = pic()
				print("finish picture")
				if p == "1":
					GPIO.output(GPIO_LED, GPIO.HIGH)
					print("it's me")
					break
				else :
					GPIO.output(GPIO_LED, GPIO.LOW)
					print("who are you")
	elif temp == "stop" :
		GPIO.output(GPIO_LED, GPIO.LOW)
		print("disconnect")
		client.disconnect()
		client.loop_stop()
	else :
		GPIO.output(GPIO_LED, GPIO.LOW)
		print("message : " + temp)
	
def pic():
	os.system("libcamera-still -o temp.jpg -t 1 --width 600 --height 600")
 
	# load your image
	image_to_be_matched = face_recognition.load_image_file("me.jpg")
 
	# encoded the loaded image into a feature vector
	image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]
 
	# load the image
	current_image = face_recognition.load_image_file("temp.jpg")
	# encode the loaded image into a feature vector
	current_image_encoded = face_recognition.face_encodings(current_image)[0]
	# match your image with the image and check if it matches
	result = face_recognition.compare_faces([image_to_be_matched_encoded], current_image_encoded)
	# check if it was a match
	os.system("rm temp.jpg")
	if result[0] == True:
		return "1"
	else:
		return "0"

def measure():
	time.sleep(1)
	GPIO.output(GPIO_TRIGGER, True)
	# 트리거 핀을 TRUE로 설정하여 센서에 트리거 신호를 보냄
	time.sleep(0.00001)
	# 10us 동안 트리거 펄스 송신
	GPIO.output(GPIO_TRIGGER, False)
	# 트리거 핀을 FALSE로 다시 설정

	start = time.time()
	# 초음파 전송이 끝나는 전송시간 저장
	while GPIO.input(GPIO_ECHO)==0:
		start = time.time()
	# 초음파 수신이 완료될 때까지 수신시간
	while GPIO.input(GPIO_ECHO)==1:
		stop = time.time()

	# 에코 핀에 의해 기록된 트리거 신호와 에코 신호간의 시간을 측정

	elapsed = stop-start
	# 음파의 초당 이동속도 (343m)를 이용하여 거리계산
	distance = (elapsed * 34300)/2
	print(distance)

	return distance

try:

	client = mqtt.Client()
	client.on_message = on_message

	client.connect("broker.emqx.io", 1883)
	client.subscribe("topic")

	client.loop_forever()
except KeyboardInterrupt:
	GPIO.cleanup()
