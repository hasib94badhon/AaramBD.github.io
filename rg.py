from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Function to create a connection to MySQL
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='registration',
            user='root',
            password=''
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    return connection

# Function to insert user data into the database
def insert_user(name, phone, password):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # SQL query to insert user data
        sql_query = "INSERT INTO reg (name, phone, password) VALUES (%s, %s, %s)"
        user_data = (name, phone, password)

        cursor.execute(sql_query, user_data)
        connection.commit()
        print("User registration successful!")

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        insert_user(name, phone, password)
        return render_template('login.html')  # You can redirect to a success page or do something else here
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
