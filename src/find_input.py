import pyinputplus as pyip

class FindInput:
    @staticmethod
    def main():
        response = pyip.inputStr(prompt="Введите песню (например, Марк Котляр путь к нашим сердцам: ")
        return response
