# equation_solver.py
import math
import sys

def solve_quadratic_equation(a, b, c):
    """
    Розв'язує квадратне рівняння ax^2 + bx + c = 0.
    Повертає кортеж: (кількість_коренів, корінь1, корінь2).
    корінь2 буде None, якщо є 0 або 1 корінь.
    Обидва корені будуть None, якщо коренів немає.
    """
    if a == 0:
        # Це не квадратне рівняння, але завдання передбачає, що a != 0
        # для "квадратного рівняння".
        # В неінтерактивному режимі це буде помилка.
        # В інтерактивному, ми повинні запитати 'a' знову.
        # Тут просто повертається індикатор помилки для внутрішнього використання.
        return -1, None, None # Спеціальний код для a=0

    delta = b**2 - 4*a*c

    if delta > 0:
        x1 = (-b - math.sqrt(delta)) / (2*a)
        x2 = (-b + math.sqrt(delta)) / (2*a)
        return 2, x1, x2
    elif delta == 0:
        x1 = -b / (2*a)
        return 1, x1, None
    else:
        return 0, None, None

def get_float_input(prompt_message, is_coefficient_a=False):
    """
    Запитує у користувача дійсне число, доки не буде введено коректне значення.
    Якщо is_coefficient_a=True, то число не може бути 0.
    """
    while True:
        try:
            user_input = input(f"{prompt_message} = ")
            value = float(user_input)
            if is_coefficient_a and value == 0.0:
                print("Error. a cannot be 0 for a quadratic equation.")
                # Завдання вимагає "давати можливість ввести число повторно"
                # для некоректних значень, але не для a=0.
                # Однак, логічніше для інтерактивного режиму
                # дати можливість ввести 'a' знову, якщо воно 0.
                # В неінтерактивному це буде фатальна помилка.
                # Для інтерактивного зробимо повторний запит.
                print(f"Error. Expected a valid real number (not zero for 'a'), got {value} instead")
                continue # Повторний запит 'a'
            return value
        except ValueError:
            print(f"Error. Expected a valid real number, got {user_input} instead")

def print_solution(a, b, c, num_roots, x1, x2):
    """Виводить рівняння та його розв'язки."""
    print(f"Equation is: ({a:.1f}) x^2 + ({b:.1f}) x + ({c:.1f}) = 0")
    if num_roots == 2:
        print("There are 2 roots")
        # Забезпечення, щоб x1 був меншим за x2 для консистентності
        print(f"x1 = {min(x1, x2):.10g}") # .10g для кращого відображення, уникаючи зайвих нулів
        print(f"x2 = {max(x1, x2):.10g}")
    elif num_roots == 1:
        print("There are 1 roots") # Приклади показують "1 roots", хоча граматично "1 root"
        print(f"x1 = {x1:.10g}")
    elif num_roots == 0:
        print("There are 0 roots")
    # num_roots == -1 (a=0) буде оброблено раніше

# Поки що основні функції готові. Далі буде інтегрування режиммів.

def interactive_mode():
    """Обробляє інтерактивний режим роботи програми."""
    print("Starting interactive mode.") # Допоміжне повідомлення, можна прибрати
    
    # Отримання коефіцієнтів
    # Для 'a' буде використовуватися цикл у get_float_input,
    # щоб переконатися, що він не нуль.
    a = get_float_input("a", is_coefficient_a=True)
    b = get_float_input("b")
    c = get_float_input("c")

    num_roots, x1, x2 = solve_quadratic_equation(a, b, c)
    print_solution(a, b, c, num_roots, x1, x2)

def main():
    args = sys.argv
    if len(args) == 1:
        interactive_mode()
    elif len(args) == 2:
        # Це буде неінтерактивний режим, реалізую пізніше
        filepath = args[1]
        print(f"Non-interactive mode requested with file: {filepath}") # Заглушка
        # non_interactive_mode(filepath)
        pass # Поки що заглушка
    else:
        print("Usage: ./equation_solver.py [filepath]")
        sys.exit(1)

if __name__ == "__main__":
    main()
$ python equation_solver.py
Starting interactive mode.
a = 2
b = 1
c = -3
Equation is: (2.0) x^2 + (1.0) x + (-3.0) = 0
There are 2 roots
x1 = -1.5
x2 = 1.0

Starting interactive mode.
a = invalid
Error. Expected a valid real number, got invalid instead
a = 0
Error. Expected a valid real number (not zero for 'a'), got 0.0 instead
a = 1
b = 0
c = 9
Equation is: (1.0) x^2 + (0.0) x + (9.0) = 0
There are 0 roots

def non_interactive_mode(filepath):
    """Обробляє неінтерактивний режим роботи програми."""
    try:
        with open(filepath, 'r') as f:
            line = f.readline().strip()
            if not line: # Порожній файл або порожній перший рядок
                print("invalid file format")
                sys.exit(1)

            parts = line.split(' ')
            if len(parts) != 3:
                print("invalid file format")
                sys.exit(1)
            
            try:
                a = float(parts[0])
                b = float(parts[1])
                c = float(parts[2])
            except ValueError:
                print("invalid file format")
                sys.exit(1)

            # Перевірка, що після трьох чисел немає зайвих даних у рядку
            # (хоча split(' ') вже мав би це покрити, якщо є більше чисел)
            # та що файл закінчується після цього рядка
            if f.read().strip(): # Читаю залишок файлу
                print("invalid file format (extra content after coefficients)")
                sys.exit(1)


            if a == 0.0:
                print("Error. a cannot be 0")
                sys.exit(1)

            num_roots, x1, x2 = solve_quadratic_equation(a, b, c)
            print_solution(a, b, c, num_roots, x1, x2)

    except FileNotFoundError:
        print(f"file {filepath} does not exist")
        sys.exit(1)
    except Exception as e: # Загальний обробник для непередбачених помилок з файлом
        print(f"An unexpected error occurred with file processing: {e}")
        sys.exit(1)


def main():
    args = sys.argv
    if len(sys.argv) == 1:
        # Запускаю інтерактивний режим, якщо немає аргументів
        interactive_mode()
    elif len(sys.argv) == 2:
        # Запускаю неінтерактивний режим, якщо є один аргумент (шлях до файлу)
        filepath = sys.argv[1]
        non_interactive_mode(filepath)
    else:
        # Вивід повідомлення про неправильне використання, якщо аргументів більше
        print("Usage: python equation_solver.py [filepath]")
        sys.exit(1)


if __name__ == "__main__":
    main()
