import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import sys
import os

# --- 설정 (사용자 환경에 맞게 수정) ---
TELEGRAM_BOT_TOKEN = "8087893994:AAHNutdMob-8HI4yVY6HTBNUCXPDrpVK_t0" 
TELEGRAM_CHAT_ID = "1338893598"

# --- sources 폴더에서 클래스 가져오기 ---
try:
    from sources.news_crawler import NewsCrawler
    from sources.telegram_bot import TelegramBot
    from sources.scheduler_manager import SchedulerManager
except Exception as e:
    print(f"error importing sources: {e}")
    messagebox.showerror("오류", "sources 폴더 또는 필요한 파일이 없습니다. 파일 구조를 확인해주세요.")
    sys.exit()

class App(tk.Tk):
    """
    메인 애플리케이션 GUI 클래스.
    """
    def __init__(self):
        super().__init__()
        self.title("텔레그램 뉴스봇 컨트롤러")
        self.geometry("600x450")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        try:
            # 핵심 컴포넌트 초기화
            self.crawler = NewsCrawler()
            self.bot = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
            self.scheduler_manager = SchedulerManager(self.crawl_and_send, self)
        except (ValueError, ConnectionError) as e:
            messagebox.showerror("초기화 오류", str(e))
            self.destroy()
            return
            
        self.create_widgets()
        self.update_button_states()

    def create_widgets(self):
        """GUI 위젯들을 생성하고 배치합니다."""
        control_frame = tk.Frame(self, pady=10)
        control_frame.pack(fill=tk.X)

        log_frame = tk.Frame(self, padx=10, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.play_button = tk.Button(control_frame, text="▶ Play", command=self.play_action, width=10, bg="#4CAF50", fg="white", font=('Helvetica', 10, 'bold'))
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.pause_button = tk.Button(control_frame, text="⏸ Pause", command=self.pause_action, width=10, bg="#FFC107", fg="white", font=('Helvetica', 10, 'bold'))
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(control_frame, text="⏹ Stop", command=self.stop_action, width=10, bg="#F44336", fg="white", font=('Helvetica', 10, 'bold'))
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.restart_button = tk.Button(control_frame, text="🔄 Restart", command=self.restart_action, width=10, bg="#03A9F4", fg="white", font=('Helvetica', 10, 'bold'))
        self.restart_button.pack(side=tk.LEFT, padx=5, pady=5)

        log_label = tk.Label(log_frame, text="--- 작업 로그 ---", font=('Helvetica', 12, 'bold'))
        log_label.pack(anchor='w')
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state='disabled', font=('Helvetica', 10))
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_message("프로그램 준비 완료. 'Play' 버튼을 눌러 시작하세요.")

    def crawl_and_send(self):
        """크롤링과 텔레그램 전송을 실행하는 메인 작업 함수."""
        self.log_message("🔍 '단독' 뉴스 크롤링 시작...")
        try:
            articles = self.crawler.crawl()
            if articles:
                self.log_message(f"✨ {len(articles)}개의 새 기사 발견!")
                for article in articles:
                    message = f"📰 {article['title']}\n\n🔗 {article['link']}"
                    self.bot.send_message(message)
                    self.log_message(f"  -> 발송 완료: {article['title']}")
                    time.sleep(1)
            else:
                self.log_message("💨 새로운 '단독' 기사가 없습니다.")
        except (ConnectionError, RuntimeError, Exception) as e:
            self.log_message(f"❌ 작업 중 오류 발생: {e}")

    def log_message(self, message):
        """로그 메시지를 스레드에 안전하게 GUI에 표시합니다."""
        def _update_log():
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')
        self.after(0, _update_log)

    def update_button_states(self):
        """스케줄러 상태에 따라 버튼 활성화/비활성화"""
        state = self.scheduler_manager.state
        self.play_button.config(state='normal' if state in ['stopped', 'paused'] else 'disabled')
        self.pause_button.config(state='normal' if state == 'running' else 'disabled')
        self.stop_button.config(state='normal' if state in ['running', 'paused'] else 'disabled')
        if state == 'paused':
            self.play_button.config(text="▶ Resume")
        else:
            self.play_button.config(text="▶ Play")

    def play_action(self):
        self.scheduler_manager.start()
        self.update_button_states()

    def pause_action(self):
        self.scheduler_manager.pause()
        self.update_button_states()

    def stop_action(self):
        self.scheduler_manager.stop()
        self.update_button_states()

    def restart_action(self):
        self.log_message("🔄 시스템 재시작 중...")
        if self.scheduler_manager.state in ['running', 'paused']:
            self.scheduler_manager.stop()
        self.after(500, self.play_action)
        self.update_button_states()

    def on_closing(self):
        if messagebox.askokcancel("종료", "프로그램을 종료하시겠습니까?"):
            self.log_message("프로그램 종료 중...")
            self.scheduler_manager.stop()
            self.destroy()

def main():
    if TELEGRAM_BOT_TOKEN == None or TELEGRAM_CHAT_ID == None:
        messagebox.showerror("설정 오류", "main.py 파일의 TELEGRAM_BOT_TOKEN과 TELEGRAM_CHAT_ID를 설정해야 합니다.")
        return
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
