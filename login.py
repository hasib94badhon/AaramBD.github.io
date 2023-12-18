from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Database connection configuration
try:
    db = pymysql.connect(host='localhost', user='root', password='', database='registration')
    cursor = db.cursor()
except pymysql.Error as e:
    print("Error connecting to the database:", e)
    exit(1)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        phone = request.form['login']
        password = request.form['password']

        try:
            # Execute SQL query to check user credentials
            query = "SELECT * FROM reg WHERE phone=%s AND password=%s"
            cursor.execute(query, (phone, password))
            user = cursor.fetchone()
            if user:
                # Fetch user data
                user_id = user[0]
                username = user[1]  # Assuming username is in the second column
                user_phone = user[2]  # Assuming phone number is in the third column

                # Redirect to profile with user data
                return redirect(url_for('profile', username=username, phone=user_phone,id = user_id))
            else:
                # Login failed
                return "Invalid phone number or password!"
        except pymysql.Error as e:
            print("Error executing SQL query:", e)
            return "An error occurred while processing your request."

# @app.route('/profile/<username>/<phone>')
# def profile(username, phone):
#     return render_template('profile.html', username=username, phone=phone)

@app.route('/profile/<username>/<phone>/<id>')
def profile(username, phone, id):
    try:
        # Fetch additional information (description, nid, address) from the user table based on the user ID
        select_query = "SELECT des, nid, address FROM user WHERE userid=%s"
        cursor.execute(select_query, (id,))
        user_info = cursor.fetchone()

        if user_info:
            description = user_info[0]  # Assuming description is in the first position in the query result
            nid = user_info[1]  # Assuming nid is in the second position in the query result
            address = user_info[2]  # Assuming address is in the third position in the query result

            # Pass fetched data to the profile.html template
            return render_template('profile.html', username=username, phone=phone, description=description, nid=nid, address=address)
        else:
            return "User information not found!"
    except pymysql.Error as e:
        print("Error fetching user information:", e)
        return "An error occurred while fetching user information."

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        username = request.form['editName']
        phone = request.form['editPhone']
        # Additional information for user table
        description = request.form['editDescription']
        nid = request.form['editNID']
        address = request.form['editAddress']
        
        try:
            # Get reg_id, username, and phone from registration table based on username and password
            reg_query = "SELECT reg_id, name, phone FROM reg WHERE name=%s AND phone=%s"
            cursor.execute(reg_query, (username, phone))
            reg_user = cursor.fetchone()

            if reg_user:
                reg_id = reg_user[0]  # Extract reg_id from the query result
                reg_name = reg_user[1]  # Extract name from the query result
                reg_phone = reg_user[2]  # Extract phone from the query result

                # Check if name or phone is updated
                if reg_name != username or reg_phone != phone:
                    # Update name and phone in both registration and user tables
                    update_reg_query = "UPDATE reg SET name=%s WHERE reg_id=%s"
                    cursor.execute(update_reg_query, (username, reg_id))

                    update_user_query = "UPDATE user SET name=%s, phone=%s WHERE userid=%s"
                    cursor.execute(update_user_query, (username, phone, reg_id))

                # Update additional information in user table only if name or phone is updated
                if reg_name != username or reg_phone != phone:
                    update_info_query = "UPDATE user SET des=%s, nid=%s, address=%s WHERE userid=%s"
                    cursor.execute(update_info_query, (description, nid, address, reg_id))

                db.commit()
                success_flag = True
        
                # Pass success flag to the profile.html template
                return render_template('profile.html', success_flag=success_flag, username=username, phone=phone, description=description, nid=nid, address=address)
                
                # return "Profile updated successfully!"
                # return render_template('profile.html')
            else:
                return "User not found in registration table!"
        except pymysql.Error as e:
            db.rollback()  
            print("Error updating profile:", e)
            return "An error occurred while updating the profile."




if __name__ == '__main__':
    app.run(debug=True)
