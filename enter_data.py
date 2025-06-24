from datetime import datetime
CATEGORIES = {
    'I': 'INCOME',
    'E': 'EXPENSE'
}
def get_date(prompt, Allow_default=False):
    date_str = input(prompt)
    if Allow_default and not date_str:
        return datetime.today().strftime('%d-%m-%Y')
    
    try:
        valid_date = datetime.strptime(date_str, '%d-%m-%Y')
        return valid_date.strftime('%d-%m-%Y')
    except ValueError:
        print("Invalid date format. Please use 'dd-mm-yyyy'.")
        return get_date(prompt, Allow_default)
def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        return amount
    except ValueError as e:
        print("Invalid amount")
        return get_amount()
def get_category():
    category = input("Enter the category ( I for INCOME/ E for EXPENSE): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    else:
        print("Invalid category. Please enter 'I' for INCOME or 'E' for EXPENSE.")
        return get_category()
def get_description():
    description = input("Enter a description (optional): ")
    return description if description else "No description provided"
    
