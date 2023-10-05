import sqlite3

instance="fantasy-dictionary"
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('instances/${instance}dictionary_entries.db')
# Create a new SQLite cursor
cur = conn.cursor()