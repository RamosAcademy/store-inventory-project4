from models import (Base, session, Product, engine)
import csv
import datetime
import time


def menu():
    while True:
        print('''
        \nINVENTORY
        \rPress 't' to view all products
        \rPress 'v' to view a product
        \rPress 'a' to add a product
        \rPress 'b' to backup your database (.csv)
        \rPress 'q' to exit''')
        choice = input('What would you like to do? ')
        if choice.lower() in ['v', 'a', 'b', 'q', 't']:
            return choice
        else:
            input('''
            \rPlease choose one of the options above.
            \rEnter v, a, b, t, or q.
            \rPress Enter to try again.''')


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
        \n *** DATE ERROR ***
        \r The date format should include a valid Month/Day/Year.
        \rEx. 6/8/2018
        \rPress Enter to try again.
        \r*******************''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        price_in_pennies = int(float(price_str.split('$')[1]) * 100)
    except ValueError:
        input('''
        \n*** PRICE ERROR ***
        \rThe price should be a number without a currency symbol.
        \rEx. 10.99
        \rPress Enter to try again.
        \r*******************''')
        return
    return price_in_pennies


def clean_qty(qty_str):
    try:
        quantity = int(qty_str)
    except ValueError:
        input('''
        \n*** QUANTITY ERROR ***
        \rThe quantity should be an intiger.
        \rEx. 25
        \rPress Enter to try again.
        \r*******************''')
        return
    return quantity


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)  # handle for first row being a header https://www.adamsmith.haus/python/answers/how-to-skip-the-first-line-of-a-csv-file-in-python
        for row in data:
            product_in_db = session.query(Product).filter(
                Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = row[2]
                date_updated = clean_date(row[3])  # TODO: change clean_date
                new_product = Product(product_name=name, product_price=price,
                                      product_quantity=quantity, date_updated=date_updated)
                session.add(new_product)
        session.commit()


def err_check(message: str, func):
    flag = True
    while flag:
        x = input(message)
        x = func(x)
        if type(x) == int:
            flag = False
    return x


def add_product():
    '''add product to database'''
    name = input('Product Name: ')
    date = datetime.date.today()
    quantity = err_check('Quantity (Ex. 25): ', clean_qty)
    price = err_check('Price (Ex. 25.64): ', clean_price)
    new_product = Product(product_name=name, product_quantity=quantity,
                          product_price=price, date_updated=date)
    session.add(new_product)
    session.commit()
    print('Product added!')
    time.sleep(1.5)


def view_all_products():
    '''view all products'''
    for product in session.query(Product):
        print(f'{product.product_id} | {product.product_name} | {product.product_quantity} | {product.product_price/100} | {product.date_updated}')
    input('\nPress enter to return to the main menu.')


def view_product():
    '''view a product'''
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    # id_error = True
    # while id_error:
    #     id_choice = input(f'''
    #     \nId Options: {id_options}
    #     \rBook id: ''')
    #     id_choice = clean_id(id_choice, id_options)
    #     if type(id_choice) == int:
    #         id_error = False
    # the_book = session.query(Book).filter(Book.id == id_choice).first()
    # print(f'''
    #     \n{the_book.title} by {the_book.author}
    #     \rPublished: {the_book.published_date}
    #     \rPrice: ${the_book.price / 100}''')
    # sub_choice = sub_menu()
    # if sub_choice == '1':
    #     '''edit'''
    #     the_book.title = edit_check('Title', the_book.title)
    #     the_book.author = edit_check('Author', the_book.author)
    #     the_book.published_date = edit_check(
    #         'Date', the_book.published_date)
    #     the_book.price = edit_check('Price', the_book.price)
    #     session.commit()
    #     print('Book updated!')
    #     time.sleep(1.5)
    # elif sub_choice == '2':
    #     '''delete'''
    #     session.delete(the_book)
    #     session.commit()
    #     print('Book deleted!')
    #     time.sleep(1.5)
