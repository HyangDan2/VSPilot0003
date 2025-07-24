import requests
from bs4 import BeautifulSoup
import logging

class DaumNewsCrawler:
    def __init__(self):
        self.sent_links = set()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36"
        }

    def crawl(self, search_query="단독"):
        url = f"https://search.daum.net/search?w=news&q={search_query}"
        found_articles = []

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            self.logger.info(f"Request to {url} - Status code: {response.status_code}")
            soup = BeautifulSoup(response.text, "html.parser")

            news_links = soup.select("a.c-item-content__headline")

            for a_tag in news_links:
                title = a_tag.get_text(strip=True)
                link = a_tag.get("href")

                if not title or not link:
                    continue
                if "단독" not in title:
                    continue
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

# 테스트
if __name__ == "__main__":
    crawler = DaumNewsCrawler()
    articles = crawler.crawl()
    if not articles:
        print("❌ 단독 기사 없음")
    else:
        for i, a in enumerate(articles, 1):
            print(f"{i}. {a['title']}")
            print(f"   ↳ {a['link']}")
