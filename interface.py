from core import register, auth, create_category, show_categories, show_transactions, add_transaction, calculate_transactions

INTERFACE : str = """
    0. Выйти
    1. Зарегестрироваться
    2. Авторизироваться
    3. Категории
    4. Доходы/Расходы
"""
INTERFACE_CATEGORIES : str = """
    0. Назад
    1. Показать категории
    2. Добавить категорию
"""
INTERFACE_TRANSACTIONS : str = """
    0. Назад
    1. Показать все записи
    2. Посчитать разницу доходов и расходов
    3. Добавить новую запись
"""
is_auth : bool = False
while True:
    print(INTERFACE)
    user_input : str = input("Введите пункт => ")
    if user_input == "0":
        break
    elif user_input == "1":
        login : str = input("Введите логин: ")
        password : str = input("Введите пароль: ")
        try:
            register(login, password)
            is_auth = True
        except:
            print("Пользователь уже существует")
    elif user_input == "2":
        login : str = input("Введите логин: ")
        password : str = input("Введите пароль: ")
        try:
            auth(login, password)
            is_auth = True
        except:
            print("Пользователь не существует")
    elif user_input == "3":
        if is_auth:
            while user_input != "0":
                print(INTERFACE_CATEGORIES)
                user_input : str = input("Введите пункт => ")
                if user_input == "0":
                    break
                elif user_input == "1":
                    categories = show_categories()
                    print("Категории: ")
                    for category in categories:
                        print(f"{category[0]}: {category[1].capitalize()}")
                elif user_input == "2":
                    title : str = input("Введите название категории: ")
                    create_category(title=title)
                    print("Категория создана успешно")
                else:
                    print("Неверный ввод")
        else:
            print("Вы не авторизованы")
    elif user_input == "4":
        if is_auth:
            while user_input != "0":
                print(INTERFACE_TRANSACTIONS)
                user_input : str = input("Введите пункт => ")
                if user_input == "0":
                    break
                elif user_input == "1":
                    transactions = show_transactions(username=login)
                    for transaction in transactions:
                        print(f"\n{transaction[2]}\nКатегория: {transaction[1]}\nСумма: {transaction[4]}\nДоход?: {transaction[5]}\nДата: {transaction[7]}\n")
                elif user_input == "2":
                    category = input("Укажите категорию. Оставьте пустым, чтобы посчитать все вместе: ")
                    if category == "" or category.isspace():
                        category = ""
                        print_head = "Ваш общий учет: "
                    elif category.lower() in [item[1].lower() for item in show_categories()]:
                        print_head = f"Ваш учет по категории {category}: "
                        category = f" AND categories.title = '{category}'"
                    else:
                        print("Некорректный ввод. Такой категории не существует, но вы можете ее добавить")
                        continue
                    [income, outgoings] = calculate_transactions(username=login, category=category)
                    print(f"\n{print_head}\nДоход: {income}\nРасход: {outgoings}\nПрофит: {income-outgoings}\n")
                elif user_input == "3":
                    print("Чтобы добавить запись введите данные:")
                    while user_input.lower() != "н":
                        category : str = input("Категория: ")
                        if not category.lower() in [item[1].lower() for item in show_categories()]:
                            print("Некорректный ввод. Такой категории не существует, но вы можете ее добавить")
                            break
                        is_income : str = input("Направление (доход/д или расход/р): ")
                        if is_income.lower() in ["доход", "д"]:
                            is_income = True
                        elif is_income.lower() in ["расход", "р"]:
                            is_income = False
                        else:
                            print("Некорректный ввод. Направление может быть только 'доход' или 'расход'")
                            break
                        try:
                            amount : float = float(input("Сумма в тенге (только число): "))
                        except:
                            print("Некорректный ввод. Сумма может быть только числом")
                            break
                        add_transaction(username=login, amount=amount, is_income=is_income, category=category)
                        user_input = input("Запись успешно добавлена. Добавить еще? (д/н): ")
        else:
            print("Вы не авторизованы")
    else:
        print("Неверный ввод")


# 1. Добавьте возможность выводить все категории.
# 2. Добавьте возможность добавлять доходы/расходы.
# 3. Добавьте возможность выводить доходы/расходы.

# *4. Возможнсть получить сумму трат или доходов
# в какой-то категории на выбор пользователя.
