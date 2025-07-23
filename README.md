Tkinter 텔레그램 뉴스봇 (Tkinter Telegram News Bot)
이 애플리케이션은 네이버 뉴스에서 '단독' 키워드가 포함된 기사를 주기적으로 크롤링하여 지정된 텔레그램 채널이나 채팅방으로 링크와 제목을 자동으로 전송하는 GUI 기반 봇입니다.

✨ 주요 기능
GUI 컨트롤러: Tkinter를 활용하여 봇의 모든 동작을 직관적인 그래픽 인터페이스로 손쉽게 제어할 수 있습니다.

▶ Play / Resume: 크롤링 작업을 시작하거나 일시정지된 작업을 다시 시작합니다.

⏸ Pause: 현재 진행 중인 작업을 일시정지합니다.

⏹ Stop: 현재 작업을 완전히 중지합니다.

🔄 Restart: 작업을 중지한 후 다시 시작합니다.

자동 크롤링: apscheduler 라이브러리를 사용해 1분마다 백그라운드에서 자동으로 새로운 '단독' 기사를 확인합니다.

텔레그램 알림: 새로운 기사가 발견되면 즉시 해당 기사의 제목과 링크를 텔레그램으로 발송합니다.

실시간 로그: GUI 화면에서 프로그램의 모든 활동 (크롤링 시작, 기사 발견, 발송 완료, 오류 등)을 실시간으로 확인할 수 있습니다.

객체 지향 설계 (OOP): 크롤러, 텔레그램 봇, 스케줄러 등 각 기능이 독립적인 클래스로 분리되어 있어, 향후 다른 뉴스 사이트를 추가하는 등 기능 확장이 용이합니다.

자동 재시작 가이드: 예기치 않은 오류로 프로그램이 종료될 경우 자동으로 재시작할 수 있는 래퍼 스크립트 (Batch, Shell) 예제를 제공하여 안정적인 운영을 돕습니다.

🛠️ 기술 스택
언어: Python 3

GUI: Tkinter

크롤링: requests, BeautifulSoup4

스케줄링: APScheduler

메시징: python-telegram-bot

⚙️ 설치 및 설정
1. 필수 라이브러리 설치
터미널 또는 명령 프롬프트에서 아래 명령어를 실행하여 필요한 라이브러리를 설치합니다.

pip install tkinter requests beautifulsoup4 python-telegram-bot apscheduler

2. 텔레그램 봇 생성 및 정보 얻기
봇 토큰 (Bot Token) 받기:

텔레그램에서 BotFather를 검색하여 대화를 시작합니다.

/newbot 명령어를 입력하여 새로운 봇을 생성합니다.

BotFather가 알려주는 HTTP API 토큰을 복사합니다. (예: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)

채팅 ID (Chat ID) 확인하기:

메시지를 받을 채널이나 그룹, 또는 개인 채팅방의 ID가 필요합니다.

개인 채팅: @userinfobot에게 메시지를 보내면 자신의 Chat ID를 알려줍니다.

채널/그룹: 생성한 봇을 채널이나 그룹에 추가한 후, 아무 메시지나 보냅니다. 그 다음 웹 브라우저 주소창에 아래 URL을 입력하여 chat 객체 안에 있는 id 값을 확인합니다.

https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

(채널의 경우 @channel_name 형식의 ID도 사용 가능합니다.)

3. 소스 코드 설정
다운로드한 파이썬 스크립트 (tkinter_telebot_pilot.py 또는 main.py)를 열어 아래 두 변수의 값을 자신의 정보로 수정합니다.

# --- 설정 (사용자 환경에 맞게 수정) ---
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # 1번에서 받은 봇 토큰을 여기에 붙여넣기
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"      # 2번에서 확인한 채팅 ID를 여기에 붙여넣기

🚀 실행 방법
터미널에서 아래 명령어를 입력하여 프로그램을 실행합니다.

python tkinter_telebot_pilot.py
# 또는 파일 분리 버전을 사용하는 경우
python main.py

GUI 창이 나타나면 ▶ Play 버튼을 눌러 작업을 시작할 수 있습니다.

🔄 안정적인 운영을 위한 자동 재시작
프로그램이 심각한 오류로 인해 완전히 종료되었을 때 자동으로 재시작하려면, 아래와 같은 래퍼 (Wrapper) 스크립트를 사용하는 것이 가장 안정적입니다.

Windows (.bat 파일)
start.bat이라는 이름으로 아래 내용을 저장합니다.

@echo off
:start
echo "Starting Python application..."
python tkinter_telebot_pilot.py
echo "Application stopped. Restarting in 5 seconds..."
timeout /t 5
goto start

Linux/macOS (.sh 파일)
start.sh이라는 이름으로 아래 내용을 저장합니다.

#!/bin/bash
while true; do
  echo "Starting Python application..."
  python3 tkinter_telebot_pilot.py
  echo "Application stopped. Restarting in 5 seconds..."
  sleep 5
done

위 내용을 각각 start.bat 또는 start.sh 파일로 저장한 뒤, 파이썬 스크립트 대신 이 파일을 실행하면 됩니다.
