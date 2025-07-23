from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

class SchedulerManager:
    """
    APScheduler를 관리하여 주기적인 작업을 처리하는 클래스.
    GUI의 Play, Pause, Stop 버튼과 연동됩니다.
    """
    def __init__(self, job_function, app_ui):
        self.scheduler = BackgroundScheduler(daemon=True)
        self.job_function = job_function
        self.app_ui = app_ui
        self.job = None
        self.state = 'stopped' # 'running', 'paused', 'stopped'

    def start(self):
        """스케줄러를 시작하고 1분마다 작업을 실행합니다."""
        if self.state == 'stopped':
            try:
                self.job = self.scheduler.add_job(
                    self.job_function,
                    trigger=IntervalTrigger(minutes=1),
                    id='news_crawl_job',
                    name='뉴스 크롤링 및 발송 작업',
                    replace_existing=True
                )
                self.scheduler.start()
                self.state = 'running'
                self.app_ui.log_message("✅ 스케줄러 시작됨. 1분마다 뉴스를 확인합니다.")
            except Exception as e:
                self.app_ui.log_message(f"❌ 스케줄러 시작 오류: {e}")
        elif self.state == 'paused':
            self.resume()

    def pause(self):
        """실행 중인 작업을 일시정지합니다."""
        if self.state == 'running' and self.job:
            self.scheduler.pause_job(self.job.id)
            self.state = 'paused'
            self.app_ui.log_message("⏸️ 작업이 일시정지 되었습니다.")

    def resume(self):
        """일시정지된 작업을 재개합니다."""
        if self.state == 'paused' and self.job:
            self.scheduler.resume_job(self.job.id)
            self.state = 'running'
            self.app_ui.log_message("▶️ 작업이 재개되었습니다.")

    def stop(self):
        """스케줄러를 완전히 중지합니다."""
        if self.state in ['running', 'paused']:
            try:
                self.scheduler.shutdown(wait=False)
                self.scheduler = BackgroundScheduler(daemon=True)
                self.state = 'stopped'
                self.app_ui.log_message("⏹️ 스케줄러가 중지되었습니다.")
            except Exception as e:
                self.app_ui.log_message(f"❌ 스케줄러 중지 오류: {e}")
