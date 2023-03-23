import RPi.GPIO as GPIO
import time
# RPi.GPIO는ㄴ 라즈베리파이의 GPIO를 사용하게 해주는 모듈
# 해당모듈이 import되어야 사용할 수 있다
# as를 사용하여 소스내에서 GPIO로 이름을 설정

# time 모듈은 딜레이를 주기위해서 import

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
# GPIO는 BCM모드가 있고 BOARD모드가 있습니다
# BCM모드는 GPIO의 핀번호로 핀을 세팅한다
# 예제에서 board로 치면 11번에 LED를 연결했고
# BCM으로 치면 GPIO 17번에 LED를 연결했다

# GPIO.setup(17,GPIO.OUT) : 지정한 핀번호의 입출력모드 지정
# LED를 제어하기 위해선 17번 핀이 출력핀(+)이 되어야 하기 때문에 
# 17번 핀을 출력으로 설정하였

while(True):
    GPIO.output(17,False)
    # false : 즉, 0V
    time.sleep(2) # 2초 지연
    GPIO.output(17,True) # true : 보통 5V 그냥 ON이라고 생각하자
    time.sleep(2)
