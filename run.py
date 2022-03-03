import gspread
from google.oauth2.service_account import Credentials

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

        data_str = input("Enter your data here:\n")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            # This check only validates data. Conversions of data inside,
            # although useful, are not returned. So, math must be done
            # with newly converted data.
            print('Data is valid!')
            break
            # The break ends the while when the user enters valid data
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly  values.
    """
    try:
        [int(value) for value in values]
        # list comprehension: for each individual value in the
        # values  list, convert that value into an integer
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e_e:
        print(f'Invalid data: {e_e}, please try again.\n')
        return False

    return True


def update_worksheet(data, sheet):
    """
    Updates worksheet, add new row with the list data provided.
    """
    print(f"Updating {sheet} worksheet...\n")
    worksheet = SHEET.worksheet(sheet)
    # line above gets access to the worksheet inside the workbook
    worksheet.append_row(data)
    # line above adds a new row in the selected worksheet with data passed in
    print(f'{sheet} worksheet updated successfully.\n')


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

    return [(int(stock) - sales)
            for stock, sales in zip(stock_row, sales_row)]
    # line above calculates surplus for each heading/item,
    # by using a list comprehension. The zip method allows us to iterate 2
    # lists at the same time. The second line is indented to the opening
    # parentheses. Alternative version:
    # 
    # surplus_data = []
    # for stock, sales in zip(stock_row, sales_row):
    #    surplus = int(stock) - sales
    #    surplus_data.append(surplus)
    #
    # return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists
    """

    sales = SHEET.worksheet('sales')
    # column = sales.col_values(3)
    # The line commented-out above gets access to the values
    # of a specific column.

    columns = [sales.col_values(ind)[-5:] for ind in range(1, 7)]
    # The line above set a list comprehension which creates a list of lists:
    # it assigns the last 5 values within the list resulting from
    # sales.col_values(ind), which prints each column values. To select only
    # the last 5 values, we added a slicer [-5:] which stands for
    # "start at index -5 from the right and arrive to the end of the list"
    # the for loop - instead - selects only positive integers for the index
    # which recalls column 1, 2, 3, 4, 5, 6.
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    for column in data:
        # the for loop above selects the lists passed with data
        # it loops column by column and gets its values converted
        # into integers thanks to the list comprehension below
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')


print('Welcome to Love Sandwiches Data Automation')
main()
