#Gestione Tycoon Devices
#import funzioni
import funzioni as f
import database as db



db.crea_database()
money = 1000
studio_points = 30
id = 1
specifc = {
    "RAM": ["4GB",],
    "CPU": ["A12",],
    "GPU": ["Mali-G76",],
    "Storage": ["64GB",],
}

func = ["Face ID",]

maxSpecifiche = f.carica_max_specifiche()
maxFunzionalita = f.carica_max_funzionalita()
dispositivi = f.carica_dispositivi()
azienda = f.carica_azienda()
opzioni_dispositivi = ["Telefono"]

if azienda is None:
    nome_azienda = input('Inserisci il nome della tua azienda -->| ')
    f.aggiungi_azienda(nome_azienda, 1000, 30)  # Aggiungi una nuova azienda al database
else:
    nome_azienda, money, studio_points = azienda[1], azienda[2], azienda[3]

# Menu
scelta = 0
while scelta != 5:
    print("""\n
    [ 1 ] Azienda
    [ 2 ] Aggiungi Dispositivi
    [ 3 ] Visualizza Dispositivi
    [ 4 ] Compra Specifiche
    [ 5 ] Esci
        """)
    
    scelta = f.ControllaInput('Scegli un opzione -->| ', [1,2,3,4,5], 'int')

    if scelta == 1:
        f.VisualizzaAzienda(nome_azienda, money, studio_points)

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
                id,studio_points = f.AggiungiPhone(id, specifc, func,studio_points)  
                dispositivi = f.carica_dispositivi()
                break

            elif sceltaD == len(opzioni_dispositivi) + 1:
                print("Tornando al menu principale...")
                break

    elif scelta == 3:
        f.VisualizzaDevices()

    elif scelta == 4:
        while True:
            print("""
            [ 1 ] Compra Specifiche
            [ 2 ] Compra Funzionalità
            [ 3 ] Indietro
                  """)
            
            sceltaC = f.ControllaInput('Scegli un opzione -->| ', [1,2,3], 'int')

            if sceltaC == 1:
                specifc, studio_points = f.CompraSpecifiche(maxSpecifiche,specifc,studio_points)
                break

            elif sceltaC == 2:
                pass

            elif sceltaC == 3:
                print("Tornando al menu principale...")
                break