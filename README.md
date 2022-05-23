Code adapted from this project: https://teamtreehouse.com/library/project-overview-8

To the best of my current ability I optimized data structures and abstracted helper functions out of the app.py file to ease code readability.

Having a solid foundation ("legacy code") to work with I instead focused on making improvements and writing more pythonic code.

# 1. Create a new virtual Python environment

## Create a virtual environment in your project's directory by running the following command in your terminal:

```
python -m venv env
```

- NOTE: The environment (./env) folder and files pertaining to your virtual environment should not be added to your GitHub repo.

# 2. Activate your new virtual Python environment

## Activate the virtual environment by running the following command in your terminal for students using macs:

If using Mac/Linux:

```
source ./env/bin/activate
```

# 3.Install required dependencies into your Python environment

## Install the project requirements by running the following command in your terminal:

```
pip install sqlalchemy
```

Make sure you freeze the dependencies into a requirements.txt file by then running this command in your terminal:

```
pip freeze > requirements.txt
```

# 4. Create a .gitignore file

## Create a new file in your project directory called .gitignore. Add your virtual environment folder (usually "env") to the .gitignore file. Add **pycache** to the .gitignore file.

# 5. Create your application file

- Create a new file in your project directory called app.py. Be sure to import the appropriate Python and SQLAlchemy modules at the top of this file.

# 6. Initialize your Sqlite database

Initialize a Sqlite database called inventory.db.

Create your database model called Product
Create a model called Product that the SQLAlchemy ORM will use to build the database. The Product model should have five attributes: product_id, product_name, product_quantity, product_price, and date_updated. Use SQLALchemy’s built-in primary_key functionality for the product_id field, so that each product will have an automatically generated unique identifier.

Connect the database and create tables
In your dunder main method:

Ensure you are connected to the database you created/initialized
Ensure you load the CSV products data into the created table
Run the application so the user can make menu choices and interact with the application.
Read in the existing CSV data
Read the inventory.csv file into your program, and create a list that contains each product inside the csv file as a dictionary. Be sure to clean up the data before adding each product dictionary to your list:

the value for product_id will be stored as SQLAlchemy’s built in primary_key
the value for product_quantity will be stored as an integer
the value for product_price will be stored as an integer and converted to cents ($3.19 becomes 319, for example)
the value for date_updated will be stored as a DateTime.
Hint: You'll need the datetime module for this.
Add the data from CSV into the database
Create a function that will add the products listed in the inventory.csv file to the database.

Create a Menu to make selections
Create a function to handle interaction with the user of your app. This function should prompt the user to enter v in order to view the details of a single product in the database, a to add a new product to the database, or b to make a backup of the entire contents of the database.

Displaying a product by its ID - Menu Option V
Create a function to handle getting and displaying a product by its product_id.

Adding a new product to the database - Menu Option A
Create a function to handle adding a new product to the database. This function should prompt the user to enter the product's name, quantity, and price. The function must process the user-provided value for price from a string to an int. Be sure the value you stored for the price field to the database is converted to cents ($2.99 becomes 299, for example).

Backup the database (Export new CSV) - Menu Option B
Create a function to handle making a backup of the database. The backup should be written to a .csv file.
