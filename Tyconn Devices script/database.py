import sqlite3

# Funzione per creare il database
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
            nome TEXT,
            id_azienda INTEGER,  -- Associa ogni dispositivo a una specifica azienda
            FOREIGN KEY (id_azienda) REFERENCES azienda(id)
        )
    ''')

    # Creazione della tabella per le specifiche dei dispositivi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS specifiche_dispositivo (
            id_dispositivo INTEGER,
            chiave TEXT,
            valore TEXT,
            id_azienda INTEGER,  -- Associa le specifiche al dispositivo dell'azienda
            FOREIGN KEY (id_dispositivo) REFERENCES dispositivi(id),
            FOREIGN KEY (id_azienda) REFERENCES azienda(id)
        )
    ''')

    # Creazione della tabella per le funzionalità dei dispositivi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funzionalita_dispositivo (
            id_dispositivo INTEGER,
            funzionalita TEXT,
            id_azienda INTEGER,  -- Associa le funzionalità al dispositivo dell'azienda
            FOREIGN KEY (id_dispositivo) REFERENCES dispositivi(id),
            FOREIGN KEY (id_azienda) REFERENCES azienda(id)
        )
    ''')

    # Creazione della tabella per le specifiche massime
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS max_specifiche (
            categoria TEXT,
            specifica TEXT,
            costo INTEGER
        )
    ''')

    # Creazione della tabella per le funzionalità massime
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS max_funzionalita (
            funzionalita TEXT,
            costo INTEGER
        )
    ''')

    # Creazione della tabella per le specifiche possedute
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS specifiche_possedute (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            specifica TEXT
        )
    ''')

    # Creazione della tabella per le funzionalità possedute
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funzioni_possedute (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funzionalita TEXT
        )
    ''')

    conn.commit()
    conn.close()
