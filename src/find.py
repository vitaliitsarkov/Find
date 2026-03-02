from src.find_input import FindInput
from src.find_yandex import FindYandex


class Find:

    def __init__(self):
        self._list_res: list[str] = []

    def __repr__(self):
        return "\n".join(self._list_res)

    def main(self) -> list[str]:
        self._list_res = []

        try:
            # получим значение от пользователя
            str_input = FindInput.main()

            # найдем данные в яндекс
            cls_yandex = FindYandex(input=str_input)

            yandex = cls_yandex.main()

            a = 1 / 0

        except Exception as e:
            self._list_res.append(str(e))

        return self._list_res.copy()
