from models import Base, engine
from functions import (add_csv, menu, add_product,
                       view_all_products, view_product,
                       export_csv)


def app():
    app_running = True
    while app_running:
        choice = menu()

        if choice == 'a':
            add_product()
        elif choice == 't':
            view_all_products()
        elif choice == 'v':
            view_product()
        elif choice == 'b':
            export_csv()

        else:
            '''exit'''
            print('GOODBYE')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # clean_csv()
    add_csv()
    app()
    # print(clean_name(
    #     ['"Bread - Crumbs', ' Bulk"', '$4.49', '88', '1/12/2019']))
