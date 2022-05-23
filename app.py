from models import (Base, session, Product, engine)
import datetime
import time

from functions import clean_date, clean_price, add_csv, menu, add_product, view_all_products


def sub_menu():
    while True:
        print('''
        \n1. Edit
        \r2. Delete
        \r3. Return to main menu''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            input('''
            \rPlease choose one of the options above.
            \rA number from 1 - 3.
            \rPress Enter to try again.''')


def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
        \n*** ID ERROR ***
        \rThe id should eb anumber.
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


def edit_check(column_name, current_value):
    print(f'\n*** EDIT {column_name} ***')
    if column_name == 'Price':
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name == 'Date':
        print(f'\rCurrent Value: {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'\rCurrent Value: {current_value}')

    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input("What would you like to change the value to? ")
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            if column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes

    else:
        return input("What would you like to change the value to? ")


def app():
    app_running = True
    while app_running:
        choice = menu()

        # this is slow... refactor to use an indexed dict obj.
        if choice == 'a':
            add_product()
        elif choice == 't':
            view_all_products()
        elif choice == 'v':
            pass
        elif choice == '4':
            '''book analysis'''
            oldest_book = session.query(Book).order_by(
                Book.published_date).first()
            newest_book = session.query(Book).order_by(
                Book.published_date.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(
                Book.title.like('%Python%')).count()
            print(f'''
                \n*** BOOK ANALYSIS ***
                \rOldest Book: {oldest_book}
                \rNewest Book: {newest_book}
                \rTotal Books: {total_books}
                \rPython Books: {python_books}''')
            input('\nPress enter to return to the main menu.')
        else:
            '''exit'''
            print('GOODBYE')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    # app()
    # menu()
    view_all_products()

    # for product in session.query(Product):
    #     print(product)
