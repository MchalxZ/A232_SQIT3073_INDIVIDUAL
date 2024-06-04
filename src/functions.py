import pandas as pd


# verify user if user provides the data that matched with the data in CSV
def verify_user(user_id, password, filename):
    df = pd.read_csv(filename, dtype=str)
    columns = ['IC Number', 'User ID', 'Password', 'Income', 'Tax Relief', 'Tax Payable']
    # determine the columns in the CSV fike
    for column in columns:
        # ignore the invalid columns name
        if column not in df.columns:
            df[column] = None
    user = df[(df['User ID'] == user_id) & (df['Password'] == password)]
    print(user)
    # return true if user is existed
    return not user.empty


# verify the marital status
def verify_marital_status(income, tax_relief):
    # if taxable income <= 35000 then return true
    if income - tax_relief <= 35000:
        return True
    return False


# User with <= RM35000  will be asked their marital status
def confirm_marital_status(income, tax_relief):
    global marital_status
    # if taxable income <= 35000, will ask user the marital status
    if verify_marital_status(income, tax_relief):
        print('Your marital status?')
        print('1 - Single')
        print('2 - Married')
        print('3 - Divorce / Widow')
        marital_status = int(input('Reply: ').strip())
        # check if user has entered between value 1 to 3
        while marital_status > 3 or marital_status < 1:
            print('invalid, enter again!')
            marital_status = int(input('Reply: ').strip())
    # return int value
    return marital_status


# The function is used for calculate the tax
def calculate_tax(income, tax_relief):
    taxable_income = income - tax_relief
    # get the int value from the function and save it in another variable
    marital_status = confirm_marital_status(income, tax_relief)
    # using if-else statement to check for all the condition
    if taxable_income <= 5000:
        return 0
    elif (5000 < taxable_income <= 20000) and (marital_status == 1 or marital_status == 3):
        return (taxable_income - 5000) * 0.01 - 400
    elif 20000 < taxable_income <= 35000 and (marital_status == 1 or marital_status == 3):
        return 150 + (taxable_income - 20000) * 0.03 - 400
    elif (5000 < taxable_income <= 20000) and marital_status == 2:
        return (taxable_income - 5000) * 0.01 - 800
    elif 20000 < taxable_income <= 35000 and marital_status == 2:
        return 150 + (taxable_income - 20000) * 0.03 - 800
    elif 35000 < taxable_income <= 50000:
        return 600 + (taxable_income - 35000) * 0.06
    elif 50000 < taxable_income <= 70000:
        return 1500 + (taxable_income - 50000) * 0.11
    elif 70000 < taxable_income <= 100000:
        return 3700 + (taxable_income - 70000) * 0.19
    elif 100000 < taxable_income <= 400000:
        return 9400 + (taxable_income - 100000) * 0.25
    elif 400000 < taxable_income <= 600000:
        return 84400 + (taxable_income - 400000) * 0.26
    elif 600000 < taxable_income <= 2000000:
        return 136400 + (taxable_income - 600000) * 0.28
    else:
        return 528400 + (taxable_income - 2000000) * 0.3


# The function is used for saving data into CSV files
def save_to_csv(data, filename):
    df = pd.read_csv(filename, dtype=str)
    required_columns = ['IC Number', 'User ID', 'Password', 'Income', 'Tax Relief', 'Tax Payable']
    # checking the columns same as the dataframe read from CSV file
    for column in required_columns:
        if column not in df.columns:
            df[column] = None

    user_index = df[(df['User ID'] == data['User ID']) & (df['Password'] == data['Password'])].index
    # checking is the user exists and return boolean value
    if not user_index.empty:
        # locating user and update the existing user
        index = user_index[0]
        for key in data.keys():
            df.at[index, key] = data[key]
    else:
        # add a new user if user details not found
        new_row = pd.DataFrame([data])
        df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(filename, index=False)


# read the CSV file
def read_from_csv(filename):
    df = pd.read_csv(filename, dtype=str)
    # return the data frame
    return df


# check if user exists and return boolean value
def user_exists(ic_number, filename):
    df = pd.read_csv(filename, dtype=str)
    user = df[df['IC Number'] == ic_number]
    # if user is existing then return true
    if not user.empty:
        return True
    else:
        return False
