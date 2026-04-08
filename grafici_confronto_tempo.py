import matplotlib.pyplot as plt
import numpy as np
import os

# 1. IMPOSTAZIONI DEI TEST
test_eseguiti = {
    8000: 'risultati_8000.txt',
    4000: 'risultati_4000.txt',
    2000: 'risultati_2000.txt',
    1000: 'risultati_1000.txt'
}

colori = {
    8000: 'darkblue', 
    4000: 'darkgreen', 
    2000: 'darkorange',
    1000: 'purple'
}

# Prepariamo una singola "tela" per i tempi
plt.figure(figsize=(10, 6))

print("Elaborazione dei file per i tempi...")

# 2. CICLO DI LETTURA E DISEGNO
for particelle, nome_file in test_eseguiti.items():
    
    if not os.path.exists(nome_file):
        print(f"  -> File '{nome_file}' non trovato. Lo salto.")
        continue
        
    dati_raccolti = {}
    
    with open(nome_file, 'r') as file:
        for linea in file:
            if "Esecuzione con" in linea:
                thread_attuale = int(linea.split()[3])
                if thread_attuale not in dati_raccolti:
                    dati_raccolti[thread_attuale] = []
            elif "Tempo di esecuzione:" in linea:
                tempo = float(linea.split(':')[1].strip())
                dati_raccolti[thread_attuale].append(tempo)

    # Matematica base (Media e Incertezza)
    if dati_raccolti:
        threads = sorted(dati_raccolti.keys())
        etichette_threads = [str(t) for t in threads]
        
        medie_T = [np.mean(dati_raccolti[t]) for t in threads]
        std_T = [np.std(dati_raccolti[t]) for t in threads]

        colore = colori.get(particelle, 'gray')
        
        # Disegnamo la linea per questo numero di particelle
        plt.errorbar(etichette_threads, medie_T, yerr=std_T, 
                     fmt='o-', color=colore, ecolor=colore, 
                     alpha=0.8, elinewidth=2, capsize=5, 
                     label=f'{particelle} particelle')

# 3. TOCCHI FINALI
plt.title('Confronto Tempi di Esecuzione N-Body')
plt.xlabel('Numero di Thread')
plt.ylabel('Tempo di esecuzione (secondi)')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

plt.tight_layout()

# 4. SALVATAGGIO
nome_cartella = 'grafici_salvati'
if not os.path.exists(nome_cartella):
    os.makedirs(nome_cartella)

nome_file_out = os.path.join(nome_cartella, 'confronto_tempi_esecuzione.png')
plt.savefig(nome_file_out, dpi=300)
print(f"Successo! Grafico dei tempi esportato in: '{nome_file_out}'")

plt.show()