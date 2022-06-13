from models import session, Product
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
            \rEnter t, v, a, b, or q.
            \rPress Enter to try again.''')


def clean_date(date_str, delim):
    split_date = date_str.split(delim)
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


def add_price(price_str):
    try:
        price_in_pennies = int(float(price_str) * 100)
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
        \rThe quantity should be an integer.
        \rEx. 25
        \rPress Enter to try again.
        \r*******************''')
        return
    return quantity

# TODO: update variable name book_id


def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
        \n*** ID ERROR ***
        \rThe id should be a number.
        \rEx. 1
        \rPress Enter to try again.
        \r****************''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(f'''
        \n*** ID ERROR ***
        \rOptions: {options}
        \rPress Enter to try again.
        \r****************''')
        return


def add_csv():
    with open('inventory.csv') as f:
        data = csv.reader(f)
        next(data)
        for row in data:

            product_in_db = session.query(Product).filter(
                Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = clean_qty(row[2])
                date_updated = clean_date(row[3], '/')

                new_product = Product(product_name=name, product_price=price,
                                      product_quantity=quantity, date_updated=date_updated)
                session.add(new_product)
            elif product_in_db != None:
                date_being_uploaded = clean_date(row[3], '/')
                date_in_db = product_in_db.date_updated
                if date_being_uploaded > date_in_db:
                    product_in_db.product_name = row[0]
                    product_in_db.product_price = clean_price(row[1])
                    product_in_db.product_quantity = clean_qty(row[2])
                    product_in_db.date_updated = date_being_uploaded

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
    price = err_check('Price (Ex. 25.64): ', add_price)
    product_exists = session.query(Product).filter(
        Product.product_name == name).one_or_none()
    if product_exists == None:
        new_product = Product(product_name=name, product_quantity=quantity,
                              product_price=price, date_updated=date)
        session.add(new_product)
        print('Product added!')
        time.sleep(1.5)
    elif product_exists != None:
        product_exists.product_quantity = quantity
        product_exists.product_price = price
        product_exists.date_updated = date
        print('Product updated!')
        time.sleep(1.5)

    session.commit()


def view_all_products():
    '''view all products'''
    for product in session.query(Product):
        print(f'{product.product_id} | Name: {product.product_name} | Qty: {product.product_quantity} | Price: {product.product_price/100} | Date Updated: {product.date_updated}')
    input('\nPress enter to return to the main menu.')


def view_product():
    '''view a product'''
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    id_error = True
    while id_error:
        id_choice = input(f'''
        \nId Options: {id_options}
        \Product id: ''')
        id_choice = clean_id(id_choice, id_options)
        if type(id_choice) == int:
            id_error = False
    indiv_product = session.query(Product).filter(
        Product.product_id == id_choice).first()
    print(f'''
        \n{indiv_product.product_id}: {indiv_product.product_name}
        \rQty: {indiv_product.product_quantity}
        \rPrice: ${indiv_product.product_price/100}
        \rDate: {indiv_product.date_updated}''')


def export_csv():
    '''export csv'''
    with open('inventory_backup.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['product_name', 'product_quantity', 'product_price', 'date_updated'])

        data = []
        for product in session.query(Product):
            price = product.product_price / 100
            data.append(
                [product.product_name, product.product_quantity, price, product.date_updated])
        writer.writerows(data)
