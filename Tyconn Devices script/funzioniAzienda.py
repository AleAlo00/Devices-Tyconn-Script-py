import sqlite3

# Funzione per caricare i dati dell'azienda
def carica_azienda():
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM azienda LIMIT 1")
    azienda = cursor.fetchone()
    conn.close()
    
    if azienda:
        return azienda  # Restituisce i dati aziendali (id, nome, money, studio_points)
    else:
        return None  # Se non esiste, ritorna None

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