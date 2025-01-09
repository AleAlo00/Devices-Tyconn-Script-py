import sqlite3


# Funzione per controllare l'input
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


# Calcola l'incremento degli studio points
def calcola_incremento_studio_points(specifiche_scelte, funzionalita_scelte, livelli_specifiche):
    livelli_specifiche = {
    "RAM": {"4GB": 1, "6GB": 2, "8GB": 3, "10GB": 4, "12GB": 5, "16GB": 6},
    "CPU": {"A12": 1, "A13": 2, "A14": 3, "A15": 4, "A16": 5, "A17": 6},
    "GPU": {"Mali-G76": 1, "Mali-G77": 2, "Mali-G78": 3, "Mali-G79": 4, "Mali-G80": 5, "Mali-G81": 6},
    "Storage": {"64GB": 1, "128GB": 2, "256GB": 3, "512GB": 4, "1TB": 5, "2TB": 6},
    "Camera": {"12MP": 1, "16MP": 2, "20MP": 3, "24MP": 4, "32MP": 5, "48MP": 6},
    "Display": {"LCD": 1, "TFT": 2, "IPS": 3, "AMOLED": 4, "OLED": 5},
    "Battery": {"3000mAh": 1, "3500mAh": 2, "4000mAh": 3, "4500mAh": 4, "5000mAh": 5, "6000mAh": 6},
    "OS": {"Android": 1, "iOS": 2},
    "Number of Cameras": {"1": 1, "2": 2, "3": 3, "4": 4},
}
    incremento_totale = 0

    # Calcola i punti per le specifiche
    print("\n--- Debug: Calcolo incremento specifiche ---")
    for categoria, specifica in specifiche_scelte.items():
        livello = livelli_specifiche.get(categoria, {}).get(specifica, 1)
        incremento_totale += livello

    # Calcola i punti per le funzionalità
    incremento_totale += len(funzionalita_scelte)

    print(f"\n--- Debug: Incremento Totale: {incremento_totale} ---")
    return incremento_totale



# Caricamento dei dispositivi
def carica_dispositivi(id_azienda):
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nome FROM dispositivi WHERE id_azienda = ?", (id_azienda,))
    dispositivi = cursor.fetchall()
    conn.close()
    
    return dispositivi



# Aggiunta di un dispositivo con specifiche e funzionalità
def aggiungi_dispositivo(conn, nome, specifiche, funzionalita, id_azienda):
    cursor = conn.cursor()
    
    # Inserisci il dispositivo con id_azienda
    cursor.execute("INSERT INTO dispositivi (nome, id_azienda) VALUES (?, ?)", (nome, id_azienda))
    id_dispositivo = cursor.lastrowid  # Ottieni l'ID generato
    
    # Inserisci le specifiche
    for chiave, valore in specifiche.items():
        cursor.execute("INSERT INTO specifiche_dispositivo (id_dispositivo, chiave, valore, id_azienda) VALUES (?, ?, ?, ?)",
                       (id_dispositivo, chiave, valore, id_azienda))
    
    # Inserisci le funzionalità
    for funz in funzionalita:
        cursor.execute("INSERT INTO funzionalita_dispositivo (id_dispositivo, funzionalita, id_azienda) VALUES (?, ?, ?)",
                       (id_dispositivo, funz, id_azienda))
    
    conn.commit()




# Gestione del flusso per aggiungere un telefono
def AggiungiPhone(id, char, func, studio_points, livelli_specifiche, id_azienda):
    name = input("\nInserisci il nome del dispositivo -->| ")
    
    specifiche_scelte = {}
    for chiave, valori in char.items():
        print(f"\n{chiave}:")
        for i, valore in enumerate(valori, start=1):
            print(f"  [{i}] {valore}")
        
        indice = ControllaInput(f"Scegli un numero per {chiave} -->| ", list(range(1, len(valori) + 1)), "int")
        specifiche_scelte[chiave] = valori[indice - 1]

    print(f"\nSpecifiche scelte: {specifiche_scelte}")

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
    
    print(f"\nFunzionalità scelte: {funzionalita_scelte}")

    conn = sqlite3.connect("devices_tycoon.db")
    aggiungi_dispositivo(conn, name, specifiche_scelte, funzionalita_scelte, id_azienda)

    # Calcola l'incremento dinamico degli studio points
    incremento = calcola_incremento_studio_points(specifiche_scelte, funzionalita_scelte, livelli_specifiche)
    studio_points += incremento

    # Aggiorna i punti studio nel database
    cursor = conn.cursor()
    cursor.execute("UPDATE azienda SET studio_points = ? WHERE id = ?", (studio_points, id_azienda))  # Usa id_azienda
    conn.commit()
    conn.close()
    
    print(f"Dispositivo {name} aggiunto con successo!")
    print(f"Hai guadagnato {incremento} studio points! Totale attuale: {studio_points}")
    return id + 1, studio_points




# Visualizzazione dettagliata dei dispositivi
def VisualizzaDevices(id_azienda):
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()
    
    # Recupera i dispositivi dell'azienda
    cursor.execute("SELECT id, nome FROM dispositivi WHERE id_azienda = ?", (id_azienda,))
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


# Funzione per eliminare un dispositivo
def elimina_dispositivo(dispositivo_id):
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()

    # Elimina il dispositivo e i suoi dati correlati
    cursor.execute("DELETE FROM dispositivi WHERE id = ?", (dispositivo_id,))
    cursor.execute("DELETE FROM specifiche_dispositivo WHERE id_dispositivo = ?", (dispositivo_id,))
    cursor.execute("DELETE FROM funzionalita_dispositivo WHERE id_dispositivo = ?", (dispositivo_id,))

    conn.commit()
    conn.close()
    print(f"Dispositivo con ID {dispositivo_id} eliminato con successo.")
