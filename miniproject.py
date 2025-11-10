import pandas as pd
import os

FILENAME = 'expense_data_1 (1).csv'

def initialize_file():
    if not os.path.exists(FILENAME):
        df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])
        df.to_csv(FILENAME, index=False)

def get_salary():
    while True:
        salary_input = input("Enter your monthly salary: ")
        try:
            salary = float(salary_input)
            if salary > 0:
                return salary
            else:
                print("Salary must be positive.")
        except ValueError:
            print("Please enter a valid number.")

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    amount_input = input("Enter amount: ")
    try:
        amount = float(amount_input)
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return
    category = input("Enter category: ")
    description = input("Enter description (optional): ")
    df = pd.read_csv(FILENAME)
    new_row = {'Date': date, 'Amount': amount, 'Category': category, 'Description': description}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FILENAME, index=False)
    print(f"Added amount: {amount:.2f}")
    total_amount = df["Amount"].sum()
    print(f"Total amount of all expenses: {total_amount:.2f}")
    if total_amount > monthly_salary:
        print("WARNING: Your total expenses have exceeded your monthly salary!")

def view_expenses():
    df = pd.read_csv(FILENAME)
    if df.empty:
        print("No expenses found.")
    else:
        print(df)

def delete_expense():
    df = pd.read_csv(FILENAME)
    if df.empty:
        print("No expenses to delete.")
        return
    print(df)
    try:
        idx = int(input("Enter the index of the expense to delete (starting from 0): "))
        if 0 <= idx < len(df):
            df = df.drop(df.index[idx])
            df.to_csv(FILENAME, index=False)
            print("Expense deleted.")
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input. Please enter a valid numeric index.")

def app_menu():
    global monthly_salary
    initialize_file()
    monthly_salary = get_salary()
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Delete an expense")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter again.")

app_menu()