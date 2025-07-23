import requests
from bs4 import BeautifulSoup

class NewsCrawler:
    """
    뉴스 웹사이트를 크롤링하여 '단독' 기사를 찾아내는 클래스.
    향후 다른 뉴스 사이트를 추가하려면 이 클래스를 상속받아 crawl 메소드만 구현하면 됩니다.
    """
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.sent_links = set() # 이미 보낸 기사 링크를 저장하여 중복 발송 방지

    def crawl(self):
        """
        네이버 뉴스에서 '단독' 키워드로 검색하여 기사 제목과 링크를 반환합니다.
        """
        search_query = "단독"
        url = f"https://search.naver.com/search.naver?where=news&query={search_query}"
        
        found_articles = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status() # 오류 발생 시 예외 처리
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_items = soup.select("div.news_area")

            for item in news_items:
                title_tag = item.select_one("a.news_tit")
                if title_tag and search_query in title_tag.get('title', ''):
                    title = title_tag.get('title')
                    link = title_tag.get('href')

                    if link and link not in self.sent_links:
                        found_articles.append({'title': title, 'link': link})
                        self.sent_links.add(link)
                        
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"네이버 뉴스 크롤링 중 네트워크 오류 발생: {e}")
        except Exception as e:
            raise RuntimeError(f"크롤링 중 예상치 못한 오류 발생: {e}")
            
        return found_articles
