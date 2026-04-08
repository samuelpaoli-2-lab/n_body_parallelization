import matplotlib.pyplot as plt
import numpy as np
import os

# 1. LETTURA E RAGGRUPPAMENTO DATI
dati_raccolti = {}
thread_attuale = None

with open('risultati_12000.txt', 'r') as file:
    for linea in file:
        if "Esecuzione con" in linea:
            thread_attuale = int(linea.split()[3])
            if thread_attuale not in dati_raccolti:
                dati_raccolti[thread_attuale] = []
        elif "Tempo di esecuzione:" in linea:
            tempo = float(linea.split(':')[1].strip())
            dati_raccolti[thread_attuale].append(tempo)

threads = sorted(dati_raccolti.keys())
etichette_threads = [str(t) for t in threads] # Per mantenere l'asse X spaziato omogeneamente

# 2. CALCOLI E PROPAGAZIONE ERRORE
medie_T = [np.mean(dati_raccolti[t]) for t in threads]
std_T = [np.std(dati_raccolti[t]) for t in threads]

T1 = medie_T[0]
std_T1 = std_T[0]

speedup_medie = []
speedup_err = []
efficienza_medie = []
efficienza_err = []

for i, p in enumerate(threads):
    Tp = medie_T[i]
    std_Tp = std_T[i]
    
    # Speedup: S = T1 / Tp
    S = T1 / Tp
    speedup_medie.append(S)
    
    # Incertezza Speedup (Propagazione)
    err_S = S * np.sqrt((std_T1/T1)**2 + (std_Tp/Tp)**2)
    speedup_err.append(err_S)
    
    # Efficienza: E = S / p
    E = S / p
    efficienza_medie.append(E)
    
    # Incertezza Efficienza
    err_E = err_S / p
    efficienza_err.append(err_E)

# 3. CREAZIONE DEI GRAFICI
plt.figure(figsize=(14, 6))

# Grafico 1: Speedup con incertezze
plt.subplot(1, 2, 1)
plt.errorbar(etichette_threads, speedup_medie, yerr=speedup_err, 
             fmt='o-', color='b', ecolor='red', elinewidth=2, capsize=5, label='Misurato')
# Disegniamo anche la retta ideale (Speedup = p)
plt.plot(etichette_threads, threads, linestyle='--', color='gray', label='Ideale') 

plt.title('Speedup N-Body con Incertezze')
plt.xlabel('Numero di Thread')
plt.ylabel('Speedup')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

# Grafico 2: Efficienza con incertezze
plt.subplot(1, 2, 2)
plt.errorbar(etichette_threads, efficienza_medie, yerr=efficienza_err, 
             fmt='s-', color='darkgreen', ecolor='red', elinewidth=2, capsize=5, label='Misurata')
plt.axhline(y=1.0, linestyle='--', color='gray', label='Ideale (1.0)')

plt.title('Efficienza N-Body con Incertezze')
plt.xlabel('Numero di Thread')
plt.ylabel('Efficienza')
plt.ylim(0, 1.1)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()
plt.tight_layout()

# 1. Definisci il nome della cartella
nome_cartella = 'grafici_salvati'

# 2. Crea la cartella se non esiste già
if not os.path.exists(nome_cartella):
    os.makedirs(nome_cartella)

# 3. Costruisci il percorso finale
# Consiglio: cambia il nome qui quando fai test con particelle diverse (es. _4000, _2000)
nome_file = os.path.join(nome_cartella, 'grafico_12000_particelle_s_e.png')

# 4. Salva il grafico dentro la cartella
plt.savefig(nome_file, dpi=300)
print(f"Fatto! Grafici esportati con successo in: '{nome_file}'")

plt.show()