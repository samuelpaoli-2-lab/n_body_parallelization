import matplotlib.pyplot as plt
import numpy as np
import os

# Dizionario per raggruppare i test: {1: [t1, t2...], 2: [t1, t2...]}
dati_raccolti = {}
thread_attuale = None

# 1. PARSING INTELLIGENTE
with open('risultati_12000.txt', 'r') as file:
    for linea in file:
        if "Esecuzione con" in linea:
            thread_attuale = int(linea.split()[3])
            if thread_attuale not in dati_raccolti:
                dati_raccolti[thread_attuale] = []
        elif "Tempo di esecuzione:" in linea:
            tempo = float(linea.split(':')[1].strip())
            dati_raccolti[thread_attuale].append(tempo)

# Prepariamo le liste per il grafico
threads = sorted(dati_raccolti.keys())
medie = [np.mean(dati_raccolti[t]) for t in threads]
deviazioni = [np.std(dati_raccolti[t]) for t in threads] # L'incertezza

# 2. CALCOLO SPEEDUP (basato sulla media del test a 1 thread)
media_T1 = medie[0]
speedup_medie = [media_T1 / m for m in medie]

# 3. GRAFICO CON BARRE D'ERRORE
plt.figure(figsize=(10, 6))

# Usiamo errorbar invece di plot
plt.errorbar(threads, medie, yerr=deviazioni, 
             fmt='o-',           # 'o' per il cerchio, '-' per la linea
             color='darkblue', 
             ecolor='red',       # Colore delle linee di incertezza
             elinewidth=2,       # Spessore linee incertezza
             capsize=5,          # Trattino orizzontale in cima e in fondo
             label='Tempo medio con Incertezza')

plt.title('Prestazioni N-Body: Tempo vs Thread (10 run per config)')
plt.xlabel('Numero di Thread')
plt.ylabel('Tempo di esecuzione (secondi)')
plt.xticks(threads)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

plt.tight_layout()

# 1. Definisci il nome della cartella
nome_cartella = 'grafici_salvati'

# 2. Crea la cartella se non esiste già
if not os.path.exists(nome_cartella):
    os.makedirs(nome_cartella)

# 3. Costruisci il percorso finale
# Consiglio: cambia il nome qui quando fai test con particelle diverse (es. _4000, _2000)
nome_file = os.path.join(nome_cartella, 'grafico_12000_particelle_t.png')

# 4. Salva il grafico dentro la cartella
plt.savefig(nome_file, dpi=300)
print(f"Fatto! Grafici esportati con successo in: '{nome_file}'")

plt.show()