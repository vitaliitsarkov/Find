from src.find_input import FindInput
from src.find_yandex import FindYandex, Item
from src.find_log import ErrorLogger


class Find:

    def __init__(self):
        self._list_res: list[str] = []
        self._list_item: list[Item] = []

    def __repr__(self):
        return "\n".join(self._list_res)

    def main(self) -> list[str]:
        self._list_item = []

        try:
            # получим значение от пользователя
            str_input = FindInput.main()

            # найдем данные в яндекс
            with FindYandex(str_input) as searcher:
                self._list_item = searcher.search()

            # парсинг ответа
            self.main_parse()

            a = 1 / 0

        except Exception as e:
            self._list_res.append(str(e))
            logger = ErrorLogger()
            logger.log_error(e)

        return self._list_res.copy()

    def main_parse(self) -> list[str]:
        self._list_res = []

        for i, item in enumerate(self._list_item, 1):
            print(f"{i}. {item.text}")
            print(f"   URL: {item.url}\n")

        self._list_res.append(f"\nНайдено {len(self._list_item)} новостей")

