
import requests
from bs4 import BeautifulSoup
import logging

class NaverMainNewsCrawler:
    """
    네이버 메인 뉴스 페이지에서 '단독' 키워드를 포함한 기사를 수집하는 크롤러.
    검색을 사용하지 않고 메인 뉴스 페이지에서 직접 수집합니다.
    """

    def __init__(self):
        self.sent_links = set()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36"
        }

    def crawl(self):
        url = "https://news.naver.com/"
        found_articles = []

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            self.logger.info(f"Request to {url} - Status code: {response.status_code}")
            if response.status_code != 200:
                raise Exception("네이버 메인 뉴스 응답 오류")

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.select("a")

            for a in links:
                title = a.get_text(strip=True)
                link = a.get("href")

                if not title or not link:
                    continue
                if "단독" not in title:
                    continue
                if not link.startswith("http"):
                    link = "https://news.naver.com" + link
                if link in self.sent_links:
                    continue

                found_articles.append({"title": title, "link": link})
                self.sent_links.add(link)
                self.logger.info(f"[단독] {title} - {link}")

                if len(found_articles) >= 10:
                    break

        except Exception as e:
            self.logger.error(f"크롤링 중 오류: {e}")
            raise

        return found_articles

if __name__ == "__main__":
    crawler = NaverMainNewsCrawler()
    articles = crawler.crawl()
    if not articles:
        print("❌ 단독 기사 없음")
    else:
        for i, a in enumerate(articles, 1):
            print(f"{i}. {a['title']}")
            print(f"   ↳ {a['link']}")
