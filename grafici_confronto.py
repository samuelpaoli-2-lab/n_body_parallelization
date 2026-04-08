import matplotlib.pyplot as plt
import numpy as np
import os

# 1. IMPOSTAZIONI DEI TEST
# Qui inserisci il numero di particelle e il nome esatto del file txt corrispondente
test_eseguiti = {
    12000: 'risultati_12000.txt',
    8000: 'risultati_8000.txt',
    4000: 'risultati_4000.txt',
    2000: 'risultati_2000.txt',
    1000: 'risultati_1000.txt'
}

# Scegliamo dei colori diversi per le varie linee
colori = {12000: 'brown', 8000: 'darkblue', 4000: 'darkgreen', 2000: 'darkorange', 1000: 'darkviolet'}

# Prepariamo la "tela" vuota con due spazi (Speedup ed Efficienza)
plt.figure(figsize=(14, 6))
ax1 = plt.subplot(1, 2, 1) # Grafico a sinistra
ax2 = plt.subplot(1, 2, 2) # Grafico a destra

print("Elaborazione dei file in corso...")

# 2. CICLO SU TUTTI I FILE
for particelle, nome_file in test_eseguiti.items():
    
    # Controlliamo che il file esista per evitare crash
    if not os.path.exists(nome_file):
        print(f"  -> File '{nome_file}' non trovato. Lo salto.")
        continue
        
    dati_raccolti = {}
    thread_attuale = None

    # Lettura e Parsing
    with open(nome_file, 'r') as file:
        for linea in file:
            if "Esecuzione con" in linea:
                thread_attuale = int(linea.split()[3])
                if thread_attuale not in dati_raccolti:
                    dati_raccolti[thread_attuale] = []
            elif "Tempo di esecuzione:" in linea:
                tempo = float(linea.split(':')[1].strip())
                dati_raccolti[thread_attuale].append(tempo)

    # Matematica (solo se abbiamo trovato dati)
    if dati_raccolti:
        threads = sorted(dati_raccolti.keys())
        etichette_threads = [str(t) for t in threads]
        
        medie_T = [np.mean(dati_raccolti[t]) for t in threads]
        std_T = [np.std(dati_raccolti[t]) for t in threads]
        T1, std_T1 = medie_T[0], std_T[0]

        speedup_medie, speedup_err = [], []
        efficienza_medie, efficienza_err = [], []

        for i, p in enumerate(threads):
            Tp, std_Tp = medie_T[i], std_T[i]
            
            S = T1 / Tp
            err_S = S * np.sqrt((std_T1/T1)**2 + (std_Tp/Tp)**2)
            
            speedup_medie.append(S)
            speedup_err.append(err_S)
            
            E = S / p
            efficienza_medie.append(E)
            efficienza_err.append(err_S / p)

        # 3. DISEGNAMO LE LINEE (Aggiungiamo un livello per ogni ciclo)
        colore = colori.get(particelle, 'gray')
        
        ax1.errorbar(etichette_threads, speedup_medie, yerr=speedup_err, 
                     fmt='o-', color=colore, ecolor=colore, alpha=0.8,
                     label=f'{particelle} particelle')
                     
        ax2.errorbar(etichette_threads, efficienza_medie, yerr=efficienza_err, 
                     fmt='s-', color=colore, ecolor=colore, alpha=0.8,
                     label=f'{particelle} particelle')

# 4. TOCCHI FINALI E DECORAZIONI (Fuori dal ciclo!)

# Grafico Speedup
ax1.plot(etichette_threads, threads, linestyle='--', color='black', alpha=0.5, label='Ideale')
ax1.set_title('Confronto Speedup N-Body')
ax1.set_xlabel('Numero di Thread')
ax1.set_ylabel('Speedup')
ax1.grid(True, linestyle=':', alpha=0.7)
ax1.legend()

# Grafico Efficienza
ax2.axhline(y=1.0, linestyle='--', color='black', alpha=0.5, label='Ideale (100%)')
ax2.set_title('Confronto Efficienza N-Body')
ax2.set_xlabel('Numero di Thread')
ax2.set_ylabel('Efficienza')
ax2.set_ylim(0, 1.1)
ax2.grid(True, linestyle=':', alpha=0.7)
ax2.legend()

plt.tight_layout()

# 5. SALVATAGGIO
nome_cartella = 'grafici_salvati'
if not os.path.exists(nome_cartella):
    os.makedirs(nome_cartella)

nome_file_out = os.path.join(nome_cartella, 'confronto_scaling_forte.png')
plt.savefig(nome_file_out, dpi=300)
print(f"Successo! Grafico di confronto esportato in: '{nome_file_out}'")

plt.show()