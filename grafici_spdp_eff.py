import matplotlib.pyplot as plt
import numpy as np
import re
from collections import defaultdict
import os

# 1. Configurazione
NOME_FILE = 'risultati_8000_fisso_2.txt'
results = defaultdict(lambda: defaultdict(list))

# 2. Lettura e Parsing (Stessa logica di pulizia)
with open(NOME_FILE, 'r') as file:
    current_thread = 0
    current_schedule = ""
    for line in file:
        match_header = re.search(r'Esecuzione con (\d+) thread e schedule (\w+)', line)
        if match_header:
            current_thread = int(match_header.group(1))
            current_schedule = match_header.group(2)
            continue
        match_time = re.search(r'Tempo di esecuzione:\s*([\d.]+)', line)
        if match_time and current_thread > 0:
            time_val = float(match_time.group(1))
            results[current_schedule][current_thread].append(time_val)

# Calcolo delle medie pulite
means_data = defaultdict(dict)
for schedule in results:
    for t in results[schedule]:
        times = results[schedule][t]
        if len(times) > 3:
            times_puliti = sorted(times)[1:-1] # Rimuove max e min
        else:
            times_puliti = times
        means_data[schedule][t] = np.mean(times_puliti)

# 3. Preparazione della figura doppia
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
colors = {'static': 'red', 'dynamic': 'blue', 'guided': 'green'}
markers = {'static': 'o', 'dynamic': 's', 'guided': '^'}
thread_list = sorted(list(means_data['static'].keys()))

# --- GRAFICO 1: SPEEDUP ---
# Linea ideale dello speedup (y = x)
ax1.plot(thread_list, thread_list, 'k--', label='Speedup Ideale', linewidth=2, alpha=0.7)

for schedule in ['static', 'dynamic', 'guided']:
    if schedule not in means_data: continue
    
    # Prende il tempo a 1 thread di questo schedule come T1
    T1 = means_data[schedule][1]
    speedups = [T1 / means_data[schedule][t] for t in thread_list]
    
    ax1.plot(thread_list, speedups, marker=markers[schedule], color=colors[schedule], 
             label=f'{schedule.capitalize()}', linewidth=2, markersize=8)

ax1.set_title('Speedup ($S = T_1 / T_p$)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Numero di Thread', fontsize=12)
ax1.set_ylabel('Speedup', fontsize=12)
ax1.set_xticks(thread_list)
ax1.grid(True, linestyle=':', alpha=0.7)
ax1.legend(fontsize=11)

# --- GRAFICO 2: EFFICIENZA ---
# Linea ideale dell'efficienza (y = 1)
ax2.axhline(y=1.0, color='k', linestyle='--', label='Efficienza Ideale (1.0)', linewidth=2, alpha=0.7)

for schedule in ['static', 'dynamic', 'guided']:
    if schedule not in means_data: continue
    
    T1 = means_data[schedule][1]
    efficiencies = [(T1 / means_data[schedule][t]) / t for t in thread_list]
    
    ax2.plot(thread_list, efficiencies, marker=markers[schedule], color=colors[schedule], 
             label=f'{schedule.capitalize()}', linewidth=2, markersize=8)

ax2.set_title('Efficienza ($E = S / p$)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Numero di Thread', fontsize=12)
ax2.set_ylabel('Efficienza', fontsize=12)
ax2.set_xticks(thread_list)
ax2.grid(True, linestyle=':', alpha=0.7)
ax2.legend(fontsize=11)

# 4. Salvataggio
nome_cartella='grafici_no_lim'
if not os.path.exists(nome_cartella):
    os.makedirs(nome_cartella)

plt.tight_layout()
nome_immagine = os.path.join(nome_cartella, 'speedup_efficienza_8000_fisso_2.png')
plt.savefig(nome_immagine, dpi=300)
print(f"Grafico salvato con successo come '{nome_immagine}'!")
plt.show()