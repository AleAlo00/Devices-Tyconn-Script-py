import sqlite3

def crea_database():
    conn = sqlite3.connect('tycoon_devices.db')  
    cursor = conn.cursor()
    
    # Creazione della tabella per l'azienda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS azienda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            money INTEGER,
            studio_points INTEGER
        )
    ''')
    
    # Creazione della tabella per i dispositivi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dispositivi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            caratteristiche TEXT,
            funzionalita TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
