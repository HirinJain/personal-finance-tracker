import pandas as pd
import csv
from datetime import datetime
from enter_data import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt
class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['Date', 'Amount', 'Category', 'Description']
    FORMAT = '%d-%m-%Y'
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    @classmethod
    def add_entry(cls, date, amount, category , description):
        new_entry = {
            'Date': date,
            'Category': category,
            'Amount': amount,
            'Description': description
        }
        with open(cls.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames = cls.COLUMNS)
            writer.writerow(new_entry)
            print("data entered successfully")
    @classmethod
    def get_transactions(cls,start_date,end_date):
        
            df = pd.read_csv(cls.CSV_FILE)
            df['Date'] = pd.to_datetime(df['Date'], format=CSV.FORMAT)
            start_date = datetime.strptime(start_date, CSV.FORMAT)
            end_date = datetime.strptime(end_date, CSV.FORMAT)
            mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
            filtered_df = df.loc[mask]
            if filtered_df.empty:
                print("No transactions found in the specified date range.")
                
            else:
                print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}:")
                print(filtered_df.to_string(
                    index=False, formatters={'Date': lambda x: x.strftime(CSV.FORMAT)}
                ))
            total_income = filtered_df[filtered_df["Category"]=="INCOME"]["Amount"].sum()
            total_expnese = filtered_df[filtered_df["Category"]=="EXPENSE"]["Amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expnese:.2f}")
            print(f"Net saving: ${total_income - total_expnese:.2f}")
            return filtered_df   
def plot_data(df):
    df.set_index('Date', inplace=True)
    income_df = df[df['Category'] == 'INCOME'].resample("D").sum().reindex(df.index, fill_value=0)   
    expense_df = df[df['Category'] == 'EXPENSE'].resample("D").sum().reindex(df.index, fill_value=0)   
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df['Amount'], label='Income', color='green')
    plt.plot(expense_df.index, expense_df['Amount'], label='Expense', color='red')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income and Expense Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
def add():
    CSV.initialize_csv()
    date = get_date("Enter the date (dd-mm-yyyy): ", Allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

            
def main():
    while True:
        print("\nMenu:")
        print("1. Add a new entry")
        print("2. View transactions")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df =  CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot the data? (y/n): ").lower() == 'y':
                plot_data(df)
                
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()  