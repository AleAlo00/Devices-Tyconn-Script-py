#Funzioni
import sqlite3
from funzioniDevices import ControllaInput

def carica_max_specifiche():
    conn = sqlite3.connect('devices_tycoon.db')
    cursor = conn.cursor()

    # Dichiara un dizionario vuoto per memorizzare le specifiche
    maxSpecifiche = {}

    # Controlla se i dati esistono già nella tabella `max_specifiche`
    cursor.execute("SELECT COUNT(*) FROM max_specifiche")
    count = cursor.fetchone()[0]

    # Se la tabella è vuota, inserisci i dati predefiniti
    if count == 0:
        defaultSpecifiche = {
            "RAM": {"6GB": 10, "8GB": 20, "10GB": 30},
            "CPU": {"A13": 10, "A14": 20, "A15": 30},
            "GPU": {"Mali-G77": 10, "Mali-G78": 20, "Mali-G79": 30},
            "Storage": {"128GB": 10, "256GB": 20, "512GB": 30},
        }
        for categoria, opzioni in defaultSpecifiche.items():
            for specifica, costo in opzioni.items():
                cursor.execute('''
                    INSERT INTO max_specifiche (categoria, specifica, costo)
                    VALUES (?, ?, ?)
                ''', (categoria, specifica, costo))
        conn.commit()

    # Carica i dati dal database
    cursor.execute("SELECT categoria, specifica, costo FROM max_specifiche")
    rows = cursor.fetchall()

    for categoria, specifica, costo in rows:
        if categoria not in maxSpecifiche:
            maxSpecifiche[categoria] = {}
        maxSpecifiche[categoria][specifica] = costo

    conn.close()
    return maxSpecifiche


def carica_max_funzionalita():
    conn = sqlite3.connect('devices_tycoon.db')
    cursor = conn.cursor()

    # Dichiara un dizionario vuoto per memorizzare le funzionalità
    maxFunzionalita = {}

    # Controlla se i dati esistono già nella tabella `max_funzionalita`
    cursor.execute("SELECT COUNT(*) FROM max_funzionalita")
    count = cursor.fetchone()[0]

    # Se la tabella è vuota, inserisci i dati predefiniti
    if count == 0:
        defaultFunzionalita = {
            "5G": 10,
            "Touch ID": 20,
            "NFC": 30,
        }
        for funzionalita, costo in defaultFunzionalita.items():
            cursor.execute('''
                INSERT INTO max_funzionalita (funzionalita, costo)
                VALUES (?, ?)
            ''', (funzionalita, costo))
        conn.commit()

    # Carica i dati dal database
    cursor.execute("SELECT funzionalita, costo FROM max_funzionalita")
    rows = cursor.fetchall()

    for funzionalita, costo in rows:
        maxFunzionalita[funzionalita] = costo

    conn.close()
    return maxFunzionalita

def carica_specifiche_possedute():
    conn = sqlite3.connect('devices_tycoon.db')
    cursor = conn.cursor()

    # Valori predefiniti
    specifiche_possedute = {
        "RAM": ["4GB"],
        "CPU": ["A12"],
        "GPU": ["Mali-G76"],
        "Storage": ["64GB"],
    }

    # Carica dal database
    cursor.execute("SELECT categoria, specifica FROM specifiche_possedute")
    rows = cursor.fetchall()

    # Unisce le specifiche predefinite con quelle dal database
    for categoria, specifica in rows:
        if categoria not in specifiche_possedute:
            specifiche_possedute[categoria] = []
        if specifica not in specifiche_possedute[categoria]:  # Evita duplicati
            specifiche_possedute[categoria].append(specifica)

    conn.close()
    return specifiche_possedute


def carica_funzioni_possedute():
    conn = sqlite3.connect('devices_tycoon.db')
    cursor = conn.cursor()

    # Valori predefiniti
    funzioni_possedute = ["Face ID"]

    # Carica dal database
    cursor.execute("SELECT funzionalita FROM funzioni_possedute")
    rows = cursor.fetchall()

    # Unisce le funzionalità predefinite con quelle dal database
    for (funzionalita,) in rows:
        if funzionalita not in funzioni_possedute:  # Evita duplicati
            funzioni_possedute.append(funzionalita)

    conn.close()
    return funzioni_possedute



def VisualizzaSpecificheFunzionalita(specifc, func):
    print("\nSpecifiche possedute:")
    for categoria, specifiche in specifc.items():
        print(f"  {categoria}: {', '.join(specifiche)}")

    print("\nFunzionalità possedute:")
    if func:
        print(f"  {', '.join(func)}")
    else:
        print("  Nessuna funzionalità posseduta.")


def CompraSpecifiche(maxSpecifiche, specifc, studio_points):
    conn = sqlite3.connect('devices_tycoon.db')
    cursor = conn.cursor()

    while True:
        categorie = list(maxSpecifiche.keys())
        print("\nSpecifiche disponibili:")
        for i, categoria in enumerate(categorie, start=1):
            print(f"[{i}] {categoria}")
        print(f"[{len(categorie) + 1}] Torna indietro")

        print(f"\nHai {studio_points} studio_points.")
        scelta_categoria = ControllaInput("\nScegli una categoria (numero) -->| ", 
                                          list(range(1, len(categorie) + 2)), 
                                          "int")
        if scelta_categoria == len(categorie) + 1:
            print("Tornando al menu principale...")
            break

        categoria = categorie[scelta_categoria - 1]

        while True:
            opzioni = list(maxSpecifiche[categoria].keys())
            print(f"\nOpzioni disponibili per {categoria}:")
            for i, specifica in enumerate(opzioni, start=1):
                costo = maxSpecifiche[categoria][specifica]
                print(f"[{i}] {specifica} - {costo} studio_points")
            print(f"[{len(opzioni) + 1}] Torna indietro")

            scelta_opzione = ControllaInput(f"Scegli un'opzione per {categoria} (numero) -->| ", 
                                            list(range(1, len(opzioni) + 2)), 
                                            "int")
            if scelta_opzione == len(opzioni) + 1:
                print("Tornando alla lista delle categorie...")
                break

            specifica = opzioni[scelta_opzione - 1]
            costo = maxSpecifiche[categoria][specifica]

            if studio_points >= costo:
                studio_points -= costo
                specifc[categoria].append(specifica)
                del maxSpecifiche[categoria][specifica]

                # Aggiorna il database
                cursor.execute("DELETE FROM max_specifiche WHERE categoria = ? AND specifica = ?", 
                               (categoria, specifica))
                cursor.execute("INSERT INTO specifiche_possedute (categoria, specifica) VALUES (?, ?)", 
                               (categoria, specifica))
                conn.commit()

                print(f"Hai comprato {specifica} per {categoria} al costo di {costo} studio_points!")
                
                if not maxSpecifiche[categoria]:
                    del maxSpecifiche[categoria]
                break
            else:
                print("Non hai abbastanza punti studio.")

    conn.close()
    return specifc, studio_points

def CompraFunzionalita(maxFunzionalita, func, studio_points):
    conn = sqlite3.connect('devices_tycoon.db')
    cursor = conn.cursor()

    while True:
        # Ottieni l'elenco delle funzionalità
        funzionalita_disponibili = list(maxFunzionalita.keys())
        print("\nFunzionalità disponibili:")
        for i, funzionalita in enumerate(funzionalita_disponibili, start=1):
            costo = maxFunzionalita[funzionalita]
            print(f"[{i}] {funzionalita} - {costo} studio_points")
        print(f"[{len(funzionalita_disponibili) + 1}] Torna indietro")

        print(f"\nHai {studio_points} studio_points.")
        scelta_funzionalita = ControllaInput("\nScegli una funzionalità (numero) -->| ", 
                                             list(range(1, len(funzionalita_disponibili) + 2)), 
                                             "int")
        if scelta_funzionalita == len(funzionalita_disponibili) + 1:
            print("Tornando al menu principale...")
            break

        funzionalita = funzionalita_disponibili[scelta_funzionalita - 1]
        costo = maxFunzionalita[funzionalita]

        # Verifica e acquista
        if studio_points >= costo:
            studio_points -= costo
            func.append(funzionalita)
            del maxFunzionalita[funzionalita]

            # Aggiorna il database
            cursor.execute("DELETE FROM max_funzionalita WHERE funzionalita = ?", (funzionalita,))
            cursor.execute("INSERT INTO funzioni_possedute (funzionalita) VALUES (?)", (funzionalita,))
            conn.commit()

            print(f"Hai comprato la funzionalità {funzionalita} al costo di {costo} studio_points!")
        else:
            print("Non hai abbastanza punti studio.")

    conn.close()
    return func, studio_points

