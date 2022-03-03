import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SHEET = GSPREAD_CLIENT.open('love_sandwiches')
# line above select and opens the spreadsheet


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. Te loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            # This check only validates data. Conversions of data inside,
            # although useful, are not returned. So, math must be done
            # with newly converted data.
            print('Data is valid!')
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly  values.
    """
    [int(value) for value in values]
    # list comprehension: for each individual value in the
    # values  list, convert that value into an integer
    try:
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e_e:
        print(f'Invalid data: {e_e}, please try again.\n')
        return False

    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet('sales')
    # line above gets access to the worksheet named 'sales' inside the workbook
    sales_worksheet.append_row(data)
    # line above adds a new row in the selected worksheet with data passed in
    print('Sales worksheet updated successfully.\n')


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    # line above gets access to the worksheet named 'stock' inside the workbook
    # and acquires all values in the form of a list of lists
    stock_row = stock[-1]
    # line above gets the last list of values in the stock sheet

    surplus_data = [(int(stock) - sales)
        for stock, sales in zip(stock_row, sales_row)]
    # line above calculates surplus for each heading/item,
    # by using a list comprehension. The zip method allows to iterate 2 lists
    # at the same time
    print(f'Surplus data list is:\n{surplus_data}')


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print('Welcome to Love Sandwiches Data Automation')
main()
