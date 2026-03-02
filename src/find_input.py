import pyinputplus as pyip

class FindInput:
    @staticmethod
    def main():
        response = pyip.inputStr(prompt="Введите название песни: ")
        return response
