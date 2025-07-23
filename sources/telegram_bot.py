import telegram

class TelegramBot:
    """
    텔레그램 메시지 발송을 담당하는 클래스.
    """
    def __init__(self, token, chat_id):
        if token == None or chat_id == None:
            raise ValueError("텔레그램 봇 토큰과 채팅 ID를 설정해야 합니다.")
        try:
            self.bot = telegram.Bot(token=token)
            self.chat_id = chat_id
        except Exception as e:
            raise ConnectionError(f"텔레그램 봇 초기화 실패: {e}")


    def send_message(self, text):
        """
        지정된 채팅 ID로 메시지를 보냅니다.
        """
        try:
            self.bot.send_message(chat_id=self.chat_id, text=text)
            return True
        except telegram.error.TelegramError as e:
            raise ConnectionError(f"텔레그램 메시지 발송 실패: {e}")
