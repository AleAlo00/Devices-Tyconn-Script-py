#Funzioni
import sqlite3

def ControllaInput(s,list,value_type):
    corretto = False
    while not corretto:
        try:
            if value_type == "int":
                x = int(input(s))
            elif value_type == "float":
                x = float(input(s))
            elif value_type == "str":
                x = input(s)
            
            if x in list:
                corretto = True
                return x
            else:
                print("Valore non valido")
        except:
            print("Valore non valido")

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

def aggiungi_azienda(nome, money, studio_points):
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO azienda (nome, money, studio_points) VALUES (?, ?, ?)", (nome, money, studio_points))
    conn.commit()
    conn.close()


def carica_dispositivi():
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM dispositivi")
    dispositivi = cursor.fetchall()
    conn.close()
    
    return dispositivi


def VisualizzaAzienda(name,money,studio_points):
    print(f"""\nAzienda
    Name: {name}
    Money: {money}
    Studio Points: {studio_points}
    """)


# Aggiunta di un dispositivo con specifiche e funzionalità
def aggiungi_dispositivo(conn, nome, specifiche, funzionalita):
    cursor = conn.cursor()
    
    # Inserisci il dispositivo
    cursor.execute("INSERT INTO dispositivi (nome) VALUES (?)", (nome,))
    id_dispositivo = cursor.lastrowid  # Ottieni l"ID generato
    
    # Inserisci le specifiche
    for chiave, valore in specifiche.items():
        cursor.execute("INSERT INTO specifiche_dispositivo (id_dispositivo, chiave, valore) VALUES (?, ?, ?)",
                       (id_dispositivo, chiave, valore))
    
    # Inserisci le funzionalità
    for funz in funzionalita:
        cursor.execute("INSERT INTO funzionalita_dispositivo (id_dispositivo, funzionalita) VALUES (?, ?)",
                       (id_dispositivo, funz))
    
    conn.commit()


# Gestione del flusso per aggiungere un telefono
def AggiungiPhone(id, char, func,studio_points):
    name = input("\nInserisci il nome del dispositivo -->| ")
    
    specifiche_scelte = {}
    for chiave, valori in char.items():
        print(f"\n{chiave}:")
        for i, valore in enumerate(valori, start=1):
            print(f"  [{i}] {valore}")
        
        indice = ControllaInput(f"Scegli un numero per {chiave} -->| ", list(range(1, len(valori) + 1)), "int")
        specifiche_scelte[chiave] = valori[indice - 1]
    
    funzionalita_scelte = []
    print(f"\nFunzionalità disponibili:")
    for i, funz in enumerate(func, start=1):
        print(f"  [{i}] {funz}")
    print("Inserisci i numeri delle funzionalità desiderate separati da spazi (esempio: 1 3 4):")
    
    while True:
        scelte = input("-->| ").split()
        try:
            scelte_numeri = [int(scelta) for scelta in scelte if scelta.isdigit()]
            if all(1 <= scelta <= len(func) for scelta in scelte_numeri):
                funzionalita_scelte = [func[scelta - 1] for scelta in scelte_numeri]
                break
            else:
                print("Una o più scelte non sono valide. Riprova.")
        except ValueError:
            print("Errore nell'input. Inserisci numeri validi separati da spazi.")
    
    conn = sqlite3.connect("devices_tycoon.db")
    aggiungi_dispositivo(conn, name, specifiche_scelte, funzionalita_scelte)

    studio_points += 10
    cursor = conn.cursor()
# Aggiorna i punti studio nella tabella azienda
    cursor.execute("UPDATE azienda SET studio_points = ? WHERE id = ?", (studio_points, id))
    conn.commit()
    conn.close()
    
    print(f"Dispositivo {name} aggiunto con successo!")
    return id + 1,studio_points


# Visualizzazione dettagliata dei dispositivi
def VisualizzaDevices():
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()
    
    # Recupera i dispositivi
    cursor.execute("SELECT * FROM dispositivi")
    dispositivi = cursor.fetchall()
    
    for dispositivo in dispositivi:
        id_dispositivo, nome = dispositivo
        print(f"\nDispositivo ID: {id_dispositivo}, Nome: {nome}")
        
        # Recupera le specifiche
        cursor.execute("SELECT chiave, valore FROM specifiche_dispositivo WHERE id_dispositivo = ?", (id_dispositivo,))
        specifiche = cursor.fetchall()
        print("  Specifiche:")
        for chiave, valore in specifiche:
            print(f"    {chiave}: {valore}")
        
        # Recupera le funzionalità
        cursor.execute("SELECT funzionalita FROM funzionalita_dispositivo WHERE id_dispositivo = ?", (id_dispositivo,))
        funzionalita = cursor.fetchall()
        print("  Funzionalità:")
        for funz in funzionalita:
            print(f"    {funz[0]}")
    
    conn.close()

def carica_max_specifiche():
    maxSpecifiche = {
        "RAM": {"4GB": 10, "6GB": 20, "8GB": 30},
        "CPU": {"A12": 10, "A13": 20, "A14": 30},
        "GPU": {"Mali-G76": 10, "Mali-G77": 20, "Mali-G78": 30},
        "Storage": {"64GB": 10, "128GB": 20, "256GB": 30},
    }
    
    conn = sqlite3.connect('devices_tycoon.db')  
    cursor = conn.cursor()

    for categoria, opzioni in maxSpecifiche.items():
        for specifica, costo in opzioni.items():
            cursor.execute('''
                INSERT INTO max_specifiche (categoria, specifica, costo)
                VALUES (?, ?, ?)
            ''', (categoria, specifica, costo))
    
    conn.commit()
    conn.close()

def carica_max_funzionalita():
    maxFunzionalita = {
        "5G": 10,
        "Touch ID": 20,
        "NFC": 30,
    }
    
    conn = sqlite3.connect('devices_tycoon.db')  
    cursor = conn.cursor()

    for funzionalita, costo in maxFunzionalita.items():
        cursor.execute('''
            INSERT INTO max_funzionalita (funzionalita, costo)
            VALUES (?, ?)
        ''', (funzionalita, costo))
    
    conn.commit()
    conn.close()



def CompraSpecifiche(maxSpecifiche, specifc, studio_points):

    categorie = list(maxSpecifiche.keys())
    print("\nSpecifiche disponibili:")
    for i, categoria in enumerate(categorie, start=1):
        print(f"[{i}] {categoria}")
        for j, (specifica, costo) in enumerate(maxSpecifiche[categoria].items(), start=1):
            print(f"    [{j}] {specifica} - {costo} studio_points")

    # Seleziona categoria
    print(f"\nHai {studio_points} studio_points.")
    scelta_categoria = ControllaInput("\nScegli una categoria (numero) -->| ", list(range(1, len(categorie) + 1)), "int")
    categoria = categorie[scelta_categoria - 1]

    # Seleziona opzione
    opzioni = list(maxSpecifiche[categoria].keys())
    scelta_opzione = ControllaInput(f"Scegli un'opzione per {categoria} (numero) -->| ", list(range(1, len(opzioni) + 1)), "int")
    specifica = opzioni[scelta_opzione - 1]
    costo = maxSpecifiche[categoria][specifica]

    # Verifica e acquista
    if studio_points >= costo:
        studio_points -= costo
        specifc[categoria].append(specifica)
        del maxSpecifiche[categoria][specifica]  
        print(f"Hai comprato {specifica} per {categoria} al costo di {costo} studio_points!")
        if not maxSpecifiche[categoria]:
            del maxSpecifiche[categoria]

    else:
        print("Non hai abbastanza punti studio.")
    
    return specifc, studio_points