import matplotlib.pyplot as plt
import numpy as np
import re
from collections import defaultdict
import os

# 1. Configurazione: nome del file di testo da leggere
NOME_FILE = 'risultati_16000.txt'

# Struttura per salvare i dati: results['static'][4] = [tempi...]
results = defaultdict(lambda: defaultdict(list))

# 2. Lettura e Parsing del file
with open(NOME_FILE, 'r') as file:
    current_thread = 0
    current_schedule = ""
    
    for line in file:
        # Cerca l'intestazione (es. "--- Esecuzione con 4 thread e schedule static---")
        match_header = re.search(r'Esecuzione con (\d+) thread e schedule (\w+)', line)
        if match_header:
            current_thread = int(match_header.group(1))
            current_schedule = match_header.group(2)
            continue
        
        # Cerca la riga del tempo (es. "Tempo di esecuzione: 44.317")
        match_time = re.search(r'Tempo di esecuzione:\s*([\d.]+)', line)
        if match_time and current_thread > 0:
            time_val = float(match_time.group(1))
            results[current_schedule][current_thread].append(time_val)

# 3. Preparazione del grafico
plt.figure(figsize=(10, 6))
colors = {'static': 'red', 'dynamic': 'blue', 'guided': 'green'}
markers = {'static': 'o', 'dynamic': 's', 'guided': '^'}

# Assicuriamoci di processare gli schedule in un ordine preciso per la legenda
for schedule in ['static', 'dynamic', 'guided']:
    if schedule not in results:
        continue
        
    threads = sorted(results[schedule].keys())
    means = []
    stds = []
    
    for t in threads:
        times = results[schedule][t]
        
        # --- RIMOZIONE OUTLIER (Trimmed Mean) ---
        # Se abbiamo almeno 4 dati, togliamo il max e il min per pulire le anomalie di Windows
        if len(times) > 3:
            times_puliti = sorted(times)[1:-1]
        else:
            times_puliti = times
            
        means.append(np.mean(times_puliti))
        stds.append(np.std(times_puliti))
        
    # Disegna la linea con le barre di errore
    plt.errorbar(threads, means, yerr=stds, fmt=f'-{markers[schedule]}', 
                 color=colors[schedule], label=f'Schedule {schedule.capitalize()}',
                 capsize=5, capthick=1.5, elinewidth=1.5, markersize=6)

# 4. Personalizzazione estetica del grafico
plt.title('Confronto Metodi di Scheduling (16000 particelle, 10 Run)', fontsize=14, fontweight='bold')
plt.xlabel('Numero di Thread', fontsize=12)
plt.ylabel('Tempo di esecuzione (secondi)', fontsize=12)

# Forza l'asse X a mostrare solo i valori reali dei thread usati
plt.xticks(threads) 

# Griglia e Legenda
plt.grid(True, linestyle=':', alpha=0.7, color='gray')
plt.legend(fontsize=11)

nome_cartella='grafici_no_lim'
if not os.path.exists(nome_cartella):
    os.makedirs(nome_cartella)

# 5. Salva l'immagine e mostrala
nome_immagine = os.path.join(nome_cartella, 'confronto_16000.png')
plt.tight_layout()
plt.savefig(nome_immagine, dpi=300)
print(f"Grafico salvato con successo come '{nome_immagine}'!")
plt.show()