from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio

class SchedulerManager:
    def __init__(self, job_function, app_ui):
        self.scheduler = AsyncIOScheduler()
        self.job_function = job_function  # async 함수!
        self.app_ui = app_ui
        self.job = None
        self.state = 'stopped'

    def start(self):
        if self.state == 'stopped':
            try:
                self.job = self.scheduler.add_job(
                    lambda: asyncio.create_task(self.job_function()),
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
        if self.state == 'running' and self.job:
            self.scheduler.pause_job(self.job.id)
            self.state = 'paused'
            self.app_ui.log_message("⏸️ 작업이 일시정지 되었습니다.")

    def resume(self):
        if self.state == 'paused' and self.job:
            self.scheduler.resume_job(self.job.id)
            self.state = 'running'
            self.app_ui.log_message("▶️ 작업이 재개되었습니다.")

    def stop(self):
        if self.state in ['running', 'paused']:
            try:
                self.scheduler.shutdown(wait=False)
                self.scheduler = AsyncIOScheduler()
                self.state = 'stopped'
                self.app_ui.log_message("⏹️ 스케줄러가 중지되었습니다.")
            except Exception as e:
                self.app_ui.log_message(f"❌ 스케줄러 중지 오류: {e}")
