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
    "RAM": {"4GB": 1, "6GB": 2, "8GB": 3, "10GB": 4},
    "CPU": {"A12": 1, "A13": 2, "A14": 3, "A15": 4},
    "GPU": {"Mali-G76": 1, "Mali-G77": 2, "Mali-G78": 3, "Mali-G79": 4},
    "Storage": {"64GB": 1, "128GB": 2, "256GB": 3, "512GB": 4},
}
    incremento_totale = 0

    # Calcola i punti per le specifiche
    print("\n--- Debug: Calcolo incremento specifiche ---")
    for categoria, specifica in specifiche_scelte.items():
        print(f"Categoria: {categoria}, Specifica: {specifica}")  # Debug: visualizza il valore di 'specifica'
        livello = livelli_specifiche.get(categoria, {}).get(specifica, 1)
        print(f"Livello trovato: {livello}")  # Debug: visualizza il livello calcolato
        incremento_totale += livello

    # Calcola i punti per le funzionalità
    print("\n--- Debug: Calcolo incremento funzionalità ---")
    for funzionalita in funzionalita_scelte:
        print(f"Funzionalità: {funzionalita}, Incremento: 1")
    incremento_totale += len(funzionalita_scelte)

    print(f"\n--- Debug: Incremento Totale: {incremento_totale} ---")
    return incremento_totale



# Caricamento dei dispositivi
def carica_dispositivi():
    conn = sqlite3.connect("devices_tycoon.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM dispositivi")
    dispositivi = cursor.fetchall()
    conn.close()
    
    return dispositivi


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
def AggiungiPhone(id, char, func, studio_points, livelli_specifiche):
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
    aggiungi_dispositivo(conn, name, specifiche_scelte, funzionalita_scelte)

    # Calcola l'incremento dinamico degli studio points
    incremento = calcola_incremento_studio_points(specifiche_scelte, funzionalita_scelte, livelli_specifiche)
    studio_points += incremento

    # Aggiorna i punti studio nel database
    cursor = conn.cursor()
    cursor.execute("UPDATE azienda SET studio_points = ? WHERE id = ?", (studio_points, id))
    conn.commit()
    conn.close()
    
    print(f"Dispositivo {name} aggiunto con successo!")
    print(f"Hai guadagnato {incremento} studio points! Totale attuale: {studio_points}")
    return id + 1, studio_points




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
