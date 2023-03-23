from __future__ import print_function
#이 문장은 print() 함수를 Python 2.x에서 함수로 사용할 수 있도록 하는 구문입니다.
import time
import RPi.GPIO as GPIO
#Raspberry Pi의 GPIO 핀을 제어하는 함수를 제공

def measure():
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

  return distance

# 측정 오류를 줄이기 위해 세 번의 층정을 통해 평균 계산
def measure_average():
  distance1=measure()
  time.sleep(0.1)
  distance2=measure()
  time.sleep(0.1)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

GPIO.setmode(GPIO.BCM)
# board 모드 대신 BCM 모드 사용
GPIO_TRIGGER = 23
GPIO_ECHO    = 24
GPIO_LED     = 18
# 트리거, 에코, LED 핀 번호 지정
print("Ultrasonic Measurement")

GPIO.setup(GPIO_LED,GPIO.OUT)
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
# 초기 초음파 송신 트리거 핀을 출력으로 지정
GPIO.setup(GPIO_ECHO,GPIO.IN)
# 반사되는 초음파를 수신하는 핀을 입력으로 지정
GPIO.output(GPIO_TRIGGER, False)
# 트리거 펄스 정지

try:

  while True:

    distance = measure_average()
    print("Distance : %.1f" % distance)
    time.sleep(1)

# 10cm 이내에 들어오면 LED ON
    if distance <=10:
      GPIO.output(GPIO_LED, GPIO.HIGH)
      print("LED_ON!!!")
    else :
      print("LED_OFF")
      GPIO.output(GPIO_LED, GPIO.LOW)

except KeyboardInterrupt:
  GPIO.cleanup()