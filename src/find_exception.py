class UserError(Exception):

    def __init__(self, message: str, value = None):
        super().__init__(message)
        self.value = value

    def __str__(self):
        base = f"[{self.__class__.__name__}] {self.args[0]}"
        if self.value is not None:
            base += f" | {repr(self.value)}"
        return base

    @classmethod
    def invalid_input(cls, text: str) :
        return cls(message="Некорректный ввод.", value=text)

    @classmethod
    def timeout(cls, time: int = 8) :
        return cls(message=f"Превышено время ожидания: {time}")

    @classmethod
    def tech_error(cls, text: str) :
        return cls(message="Некорректный ввод.", value=text)


# Пример использования
if __name__ == "__main__":

    invalid_input = UserError.invalid_input("qwerty")
    print(f"1. {invalid_input}")

    try:
        raise UserError.invalid_input(text="qwerty")
    except Exception as e:
        print(f"\nИсключение перехвачено: {e}")
        print(f"Тип исключения: {type(e).__name__}")
        print(f"Значение: {str(e)}")

    try:
        raise UserError.timeout(time=10)
    except Exception as e:
        print(f"\nИсключение перехвачено: {e}")
        print(f"Тип исключения: {type(e).__name__}")
        print(f"Значение: {str(e)}")
