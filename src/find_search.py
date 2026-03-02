import re
from typing import NamedTuple,List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException, JavascriptException
from src.find_exception import UserError
import src.find_constants as const


class Item(NamedTuple):
    url: str
    text: str


class FindYandex:

    def __init__(self, str_query: str) -> None:

        if not str_query or not isinstance(str_query, str) or len(str_query.strip()) == 0:
            raise UserError.invalid_input(text="Поисковый запрос не может быть пустым")

        if not re.search(r'[a-zA-Zа-яА-Я]', str_query):
            raise UserError.invalid_input(text="Поисковый запрос должен содержать хотя бы одну букву")

        self.query = str_query.strip()
        self.d_driver = None
        self._setup_d_driver()

    def _setup_d_driver(self) -> None:
        """Настройка и инициализация веб-драйвера в фоновом режиме"""
        cls_chrome_options = Options()
        cls_chrome_options.add_argument("--headless=new")  # Новый headless-режим
        cls_chrome_options.add_argument("--disable-gpu")
        cls_chrome_options.add_argument("--no-sandbox")
        cls_chrome_options.add_argument("--disable-dev-shm-usage")
        cls_chrome_options.add_argument("--window-size=1920,1080")
        cls_chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Маскировка под обычного пользователя
        cls_chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        cls_chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        cls_chrome_options.add_experimental_option("useAutomationExtension", False)

        try:
            self.d_driver = webdriver.Chrome(options=cls_chrome_options)
            # Скрыть признак автоматизации после запуска
            self.d_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })
        except WebDriverException:
            raise UserError.tech_error(text=str(e))

    def search(self, timeout: int = 15, max_results: int = const.INT_MAX_RESULTS) -> List[Item]:

        try:
            # Открываем главную страницу Яндекса
            self.d_driver.get(const.STR_SEARCH)

            # Ожидаем загрузки поисковой формы
            cls_search_box = WebDriverWait(self.d_driver, timeout).until(
                ec.presence_of_element_located((By.NAME, "text"))
            )

            # Вводим запрос и отправляем форму
            cls_search_box.clear()
            cls_search_box.send_keys(self.query)
            cls_search_box.send_keys(Keys.ENTER)

            # Ожидаем появления результатов поиска
            WebDriverWait(self.d_driver, timeout).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "li.serp-item"))
            )

            # Вариант 1: Ожидание полного состояния документа
            if not self._wait_for_page_load(timeout=timeout):
                # Если document.readyState не достиг 'complete', попробуем другой подход
                # Вариант 2: Ожидание появления специфичного элемента, который появляется только после полной загрузки
                if not self._wait_for_specific_element("div.serp-list", timeout=timeout):
                    # Если и это не сработало, попробуем подождать появления конкретных элементов результатов
                    if not self._wait_for_specific_element("li.serp-item a[href]", timeout=timeout):
                        raise UserError.timeout(time=timeout)

            # Находим все элементы с результатами поиска
            list_result_items = self.d_driver.find_elements(By.CSS_SELECTOR, "li.serp-item")

            # Ограничиваем количество проверяемых результатов
            list_result_items = list_result_items[:max_results]

            # Регулярное выражение для поиска слов "с"
            str_pattern = re.compile(r'\b(слушать)\b', re.IGNORECASE)

            list_news_items: List[Item] = []

            for item in list_result_items:
                try:
                    # Ищем ссылку в элементе результата
                    link = item.find_element(By.CSS_SELECTOR, "a[href]")
                    url = link.get_attribute("href")
                    text = link.text.strip()

                    # Пропускаем пустые тексты
                    if not text:
                        continue

                    # Проверяем, содержит ли текст слова "новость" или "новости"
                    if str_pattern.search(text):
                        list_news_items.append(Item(url=url, text=text))

                except WebDriverException, AttributeError:
                    # Игнорируем ошибки при обработке отдельного элемента
                    continue

            return list_news_items

        except TimeoutException:
            raise UserError.timeout(time=timeout)
        except WebDriverException as ew:
            raise UserError.tech_error(text=str(ew))

    def close(self) -> None:
        """Закрывает веб-драйвер и освобождает ресурсы"""
        if self.d_driver:
            try:
                self.d_driver.quit()
                self.d_driver = None
            except WebDriverException:
                # Игнорируем ошибки при закрытии
                pass

    def _wait_for_page_load(self, timeout: int = 10) -> bool:

        try:
            WebDriverWait(self.d_driver, timeout).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            return True
        except (TimeoutException, JavascriptException):
            return False

    def _wait_for_specific_element(self, css_selector: str, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.d_driver, timeout).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except TimeoutException:
            return False

    def __enter__(self) -> 'FindYandex':
        """Поддержка контекстного менеджера"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Автоматическое закрытие драйвера при выходе из контекста"""
        self.close()



