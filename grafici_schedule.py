import matplotlib.pyplot as plt
import numpy as np
import os

# 1. IMPOSTAZIONI DEI TEST
# Associa il nome dello schedule al suo file di testo
file_schedules = {
    'Static': 'risultati_8000_static.txt',
    'Dynamic': 'risultati_8000_dynamic.txt',
    'Guided': 'risultati_8000_guided.txt'
}

# Colori per i diversi schedule
colori = {
    'Static': 'red', 
    'Dynamic': 'blue', 
    'Guided': 'green'
}

plt.figure(figsize=(10, 6))
print("Elaborazione dei file degli schedule in corso...")

# 2. CICLO SUGLI SCHEDULE
for nome_schedule, nome_file in file_schedules.items():
    
    if not os.path.exists(nome_file):
        print(f"  -> File '{nome_file}' non trovato. Controlla il nome!")
        continue
        
    dati_raccolti = {}
    
    # Lettura dei file
    with open(nome_file, 'r') as file:
        for linea in file:
            if "Esecuzione con" in linea:
                # Prende il numero di thread
                thread_attuale = int(linea.split()[3])
                if thread_attuale not in dati_raccolti:
                    dati_raccolti[thread_attuale] = []
            elif "Tempo di esecuzione:" in linea:
                # Prende il tempo
                tempo = float(linea.split(':')[1].strip())
                dati_raccolti[thread_attuale].append(tempo)

    # Calcolo medie e deviazioni standard
    if dati_raccolti:
        threads = sorted(dati_raccolti.keys())
        etichette_threads = [str(t) for t in threads]
        
        medie_T = [np.mean(dati_raccolti[t]) for t in threads]
        std_T = [np.std(dati_raccolti[t]) for t in threads]
        
        colore = colori.get(nome_schedule, 'gray')
        
        # Disegno della linea per questo schedule
        plt.errorbar(etichette_threads, medie_T, yerr=std_T, 
                     fmt='o-', color=colore, ecolor=colore, alpha=0.8,
                     elinewidth=2, capsize=5, label=f'Schedule {nome_schedule}')

# 3. DECORAZIONI DEL GRAFICO
plt.title('Confronto Prestazioni: Metodi di Scheduling (8000 particelle)')
plt.xlabel('Numero di Thread')
plt.ylabel('Tempo di esecuzione (secondi)')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

plt.tight_layout()

# 4. SALVATAGGIO
nome_cartella = 'grafici_salvati'
if not os.path.exists(nome_cartella):
    os.makedirs(nome_cartella)

nome_file_out = os.path.join(nome_cartella, 'confronto_8000_schedules.png')
plt.savefig(nome_file_out, dpi=300)
print(f"Successo! Grafico esportato in: '{nome_file_out}'")

plt.show()