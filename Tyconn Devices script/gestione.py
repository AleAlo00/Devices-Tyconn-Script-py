#Gestione Tycoon Devices
#import funzioni
import funzioni as f
import database as db



db.crea_database()
id = 1
char = ["RAM", "CPU", "GPU", "Storage"]
func = ["Face ID", "Touch ID", "Dual SIM", "5G"]
dispositivi = f.carica_dispositivi()
azienda = f.carica_azienda()

if azienda is None:
    nome_azienda = input('Inserisci il nome della tua azienda -->| ')
    f.aggiungi_azienda(nome_azienda, 1000, 30)  # Aggiungi una nuova azienda al database
else:
    nome_azienda, money, studio_points = azienda[1], azienda[2], azienda[3]

# Menu
scelta = 0
while scelta != 4:
    print("""\n
    [ 1 ] Azienda
    [ 2 ] Aggiungi Dispositivi
    [ 3 ] Visualizza Dispositivi
    [ 4 ] Esci
        """)
    
    scelta = f.ControllaInput('Scegli un opzione -->| ', [1,2,3,4], 'int')

    if scelta == 1:
        f.VisualizzaAzienda(nome_azienda, money, studio_points)

    elif scelta == 2:
        id = f.AggiungiPhone(id, char, func)  # Aggiungi il dispositivo e aggiorna l'ID
        dispositivi = f.carica_dispositivi()

    elif scelta == 3:
        f.VisualizzaDevices(dispositivi)