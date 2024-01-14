import MySQLdb
import datetime
import os
import bcrypt

connection = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl={
        "rejectUnauthorized": True,
    },
)


def add_task(user_id, task_content):
    cursor = connection.cursor()
    query = f"""
        INSERT INTO tasks (user_id, task_content, is_finished, date_added)
        VALUES ("{user_id}", "{task_content}", "0", "{str(datetime.datetime.now())}");
    """
    cursor.execute(query)
    

def check_login(username, password):
    cursor = connection.cursor()
    query = f"""
        SELECT user_password_hash, user_password_salt
        FROM users WHERE username = "{username}";
    """
    cursor.execute(query)
    response = cursor.fetchall()
    if response:
        result = response[0]
        server_hashed = result[0]
        server_salt = result[1]
        user_hashed = bcrypt.hashpw(password.encode("utf-8"), server_salt.encode("utf-8")).decode("utf-8")
        print(user_hashed)
        if server_hashed == user_hashed:
            print('AUTHENTICATED')
            return True
    return False



def new_user(username, email, password):
    cursor = connection.cursor()
    query = f"""
        SELECT *
        FROM users WHERE username = "{username}";
    """
    if cursor.execute(query) == 0:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        cursor = connection.cursor()
        query = f"""
            INSERT INTO users (username, user_email, user_password_hash, user_password_salt)
            VALUES ("{username}", "{email}", "{hashed.decode("utf-8")}", "{salt.decode("utf-8")}");
        """
        cursor.execute(query)
        return True
    else:
        return False