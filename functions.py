from models import (Base, session, Product, engine)
import csv
import datetime


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
    # months = ['January', 'February', 'March', 'April', 'May', 'June',
    #           'July', 'August', 'September', 'October', 'November', 'December']
    # split_date = date_str.split(' ')
    # try:
    #     month = int(months.index(split_date[0]) + 1)
    #     day = int(split_date[1].split(',')[0])
    #     year = int(split_date[2])
    #     return_date = datetime.date(year, month, day)
    # except ValueError:
    #     input('''
    #     \n *** DATE ERROR ***
    #     \r The date format should include a valid Month Day, Year from the past.
    #     \rEx. January 13, 2003.
    #     \rPress Enter to try again.
    #     \r*******************''')
    #     return
    # else:
    #     return return_date


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
    # try:
    #     price_float = float(price_str)
    # except ValueError:
    #     input('''
    #     \n*** PRICE ERROR ***
    #     \rThe price should be a number without a currency symbol.
    #     \rEx. 10.99
    #     \rPress Enter to try again.
    #     \r*******************''')
    #     return
    # return int(price_float * 100)


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
        #     if book_in_db == None:
        #         title = row[0]
        #         author = row[1]
        #         date = clean_date(row[2])
        #         price = clean_price(row[3])
        #         new_book = Book(title=title, author=author,
        #                         published_date=date, price=price)
        #         session.add(new_book)
        # session.commit()
