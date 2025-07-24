from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time

class NewsCrawler:
    """
    Selenium을 이용한 네이버 뉴스 '단독' 기사 크롤러 (JS 렌더링 대응)
    """
    def __init__(self):
        self.sent_links = set()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        options = Options()
        options.add_argument("--headless")  # 창 안 띄우기
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def crawl(self, search_query="단독"):
        url = f"https://search.naver.com/search.naver?where=news&query={search_query}"
        self.driver.get(url)
        time.sleep(2)  # JS 로딩 기다리기

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        news_items = soup.select("a.news_tit")

        found_articles = []
        for tag in news_items:
            title = tag.get_text(strip=True)
            link = tag.get("href")
            if not title or not link:
                continue
            if "단독" not in title and "특별취재" not in title:
                continue
            if link in self.sent_links:
                continue
            found_articles.append({"title": title, "link": link})
            self.sent_links.add(link)
            self.logger.info(f"[단독] {title} - {link}")
            if len(found_articles) >= 10:
                break

        return found_articles
    
    
if __name__ == "__main__":
    crawler = NewsCrawler()
    articles = crawler.crawl()
    for a in articles:
        print(a['title'], a['link'])