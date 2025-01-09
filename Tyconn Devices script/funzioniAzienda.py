import sqlite3

# Funzione per caricare i dati dell'azienda
def carica_azienda(nome_azienda=None):
    conn = sqlite3.connect('devices_tycoon.db')
    cursor = conn.cursor()

    if nome_azienda:  # Carica i dettagli dell'azienda specifica
        cursor.execute("SELECT nome, money, studio_points FROM azienda WHERE nome = ?", (nome_azienda,))
    else:  # Carica l'ultima azienda aggiunta se nome_azienda è None
        cursor.execute("SELECT nome, money, studio_points FROM azienda ORDER BY id DESC LIMIT 1")
    
    azienda = cursor.fetchone()
    conn.close()

    if azienda:
        return {"nome": azienda[0], "money": azienda[1], "studio_points": azienda[2]}
    return None



# Funzione per visualizzare i dati dell'azienda
def aggiungi_azienda(nome, money, studio_points):
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO azienda (nome, money, studio_points) VALUES (?, ?, ?)", (nome, money, studio_points))
    conn.commit()
    conn.close()

# Funzione per visualizzare i dati dell'azienda
def VisualizzaAzienda(name,money,studio_points):
    print(f"""\nAzienda
    Name: {name}
    Money: {money}
    Studio Points: {studio_points}
    """)


# Funzione per eliminare l'azienda
def elimina_azienda():
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()

    # Elimina i dati dall'azienda e tutte le tabelle correlate
    cursor.execute("DELETE FROM azienda")
    cursor.execute("DELETE FROM dispositivi")
    cursor.execute("DELETE FROM specifiche_dispositivo")
    cursor.execute("DELETE FROM funzionalita_dispositivo")
    cursor.execute("DELETE FROM specifiche_possedute")
    cursor.execute("DELETE FROM funzioni_possedute")

    conn.commit()
    conn.close()
    print("Tutti i dati relativi all'azienda sono stati eliminati.")


# Funzione per aggiungere un'azienda
def esiste_azienda(nome_azienda):
    conn = sqlite3.connect("devices_tycoon.db") 
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM azienda WHERE nome = ?", (nome_azienda,))
    esiste = cursor.fetchone()[0] > 0
    conn.close()
    return esiste

# Funzione per visualizzare i dati dell'azienda
def lista_aziende():
    conn = sqlite3.connect('devices_tycoon.db')
    cursor = conn.cursor()

    # Query per ottenere tutte le aziende
    cursor.execute("SELECT id, nome, money, studio_points FROM azienda")
    aziende = cursor.fetchall()

    conn.close()
    return aziende

import sqlite3

# Funzione per ottenere l'ID dell'azienda in base al nome
def ottieni_id_azienda(nome_azienda):
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM azienda WHERE nome = ?", (nome_azienda,))
    azienda = cursor.fetchone()
    conn.close()
    
    if azienda:
        return azienda[0]  # Restituisci l'ID
    else:
        print("Errore: azienda non trovata.")
        return None



