import sqlite3

# Creazione del database
def crea_database():
    conn = sqlite3.connect('devices_tycoon.db')  
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
            nome TEXT
        )
    ''')

    # Creazione della tabella per le specifiche dei dispositivi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS specifiche_dispositivo (
            id_dispositivo INTEGER,
            chiave TEXT,
            valore TEXT,
            FOREIGN KEY (id_dispositivo) REFERENCES dispositivi (id)
        )
    ''')

    # Creazione della tabella per le funzionalità dei dispositivi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funzionalita_dispositivo (
            id_dispositivo INTEGER,
            funzionalita TEXT,
            FOREIGN KEY (id_dispositivo) REFERENCES dispositivi (id)
        )
    ''')

    # Creazione della tabella per le max specifiche
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS max_specifiche (
            categoria TEXT,
            specifica TEXT,
            costo INTEGER
        )
    ''')

    # Creazione della tabella per le max funzionalità
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS max_funzionalita (
            funzionalita TEXT,
            costo INTEGER
        )
    ''')

    conn.commit()
    conn.close()
