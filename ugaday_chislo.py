import random
import json
import os
from datetime import datetime


class NumberGuessingGame:
    def __init__(self):
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = 10
        self.min_range = 1
        self.max_range = 100
        self.stats = []
        self.save_file = "game_save.json"

    def show_instructions(self):
        print("\n=== Игра 'Угадай число' ===")
        print(f"Я загадал число от {self.min_range} до {self.max_range}.")
        print(f"У вас есть {self.max_attempts} попыток, чтобы угадать его.")
        print("После каждой попытки я скажу, больше или меньше ваше число.")
        print("Для выхода введите 'выход'")
        print("Для подсказки введите 'подсказка'\n")

    def generate_number(self):
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0

    def get_input(self):
        while True:
            user_input = input(f"Попытка {self.attempts + 1}. Ваше число: ").strip().lower()

            if user_input == 'выход':
                return None
            elif user_input == 'подсказка':
                self.give_hint()
                continue

            try:
                number = int(user_input)
                if number < self.min_range or number > self.max_range:
                    print(f"Число должно быть от {self.min_range} до {self.max_range}!")
                    continue
                return number
            except ValueError:
                print("Пожалуйста, введите целое число или 'выход'!")
                continue

    def give_hint(self):
        if self.attempts == 0:
            print("Сделайте хотя бы одну попытку!")
            return

        hint_range = max(10, (self.max_range - self.min_range) // 10)
        min_hint = max(self.min_range, self.secret_number - hint_range)
        max_hint = min(self.max_range, self.secret_number + hint_range)
        print(f"Подсказка: число между {min_hint} и {max_hint}")

    def check_guess(self, guess):
        self.attempts += 1

        if guess == self.secret_number:
            print(f"\nПоздравляю! Вы угадали число {self.secret_number} за {self.attempts} попыток!")
            self.save_stats(success=True)
            return True
        elif guess < self.secret_number:
            print("Загаданное число больше!")
        else:
            print("Загаданное число меньше!")

        if self.attempts >= self.max_attempts:
            print(f"\nК сожалению, вы исчерпали все попытки. Загаданное число было {self.secret_number}.")
            self.save_stats(success=False)
            return True

        return False

    def save_stats(self, success):
        record = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'number': self.secret_number,
            'attempts': self.attempts,
            'success': success,
            'range': f"{self.min_range}-{self.max_range}"
        }
        self.stats.append(record)

    def save_game(self):
        game_data = {
            'secret_number': self.secret_number,
            'attempts': self.attempts,
            'stats': self.stats
        }
        with open(self.save_file, 'w') as f:
            json.dump(game_data, f)
        print("Игра сохранена!")

    def load_game(self):
        if not os.path.exists(self.save_file):
            return False

        with open(self.save_file, 'r') as f:
            game_data = json.load(f)

        self.secret_number = game_data['secret_number']
        self.attempts = game_data['attempts']
        self.stats = game_data['stats']
        print("Игра загружена!")
        return True

    def show_stats(self):
        if not self.stats:
            print("Статистика пока отсутствует.")
            return

        print("\n=== Статистика игр ===")
        for i, record in enumerate(self.stats, 1):
            result = "Успех" if record['success'] else "Неудача"
            print(
                f"{i}. {record['date']} - Число: {record['number']}, Попыток: {record['attempts']}, {result}, Диапазон: {record['range']}")

    def ask_replay(self):
        while True:
            answer = input("\nХотите сыграть еще раз? (да/нет): ").strip().lower()
            if answer in ('да', 'д', 'yes', 'y'):
                return True
            elif answer in ('нет', 'н', 'no', 'n'):
                return False
            else:
                print("Пожалуйста, введите 'да' или 'нет'.")

    def run(self):
        print("Добро пожаловать в игру 'Угадай число'!")

        if os.path.exists(self.save_file):
            load = input("Обнаружено сохранение. Загрузить? (да/нет): ").strip().lower()
            if load in ('да', 'д', 'yes', 'y'):
                if not self.load_game():
                    print("Не удалось загрузить сохранение. Начинаем новую игру.")
                    self.generate_number()
        else:
            self.generate_number()

        game_active = True
        while game_active:
            self.show_instructions()
            game_completed = False

            while not game_completed:
                guess = self.get_input()

                if guess is None:
                    save = input("Хотите сохранить игру перед выходом? (да/нет): ").strip().lower()
                    if save in ('да', 'д', 'yes', 'y'):
                        self.save_game()
                    game_active = False
                    break

                game_completed = self.check_guess(guess)

            if game_active:
                self.show_stats()
                game_active = self.ask_replay()
                if game_active:
                    self.generate_number()

        print("\nСпасибо за игру! До свидания!")


if __name__ == "__main__":
    game = NumberGuessingGame()
    game.run()
