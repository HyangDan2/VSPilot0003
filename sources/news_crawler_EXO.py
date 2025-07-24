import requests
from bs4 import BeautifulSoup
import re
import logging

class NewsCrawler:
    """
    뉴스 웹사이트를 크롤링하여 '단독' 기사를 찾아내는 클래스.
    향후 다른 뉴스 사이트를 추가하려면 이 클래스를 상속받아 crawl 메소드만 구현하면 됩니다.
    """
    def __init__(self):
        # User-Agent를 실제 브라우저 값으로 변경 (크록링 제한 회피)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.naver.com'
        }
        self.sent_links = set() # 이미 보낸 기사 링크를 저장하여 중복 발송 방지
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def crawl(self, search_query="단독"):
        """
        네이버 뉴스에서 '단독' 키워드로 검색하여 기사 제목과 링크를 반환합니다.
        """
        # 검색 결과 URL
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={search_query}"

        found_articles =[]
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            self.logger.info(f"Request to {url} - Status code: {response.status_code}")
            if response.status_code!= 200:
                raise Exception(f"HTTP status code {response.status_code} from Naver")

            soup = BeautifulSoup(response.text, 'html.parser')

            # 네이버 뉴스 검색 결과의 HTML 구조 변경에 따른 수정된 CSS 선택자
            # 최신 구조는 <ul class="type01"> 내 <li> 태그에 뉴스가 포함됨
            news_items = soup.select("ul.type01 > li")

            for item in news_items:
                # 제목과 링크를 가지고 있는 <a> 태그를 선택합니다.
                title_tag = item.select_one("a._sp_each_title")

                if not title_tag:
                   self.logger.debug(f"No title tag found in item")
                   continue

                # '단독' 키워드 또는 관련 패턴(예: [단독]) 포함 여부 확인
                title_str = title_tag.get_text(strip=True)
                search_pattern = re.compile(rf"\b{re.escape(search_query)}\b", re.IGNORECASE)
                is_relevant = bool(search_pattern.search(title_str)) or "[단독]" in title_str or "[특별취재]" in title_str

                if not is_relevant:
                   self.logger.debug(f"Title not relevant: {title_str}")
                   continue

                # 링크 추출
                link = title_tag.get('href')
                if not link:
                   self.logger.debug(f"No link found for title: {title_str}")
                   continue

                # 상대 링크를 절대 링크로 변환
                if not link.startswith("http"):
                   link = f"https://news.naver.com{link}"

                # 중복 체크
                if link in self.sent_links:
                   self.logger.debug(f"Duplicate link found: {link}")
                   continue

                # 기사 정보 저장
                found_articles.append({'title': title_str, 'link': link})
                self.sent_links.add(link)
                self.logger.info(f"Found article: {title_str} - {link}")

                # 10개 이상 크롤링한 경우 중간에 중단 (네이버 크롤링 제한 회피)
                if len(found_articles) >= 10:
                   self.logger.info("Reached maximum articles per page, stopping")
                   break

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Naver news crawling failed - Network error: {e}")
            raise ConnectionError(f"네이버 뉴스 크롤링 중 네트워크 오류 발생: {e}")
        except Exception as e:
            self.logger.error(f"Naver news crawling failed - Unexpected error: {str(e)}", exc_info=True)
            raise RuntimeError(f"크롤링 중 예상치 못한 오류 발생: {e}")

        return found_articles