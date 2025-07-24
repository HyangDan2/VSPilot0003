
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time

class NewsCrawler:
    """
    Selenium 기반 네이버 뉴스 '단독' 기사 크롤러 (JS 렌더링 대응 + 뉴스 탭 클릭 + 디버깅 저장)
    """
    def __init__(self):
        self.sent_links = set()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        options = Options()
        options.add_argument("--headless")
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
        time.sleep(2)

        # 뉴스 탭 클릭 먼저 시도
        try:
            news_tab = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "뉴스"))
            )
            news_tab.click()
            time.sleep(2)
        except Exception as e:
            self.logger.warning(f"뉴스 탭 클릭 실패 (무시됨): {e}")

        # 렌더링된 페이지 저장 (탭 클릭 후)
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        news_items = soup.select("a.news_title")
        self.logger.info(f"뉴스 기사 수: {len(news_items)}개")

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

    print("🔍 debug_page.html 저장 완료!")
    print("📄 수집된 기사 목록:")

    if not articles:
        print("❌ 단독/특별취재 기사 없음!")
    else:
        for i, a in enumerate(articles, start=1):
            print(f"{i}. {a['title']}")
            print(f"   ↳ {a['link']}")