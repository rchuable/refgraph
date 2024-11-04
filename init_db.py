'''
I need to set up a database for the files

References:

'''

import sqlite3

def initialize_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # datatable called files
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   filename TEXT NOT NULL,
                   filepath TEXT NOT NULL,
                   filetype TEXT NOT NULL,
                   uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                ''')

    # datatable called urls
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   url TEXT NOT NULL
                   )
                ''')

    # datatable called annotations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS annotations (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   file_id INTEGER NOT NULL,
                   content TEXT NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMPE,
                   FOREIGN KEY (file_id) REFERENCES files (id)
                   )
                ''')

    # datatable called links (yay networks)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   source_id INTEGER NOT NULL,
                   target_id INTEGER NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (source_id) REFERENCES files (id),
                   FOREIGN KEY (target_id) REFERENCES files (id)
                   )
                   ''')

    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == '__main__':
    initialize_db()
