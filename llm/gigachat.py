from langchain_gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage
import logging
from config import GIGA_API_KEY


class LLMService:
    def __init__(self, **kwargs):
        """Инициализация LLM сервиса с заданным API ключом."""
        try:
            # Используем новую версию GigaChat
            self.llm = GigaChat(credentials=GIGA_API_KEY, verify_ssl_certs=False, **kwargs)
        except Exception as e:
            logging.error(f"Ошибка инициализации LLM: {e}")
            self.llm = None

    def generate_response(self, system_prompt, user_prompt):
        """Генерирует ответ на основе системного и пользовательского сообщения."""
        if not self.llm:
            logging.error("LLM не был инициализирован.")
            return None

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        try:
            logging.info(f"Переданные сообщения: {messages}")

            response = self.llm.invoke(messages)  # Используем метод `invoke`, а не устаревший `__call__`
            return response.content
        except Exception as e:
            logging.error(f"Ошибка при генерации ответа: {e}")
            return None

