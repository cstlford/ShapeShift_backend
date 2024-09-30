import sqlite3
import pandas as pd

def init_food_db():
    # Connect to db
    connection = sqlite3.connect("food.db")
    cursor = connection.cursor()

    # Get food data
    df = pd.read_csv('nutrition.csv')

    # Create table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_data (
            id TEXT,
            name TEXT,
            serving_size TEXT,
            calories TEXT,
            total_fat TEXT,
            protein TEXT,
            carbohydrate TEXT
        )
    ''')

    # Inserts data from csv file
    df.to_sql('food_data', connection, if_exists='replace', index=False)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    return 0

def search_food_db(food):

    if food == 'beef' or 'chicken':
        food = food+', raw'
    
    connection = sqlite3.connect('food.db') 
    
    raw_results = connection.execute(f"SELECT * FROM food_data WHERE name LIKE '%{food}%' LIMIT 50")
    results = raw_results.fetchall()

    
    # terminate the connection 
    connection.close()
    return results

#search_food_db('Beef')







