# pidcontrol 프로젝트 

Ball and Beam 이라는 문제를 2D 물리엔진 pymunk와 그래픽엔진 pygame으로 시각적으로 시뮬레이션합니다.

Ball and Beam은 막대기 위에 공을 굴려 원하는 위치(예를 들어 가운데)로 옮기는 문제입니다. 사람이 하기에도 만만치 않습니다.
pymunk는 공이 중력과 관성에 의해 움직이는 물리현상을 계산하여 현실감을 주고, pygame은 이를 컴퓨터 화면에 그립니다.

PID 제어를 사용하여 공을 원하는 위치에 옮기도록 beam의 각도를 조절합니다. 원하는 위치(Set point)와 현재 공의 위치를 `오차`라고 합니다. 
- P (Proportional)
  - 오차에 비례하여 beam을 얼마나 올리고 내릴건지 정합니다. 
  - 그런데 중력은 2차식으로 작용하기 때문에 비례 제어만으로는 원하는 위치로 공을 옮기기 어렵습니다.
- D (Derivative)
  - 오차의 변화율(미분)에 계수를 곱하여 beam을 움직일 양을 정합니다. 
  - 변화율(공의 속도)이 높으면 set-point를 지나칠 것이기 때문에 beam을 반대로 제어하여 속도를 늦춥니다. 
- I (Integral): 
  - 오차의 누적에 계수를 곱하여 beam을 움직일 양을 정합니다. 
  - 일반적으로 시작부터 모든 값을 누적하기 보다는 일정 구간 (여기서는 1초, 50개)동안의 누적을 사용합니다.
  - 외력에 의해 P와 D로는 목표를 이루지 못할때 힘을 발휘합니다. 
  - 예를 들어 바람, 물살, 장애물 등으로 정상적인 제어로는 목표를 이루지 못할 때, 오차가 누적되어 과도한 행동을 하게 합니다. 

## 실행방법
- Python 최신 버전 설치하기 (버전 3.XX): https://www.python.org/downloads/windows/
- git 설치하기: https://git-scm.com/download/win
- 적당한 위치로 디렉토리 이동 후, 소스코드 다운받기
  - `git clone https://github.com/strongwire2/pidcontrol.git`
  - `cd pidcontrol`
- 가상환경 만들기
  - `python -m venv .venv`
- 가상환경 실행하기
  - `.venv\Scripts\activate`
- 필요한 라이브러리 설치하기
  - `pip install -r requirements.txt`
- PID Control 프로그램 실행하기. 기본 Kp, Ki, Kd 값 사용
  - `python pidcontrol.py`
- 조건을 주어 실행하기
  - `python pidcontrol.py [Kp] [Ki] [Kd] [use_bump]`
  - 예: `python pidcontrol.py 0.3 0 10 False`

## PID Control 키 설명 
- Set Point 설정
  - 왼쪽 화살표: 왼쪽 (200)
  - 아래쪽 화살표: 가운데 (400)
  - 오른쪽 화살표: 오른쪽 (600)

## 변화하는 값 파일로 저장하기
- 다음 명령으로 CSV로 저장 가능함. 엑셀에서 읽어 차트 그릴 수 있음. 
  - `python pidcontrol.py > case1.csv`

## 실행 케이스
- Case 1: P만 사용
  - Kp=0.3, Ki=0, Kd=0
  - `python pidcontrol.py 0.3 0 0`
  - 좌우로 왔다갔다 하지만 오차는 더욱 커져 떨어짐 
- Case 2: P만 사용. Kp를 줄여봄 
  - Kp=0.1, Ki=0, Kd=0
  - `python pidcontrol.py 0.1 0 0`
  - 몇번 더 좌우로 왔다갔다 하지만, 결국 떨어짐. 
  - Case1, 2에서 볼 수 있는 건, 공은 t^2에 비례하여 움직이지만, 액션은 선형이라 맞출수가 없다. 
  - 속도가 빠르면 브레이크 역할을 하는 미분항이 필요하다. 
- Case 3: Kp=0.3, Kd=10
  - Kp=0.3, Ki=0, Kd=10
  - `python pidcontrol.py 0.3 0 10`
  - 몇번 왔다갔다 하지만(over-shoot) 결국엔 잘 멈춘다. 
  - Kd를 더 올리면 더 빨리 멈출 것이다
- Case 4: Kp=0.3, Kd=30
  - Kp=0.3, Ki=0, Kd=30
  - `python pidcontrol.py 0.3 0 30`
  - 오버슛없이 한번에 잘 멈춘다. 
- Case 5: Kp=0.3, Kd=50
  - Kp=0.3, Ki=0, Kd=50
  - `python pidcontrol.py 0.3 0 50`
  - 오버슛없지만 브레이크를 너무 많이 써서 느리다. 
- Case 6: 장애물을 놓아보자. 
  - Kp=0.3, Ki=0, Kd=30, use_bump=True
  - `python pidcontrol.py 0.3 0 30 True`
  - 장애물에 걸려서 진행하지 못한다. 
  - 속도가 0에 가깝고, 위치가 고정되어 항상 같은 각도를 유지해서 넘지 못하는 것.
  - 오차를 누적하면 beam의 각도를 더 높이게 하면 해결될 것이다. 그래서 I항 사용
- Case 7: I항 추가
  - Kp=0.3, Ki=0.01, Kd=30, use_bump=True
  - `python pidcontrol.py 0.3 0.01 30 True`
  - 장애물은 통과하지만, I항 때문에 빔 컨트롤이 과도해 브레이크 더 필요함. 
- Case 8: I항 추가에 속도가 빨라 D항 올림
  - Kp=0.3, Ki=0.01, Kd=60, use_bump=True
  - `python pidcontrol.py 0.3 0.01 60 True`
  - 오버슛 최소화, 장애물 통과 

## 참고자료
- [pymunk Documentation](http://www.pymunk.org/_/downloads/en/stable/pdf/)
- [pymunk Tutorial](https://readthedocs.org/projects/pymunk-tutorial/downloads/pdf/latest/)
- [Slide and Pin Joint Demo Step by Step](https://www.pymunk.org/en/latest/tutorials/SlideAndPinJoint.html)
- [pymunk Basics: Bouncing Ball](https://www.youtube.com/watch?v=nNjRz31-7s0&list=PL_N_kL9gRTm8lh7GxFHh3ym1RXi6I6c50&index=2)
- [Why this Plate never lets the Ball Fall? Ball on Plate PID controller with Arduino](https://www.youtube.com/watch?v=0BDvbljP4Yk)
- [PID Balance+Ball | full explanation & tuning](https://www.youtube.com/watch?v=JFTJ2SS4xyA)
- [Hardware Demo of a Digital PID Controller](https://www.youtube.com/watch?v=fusr9eTceEo)
- [Controlling Self Driving Cars](https://www.youtube.com/watch?v=4Y7zG48uHRo)
- [PID Controller - A Real Example with Animation](https://www.youtube.com/watch?v=7qw7vnTGNsA)
- [넘나 쉬운 게임엔진 pymunk를 소개합니다!](https://www.youtube.com/watch?v=QJsFy2A05X0)
- [파이썬 물리엔진은 어떻게 쓰는걸까?](https://www.youtube.com/watch?v=tF4PctX66ek)
- [Ball and beam: Wikipedia](https://en.wikipedia.org/wiki/Ball_and_beam)
- [DIY Arduino Ball and Beam : PID control](https://www.youtube.com/watch?v=FidxDZ7X6OI)