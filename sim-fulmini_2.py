import time
from datetime import datetime
import pyrebase
import random

# Inizializzazione delle credenziali Firebase
config = {
    "apiKey": "AIzaSyCjtTR-s_bzCSlTkcx3QiTPJEl8E_VPJ5Y",
    "authDomain": "prova-2-2588a.firebaseapp.com",
    "databaseURL": "https://prova-2-2588a-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "prova-2-2588a.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Inizializza la variabile per il conteggio totale dei fulmini
total_lightning = 0

# Inizializza la variabile per l'ID dell'ultimo elemento inviato
last_push_id = 0

# Funzione di callback per la gestione degli interrupt
while True:
    # Simulating interrupt source
    intSrc = random.randint(1, 3)

    if intSrc == 1:
        # Caso in cui l'interrupt è causato da un fulmine simulato
        lightning_distKm = round(random.uniform(1, 40), 1)
        print('Lightning occurs!')
        print('Distance: %.1fkm' % lightning_distKm)

        lightning_energy_val = random.randint(1, 100)
        print('Intensity: %d ' % lightning_energy_val)

        # Aggiorna il conteggio totale dei fulmini
        total_lightning += 1

        # Invia dati a Firebase
        current_year = datetime.now().year
        current_month = datetime.now().month
        path = f'/nuovo-percorso/{current_year:04d}/{current_month:02d}'

        if last_push_id == 0:
            existing_data = db.child(path).get().val()
        else:
            existing_data = db.child(path).order_by_key().start_at(last_push_id).get().val()

        if existing_data:
            # Trova l'ID dell'ultimo elemento
            last_push_id = list(existing_data.keys())[-1]
            new_push_id = int(last_push_id.split('_')[-1]) + 1
        else:
            # Se non ci sono dati esistenti, inizia con 1
            new_push_id = 1

        push_id = f'Push_ID_{new_push_id:04d}'

        data_to_push = {
            push_id: {
                'value': f'Year: {current_year}, Month: {current_month:02d}, Distance: {lightning_distKm} km, Timestamp: {str(datetime.now())}, Total Lightning: {total_lightning}'
            }
        }

        db.child(path).update(data_to_push)
        print(f'Lightning data sent to Firebase at {path}')

        # Aggiorna il numero totale di fulmini nell'anno
        year_path = f'/nuovo-percorso/{current_year:04d}/total_lightning'
        current_total_year_lightning = db.child(year_path).get().val() or 0
        current_total_year_lightning += 1
        db.child(year_path).set(current_total_year_lightning)

    elif intSrc == 2:
        # Caso in cui l'interrupt è causato dalla rilevazione di un disturbo simulato
        print('Disturber discovered!')

    elif intSrc == 3:
        # Caso in cui l'interrupt è causato da un livello di rumore troppo alto simulato
        print('Noise level too high!')

    else:
        # Altro caso (non dovrebbe verificarsi)
        pass

    time.sleep(1.0)