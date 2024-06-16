import streamlit as st
import sqlite3
from hashlib import sha256

# Function to hash the password
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Function to create a new user in the database
def create_user(username, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

# Function to authenticate user during sign-in
def authenticate_user(username, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

# Create the users table if it doesn't exist
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )''')
conn.commit()
conn.close()

# Streamlit app
def main():
    st.title("Professional Sign-Up and Sign-In")

    menu = ["Sign Up", "Sign In"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign Up":
        st.subheader("Create New Account")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Sign Up"):
            create_user(new_username, new_password)
            st.success("Account created successfully!")

    elif choice == "Sign In":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Sign In"):
            user = authenticate_user(username, password)
            if user:
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Invalid username or password.")

if __name__ == '__main__':
    main()
