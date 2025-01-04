#Funzioni
import sqlite3

def ControllaInput(s,list,value_type):
    corretto = False
    while not corretto:
        try:
            if value_type == 'int':
                x = int(input(s))
            elif value_type == 'float':
                x = float(input(s))
            elif value_type == 'str':
                x = input(s)
            
            if x in list:
                corretto = True
                return x
            else:
                print('Valore non valido')
        except:
            print('Valore non valido')

def carica_azienda():
    conn = sqlite3.connect('tycoon_devices.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM azienda LIMIT 1")
    azienda = cursor.fetchone()
    conn.close()
    
    if azienda:
        return azienda  # Restituisce i dati aziendali (id, nome, money, studio_points)
    else:
        return None  # Se non esiste, ritorna None

def aggiungi_azienda(nome, money, studio_points):
    conn = sqlite3.connect('tycoon_devices.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO azienda (nome, money, studio_points) VALUES (?, ?, ?)", (nome, money, studio_points))
    conn.commit()
    conn.close()


def carica_dispositivi():
    conn = sqlite3.connect('tycoon_devices.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM dispositivi")
    dispositivi = cursor.fetchall()
    conn.close()
    
    return dispositivi


def aggiungi_dispositivo(conn, nome, caratteristiche, funzionalita):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dispositivi (nome, caratteristiche, funzionalita) VALUES (?, ?, ?)", 
                   (nome, ', '.join(caratteristiche), ', '.join(funzionalita)))
    conn.commit()



def AggiungiPhone(id, char, func):
    name = input('Inserisci il nome del dispositivo -->| ')
    conn = sqlite3.connect('tycoon_devices.db')  # Crea la connessione una sola volta
    aggiungi_dispositivo(conn, name, char, func)
    conn.close()  # Chiudi la connessione al termine
    print(f"Dispositivo {name} aggiunto con successo!")
    return id + 1




def VisualizzaDevices(devices):
    for device in devices:
        id_device, name, caratteristiche, funzionalita = device
        print(f"""
        \nDispositivo
        ID: {id_device}
        Nome: {name}
        Caratteristiche: {caratteristiche}
        Funzionalità: {funzionalita}
        """)

def VisualizzaAzienda(name,money,studio_points):
    print(f"""\nAzienda
    Name: {name}
    Money: {money}
    Studio Points: {studio_points}
    """)