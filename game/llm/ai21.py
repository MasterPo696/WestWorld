import requests
import logging
from config import AI21_API_KEY



import logging
from ai21 import AI21Client
from config import AI21_API_KEY
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_ai21.chat_models import ChatAI21

class LLMServiceAI21:
    def __init__(self):
        """Инициализация AI21 модели."""
        try:
            self.parser = StrOutputParser()
            self.model = ChatAI21(model="jamba-instruct", api_key=AI21_API_KEY, streaming=True)
        except Exception as e:
            logging.error(f"Ошибка инициализации AI21: {e}")
            self.model = None

    def generate_response(self, system_message, user_message):
        """Генерирует ответ на основе системного и пользовательского сообщения."""
        if not self.model:
            logging.error("Модель AI21 не инициализирована.")
            return None
        
        try:
            messages = [
                SystemMessage(content=system_message),
                HumanMessage(content=user_message)
            ]
            response = self.model.invoke(messages)
            return self.parser.invoke(response)
        except Exception as e:
            logging.error(f"Ошибка при генерации ответа AI21: {e}")
            return "[Ошибка: Не удалось получить ответ от ИИ.]"






# class LLMService:
#     def __init__(self, api_key=None):
#         """Инициализация LLM сервиса AI21."""
#         self.api_key = api_key or AI21_API_KEY
#         self.endpoint = "https://api.ai21.com/studio/v1/j2-ultra/complete"  # AI21 Endpoint для Jurassic-2 Ultra

#     def generate_response(self, system_prompt, user_prompt):
#         """
#         Генерирует ответ на основе системного и пользовательского сообщения.
#         AI21 требует единого промпта, объединяем system_prompt и user_prompt.
#         """
#         if not self.api_key:
#             logging.error("API ключ не указан.")
#             return None

#         prompt = f"{system_prompt}\n\n{user_prompt}"

#         payload = {
#             "prompt": prompt,
#             "maxTokens": 200,  # Ограничение на длину ответа
#             "temperature": 0.7,  # Креативность
#             "topP": 0.95,
#             "stopSequences": ["\n"]
#         }

#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json"
#         }

#         try:
#             logging.info(f"Отправка запроса к AI21 с промптом: {prompt}")

#             response = requests.post(self.endpoint, json=payload, headers=headers)
#             response.raise_for_status()  # Вызывает исключение для кода ответа != 200

#             response_data = response.json()
#             return response_data.get("completions", [{}])[0].get("data", {}).get("text", "").strip()
#         except Exception as e:
#             logging.error(f"Ошибка при генерации ответа: {e}")
#             return None
