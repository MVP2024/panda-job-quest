import requests
from .base_parser import BaseParser
from logger.logger import setup_logger


class HHParser(BaseParser):
	"""
	Класс для работы с API HeadHunter
	"""

	def __init__(self, file_worker=None):
		"""
		Инициализация парсера HeadHunter

		:param file_worker: Объект для работы с файлами (опционально)
		"""
		super().__init__(file_worker)

		# Настройка логгера
		self.logger = setup_logger(__name__)

		self.url = 'https://api.hh.ru/vacancies'
		self.headers = {'User-Agent': 'HH-User-Agent'}
		self.params = {'text': '', 'page': 0, 'per_page': 100}
		self.vacancies = []

		self.logger.info("Инициализация HH парсера")

	def load_vacancies(self, keyword):
		"""
		Загрузка вакансий по ключевому слову

		:param keyword: Ключевое слово для поиска
		:return: Список вакансий
		"""
		self.logger.info(f"Начало загрузки вакансий по ключевому слову: {keyword}")

		self.params['text'] = keyword
		self.params['page'] = 0  # Сбрасываем страницу перед новым поиском
		self.vacancies = []  # Очищаем список вакансий

		try:
			while self.params.get('page') < 20:  # Ограничиваем количество страниц
				self.logger.debug(f"Загрузка страницы {self.params.get('page')}")

				response = requests.get(self.url, headers=self.headers, params=self.params)
				response.raise_for_status()

				vacancies = response.json()['items']
				self.vacancies.extend(vacancies)

				self.logger.info(f"Загружено вакансий на странице: {len(vacancies)}")

				# Проверка, есть ли еще страницы
				if len(vacancies) == 0:
					self.logger.info("Больше вакансий нет, завершение парсинга")
					break

				self.params['page'] += 1

			# Сохраняем вакансии с помощью file_worker, если он передан
			if self.file_worker:
				self.logger.info(f"Сохранение {len(self.vacancies)} вакансий")
				self.file_worker.save_vacancies(self.vacancies)

			self.logger.info(f"Всего загружено вакансий: {len(self.vacancies)}")
			return self.vacancies


		except requests.RequestException as e:
			error_message = f"Ошибка при загрузке вакансий: {e}"
			print(error_message)  # Явный вывод
			self.logger.error(error_message)
			return []
