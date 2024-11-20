import csv
from datetime import datetime, timedelta

# для хранения транзакций
TRANSACTION_FILE = 'data/transactions.csv'

# доступныЕ категории
categories = ['Еда', 'Транспорт', 'Развлечения', 'Зарплата', 'Другое']

#словарик
budgets = {}

def add_transaction(category, amount, date=None):

    if date is None:
        date = datetime.today().strftime('%Y-%m-%d')

    with open(TRANSACTION_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])

def get_transactions(start_date=None, end_date=None, category=None):

    transactions = []
    with open(TRANSACTION_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            date, cat, amount = row
            date = datetime.strptime(date, '%Y-%m-%d')
            amount = float(amount)

            if start_date and date < datetime.strptime(start_date, '%Y-%m-%d'):
                continue
            if end_date and date > datetime.strptime(end_date, '%Y-%m-%d'):
                continue
            if category and cat != category:
                continue

            transactions.append((date, cat, amount))

    return transactions

def generate_report(period='month', category=None):

    today = datetime.today()

    if period == 'day':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=7)
        end_date = today
    elif period == 'month':
        start_date = today - timedelta(days=30)
        end_date = today
    elif period == 'year':
        start_date = today - timedelta(days=365)
        end_date = today
    else:
        raise ValueError("Неверный период отчета")

    transactions = get_transactions(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), category)

    report = f"Отчет за период с {start_date.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')}:\n"
    total_income = sum(t[2] for t in transactions if t[2] > 0)
    total_expenses = sum(t[2] for t in transactions if t[2] < 0)

    report += f"Общий доход: {total_income:.2f}\n"
    report += f"Общие расходы: {total_expenses:.2f}\n"
    report += f"Баланс: {total_income + total_expenses:.2f}\n"

    return report

def set_budget(category, limit):

    budgets[category] = limit

def check_budgets():

    today = datetime.today()
    start_date = today - timedelta(days=30)
    end_date = today

    notifications = []

    for category, limit in budgets.items():
        transactions = get_transactions(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), category)
        total_expenses = sum(t[2] for t in transactions if t[2] < 0)

        if total_expenses < -limit:
            notifications.append(f"Превышен бюджет для категории '{category}': {total_expenses:.2f} из {limit:.2f}")

    return "\n".join(notifications)

def add_category(category):

    if category not in categories:
        categories.append(category)

def get_categories():

    return categories

def import_transactions():

    # пример(возвращаем фиктивные данные)
    return [
        ('2023-10-01', 'Еда', -100),
        ('2023-10-02', 'Транспорт', -50),
        ('2023-10-03', 'Зарплата', 1000),
    ]

def main():
    while True:
        print("\nМенеджер личных финансов")
        print("1. Добавить транзакцию")
        print("2. Просмотреть отчет")
        print("3. Установить бюджет")
        print("4. Проверить бюджеты")
        print("5. Добавить категорию")
        print("6. Импортировать транзакции")
        print("7. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            category = input("Введите категорию: ")
            amount = float(input("Введите сумму: "))
            date = input("Введите дату (YYYY-MM-DD, опционально): ")
            add_transaction(category, amount, date)
            print("Транзакция добавлена.")

        elif choice == '2':
            period = input("Введите период (day, week, month, year): ")
            category = input("Введите категорию (опционально): ")
            if category == '':
                category = None
            print(generate_report(period, category))

        elif choice == '3':
            category = input("Введите категорию: ")
            limit = float(input("Введите лимит: "))
            set_budget(category, limit)
            print("Бюджет установлен.")

        elif choice == '4':
            print(check_budgets())

        elif choice == '5':
            category = input("Введите новую категорию: ")
            add_category(category)
            print("Категория добавлена.")

        elif choice == '6':
            transactions = import_transactions()
            for t in transactions:
                add_transaction(t[1], t[2], t[0])
            print("Транзакции импортированы.")

        elif choice == '7':
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()