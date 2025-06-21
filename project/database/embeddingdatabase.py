# database/EmbeddingDatabase.py

import sqlite3

# Connect to SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect("email_data.db")
c = conn.cursor()

# Create table for storing email and embeddings
def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS emails
                 (subject TEXT, sender TEXT, embedding BLOB)''')
    conn.commit()

# Insert email data and its embedding
def insert_email_data(subject, sender, embedding):
    c.execute("INSERT INTO emails (subject, sender, embedding) VALUES (?, ?, ?)", 
              (subject, sender, embedding))
    conn.commit()

# Fetch all stored emails
def fetch_all_emails():
    c.execute("SELECT * FROM emails")
    return c.fetchall()

# Example Usage
create_table()
insert_email_data("Test Subject", "test@example.com", b"embedding_data_here")  # Replace with actual embedding
print(fetch_all_emails())

# Close the connection
conn.close()
