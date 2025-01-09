#Gestione Tycoon Devices
#import funzioni
import funzioniSpecificheFunzionalità as f
import funzioniAzienda as fA
import funzioniDevices as fD
import database as db

# Inizializza il database
db.crea_database()

# Variabili iniziali
money = 1000
studio_points = 30
id = 1
nome_azienda = None  # Inizializza come None
id_azienda = None  # Inizializza come None

# Carica specifiche e funzionalità massime
maxSpecifiche = f.carica_max_specifiche()
maxFunzionalita = f.carica_max_funzionalita()

# Carica specifiche e funzionalità possedute
specifc = f.carica_specifiche_possedute()
func = f.carica_funzioni_possedute()

# Carica dispositivi
dispositivi = fD.carica_dispositivi(id_azienda)
azienda = fA.carica_azienda()
azienda = fA.carica_azienda(nome_azienda)

if azienda:
    nome_azienda = azienda['nome']
    money = azienda['money']
    studio_points = azienda['studio_points']
    id_azienda = fA.ottieni_id_azienda(nome_azienda)  # Aggiungi questa riga
    print(f"L'azienda '{nome_azienda}' è stata caricata con successo!")
else:
    id_azienda = None  # Nel caso in cui non ci sia nessuna azienda
    print("Nessuna azienda disponibile da caricare.")


opzioni_dispositivi = ["Telefono"]

if azienda is not None:
    nome_azienda, money, studio_points = azienda['nome'], azienda['money'], azienda['studio_points']


# Menu
scelta = 0
while scelta != 7:
    # Controlla se l'azienda esiste
    if nome_azienda is None:
        print("\nNon esiste un'azienda. Creane una nuova per continuare.")
        nome_azienda = input('Inserisci il nome della tua azienda -->| ')
        fA.aggiungi_azienda(nome_azienda, 1000, 30)
        money = 1000
        studio_points = 30
        continue  # Ritorna all'inizio del ciclo principale
    
    print("""\n
    [ 1 ] Azienda
    [ 2 ] Aggiungi Dispositivi
    [ 3 ] Visualizza Dispositivi
    [ 4 ] Compra Specifiche
    [ 5 ] Visualizza Specifiche e Funzionalità
    [ 6 ] Impostazioni
    [ 7 ] Esci
        """)
    
    scelta = fD.ControllaInput('Scegli un opzione -->| ', [1, 2, 3, 4, 5, 6, 7], 'int')

    if scelta == 1:
        fA.VisualizzaAzienda(nome_azienda, money, studio_points)

    elif scelta == 2:
        while True:
            print("\n")
            for i, opzione in enumerate(opzioni_dispositivi, start=1):
                print(f"[ {i} ] {opzione}")
            print(f"[ {len(opzioni_dispositivi) + 1} ] Indietro")
            
            sceltaD = f.ControllaInput('Scegli un dispositivo da aggiungere -->| ', 
                                    list(range(1, len(opzioni_dispositivi) + 2)), 
                                    'int')
            
            if sceltaD == 1:
                id_azienda = fA.ottieni_id_azienda(nome_azienda)  # Recupera l'ID azienda
                id, studio_points = fD.AggiungiPhone(id, specifc, func, studio_points, maxSpecifiche, id_azienda)
                dispositivi = fD.carica_dispositivi(id_azienda)  # Passa id_azienda qui
                break



            elif sceltaD == len(opzioni_dispositivi) + 1:
                print("Tornando al menu principale...")
                break

    elif scelta == 3:
        fD.VisualizzaDevices(id_azienda)

    elif scelta == 4:
        while True:
            print("""
            [ 1 ] Compra Specifiche
            [ 2 ] Compra Funzionalità
            [ 3 ] Indietro
                  """)
            
            sceltaC = fD.ControllaInput('Scegli un opzione -->| ', [1, 2, 3], 'int')

            if sceltaC == 1:
                specifc, studio_points = f.CompraSpecifiche(maxSpecifiche, specifc, studio_points)
                break

            elif sceltaC == 2:
                func, studio_points = f.CompraFunzionalita(maxFunzionalita, func, studio_points)
                break

            elif sceltaC == 3:
                print("Tornando al menu principale...")
                break

    elif scelta == 5:
        f.VisualizzaSpecificheFunzionalita(specifc, func)
    
    elif scelta == 6:
        while True:
            print("""
            [ 1 ] Elimina Azienda
            [ 2 ] Elimina Dispositivi
            [ 3 ] Nuova Azienda
            [ 4 ] Carica Azienda
            [ 5 ] Indietro
                  """)
            
            sceltaE = fD.ControllaInput('Scegli un opzione -->| ', [1, 2, 3, 4, 5], 'int')

            if sceltaE == 1:  # Elimina Azienda
                conferma = input("Sei sicuro di voler eliminare l'azienda? Tutti i dati andranno persi! (y/n) -->| ").lower()
                if conferma == 'y':
                    fA.elimina_azienda()
                    print("Azienda eliminata con successo!")
                    nome_azienda = None
                    money = 0
                    studio_points = 0
                    exit()
                else:
                    print("Operazione annullata.")
            
            elif sceltaE == 2:  # Elimina Dispositivi
                dispositivi = fD.carica_dispositivi()
                if not dispositivi:
                    print("Non ci sono dispositivi da eliminare.")
                else:
                    print("\nDispositivi disponibili:")
                    for i, dispositivo in enumerate(dispositivi, start=1):
                        print(f"[ {i} ] {dispositivo[1]}")
                    print(f"[ {len(dispositivi) + 1} ] Indietro")
                    
                    sceltaD = fD.ControllaInput("Scegli un dispositivo da eliminare (numero) -->| ", 
                                               list(range(1, len(dispositivi) + 2)), 
                                               "int")
                    
                    if sceltaD == len(dispositivi) + 1:
                        print("Tornando al menu precedente...")
                    else:
                        dispositivo_id = dispositivi[sceltaD - 1][0]
                        fD.elimina_dispositivo(dispositivo_id)
                        print(f"Dispositivo {dispositivi[sceltaD - 1][1]} eliminato con successo!")

            elif sceltaE == 3:  # Nuova Azienda
                nome_azienda_nuova = input("Inserisci il nome della nuova azienda -->| ")
                if fA.esiste_azienda(nome_azienda_nuova):  # Controlla se il nome è già usato
                    print("Un'azienda con questo nome esiste già. Scegli un altro nome.")
                else:
                    fA.aggiungi_azienda(nome_azienda_nuova, 1000, 30)  # Valori iniziali
                    print(f"Nuova azienda '{nome_azienda_nuova}' creata con successo!")
                    
                    # Carica l'azienda appena creata
                    azienda = fA.carica_azienda(nome_azienda_nuova)
                    if azienda:  # Verifica se il caricamento ha avuto successo
                        nome_azienda = azienda['nome']
                        money = azienda['money']
                        studio_points = azienda['studio_points']
                        print(f"L'azienda '{nome_azienda}' è stata caricata con successo!")
                        break
                    else:
                        print("Errore durante il caricamento dell'azienda.")
                    break


            elif sceltaE == 4:  # Carica Azienda
                aziende = fA.lista_aziende()
                if not aziende:
                    print("Non ci sono aziende disponibili da caricare.")
                else:
                    print("\nAziende disponibili:")
                    for i, azienda in enumerate(aziende, start=1):
                        print(f"[ {i} ] {azienda[1]}")  # Mostra il nome dell'azienda
                    print(f"[ {len(aziende) + 1} ] Indietro")
                    
                    sceltaA = fD.ControllaInput("Scegli un'azienda da caricare (numero) -->| ", 
                                                list(range(1, len(aziende) + 2)), 
                                                "int")
                    
                    if sceltaA == len(aziende) + 1:
                        print("Tornando al menu precedente...")
                    else:
                        azienda = aziende[sceltaA - 1]
                        nome_azienda, money, studio_points = azienda[1], azienda[2], azienda[3]
                        id_azienda = azienda[0]  # Aggiorna id_azienda
                        dispositivi = fD.carica_dispositivi(id_azienda)  # Filtra i dispositivi per azienda
                        print(f"Azienda '{nome_azienda}' caricata con successo!")
                        break

            
            elif sceltaE == 5:  # Torna indietro
                print("Tornando al menu principale...")
                break
