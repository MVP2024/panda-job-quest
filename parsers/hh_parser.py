import requests
from .base_parser import BaseParser


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
		self.url = 'https://api.hh.ru/vacancies'
		self.headers = {'User-Agent': 'HH-User-Agent'}
		self.params = {'text': '', 'page': 0, 'per_page': 100}
		self.vacancies = []

	def load_vacancies(self, keyword):
		"""
		Загрузка вакансий по ключевому слову

		:param keyword: Ключевое слово для поиска
		:return: Список вакансий
		"""
		self.params['text'] = keyword
		self.params['page'] = 0  # Сбрасываем страницу перед новым поиском
		self.vacancies = []  # Очищаем список вакансий

		try:
			while self.params.get('page') < 20:  # Ограничиваем количество страниц
				response = requests.get(self.url, headers=self.headers, params=self.params)
				response.raise_for_status()

				vacancies = response.json()['items']
				self.vacancies.extend(vacancies)

				# Проверка, есть ли еще страницы
				if len(vacancies) == 0:
					break

				self.params['page'] += 1

			# Сохраняем вакансии с помощью file_worker, если он передан
			if self.file_worker:
				self.file_worker.save_vacancies(self.vacancies)

			return self.vacancies

		except requests.RequestException as e:
			print(f"Ошибка при загрузке вакансий: {e}")
			return []
