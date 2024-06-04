import pandas as pd

from functions import verify_user, calculate_tax, save_to_csv, user_exists

# declaration of filename,link for tax relief and minimum tax relief
filename = 'user_data.csv'
link = 'https://www.hasil.gov.my/en/individual/individual-life-cycle/how-to-declare-income/tax-reliefs/'
min_tax_relief = '(Min RM 9000)'

# using while loop to check if the program wants to terminate or not
while True:
    print()
    print('Welcome to the Malaysian Tax Calculator Program')
    print('Before this, if you do not know your tax relief claims, take a look at the link below (latest assessment):')
    print(link)
    print()
    # starting by asking if user has an account
    registered = input('Do you have an existing account? (yes/no): ').strip().lower()
    # if not yet register then perform registration
    if registered == 'no':
        user_id = input('Enter your user ID: ').strip()
        ic_number = input('Enter your IC number: ').strip()
        # check if user has entered exactly 12 digit of ic number
        while len(ic_number) != 12:
            ic_number = input('IC number should be 12 digit. Enter your IC number: ').strip()
        # check for existence of the user in CSV file if user details exist then remind user
        if user_exists(ic_number, filename):
            print(f'User with IC number {ic_number} is already registered.')
        else:
            # store in CSV file if user data is not existed
            password = ic_number[8:12]
            user_data = {
                'IC Number': ic_number,
                'User ID': user_id,
                'Password': password,
                'Income': '0',
                'Tax Relief': '0',
                'Tax Payable': '0'
            }
            save_to_csv(user_data, filename)
            print(f'User {user_id} registered successfully.')
    # if user has an account, just need to use last four digit of IC as the password
    elif registered == 'yes':
        user_id = input('Enter your user ID: ').strip()
        password = input('Enter your password (last 4 digits of your IC number): ').strip()
        # if user details found, just enter annual income amount and tax relief amount
        if verify_user(user_id, password, filename):
            income = float(input('Enter your annual income: RM ').strip().replace(',', ''))
            tax_relief = float(
                input('Enter your tax relief amount ' + min_tax_relief + ': RM ').strip().replace(',', ''))
            # check if tax relief is less than 9000, true will need user to insert again
            while tax_relief < 9000:
                print('Invalid tax relief amount, enter again!')
                tax_relief = float(
                    input('Enter your tax relief amount ' + min_tax_relief + ': RM ').strip().replace(',', ''))
            # perform tax calculation using income and tax relief amount
            tax_payable = calculate_tax(income, tax_relief)
            # avoid the negative value stored in CSV file
            if tax_payable < 0:
                tax_payable = 0
            # read files through CSV
            df = pd.read_csv(filename, dtype=str)
            # locating user details and modify the tax_payable amount as well as the annual income and tax relief
            ic_number = df.loc[(df['User ID'] == user_id) & (df['Password'] == password), 'IC Number'].values[0]
            # using dictionaries to store user details
            user_data = {
                'IC Number': ic_number,
                'User ID': user_id,
                'Password': password,
                'Income': income,
                'Tax Relief': tax_relief,
                'Tax Payable': tax_payable
            }
            # perform saving action
            save_to_csv(user_data, filename)
            print(f'Your tax payable is: RM {tax_payable:.2f}')
        else:
            print('User not found or password incorrect.')
    # always checking user input yes or no only, user will need to input again if invalid response entered
    while True:
        response = input('Would you like to continue? (yes/no): ').strip().lower()
        # if response yes meaning will break this while loop and continue the program
        if response == 'yes':
            break
        # if response no meaning will exit the program
        elif response == 'no':
            exit()
        # print invalid message if the response is not yes or no
        else:
            print('Invalid response, enter again.')
