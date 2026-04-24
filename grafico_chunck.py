import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CONFIGURAZIONE ESTETICA (per uniformare lo stile) ---
# Impostiamo un tema pulito e professionale
sns.set_theme(style="whitegrid")

# Parametri globali per i font (assicurati che siano leggibili)
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'font.family': 'sans-serif' # o 'serif' a seconda delle preferenze
})

# Colori aziendali/accademici
COLORE_LINEA = 'steelblue'
COLORE_PUNTI = 'darkred'

# --- CARICAMENTO DATI ---
# Sostituisci questo percorso con il tuo percorso reale se necessario
percorso_csv = r"/home/samuel/progetto_parallellizzazione/risultati_ott/chunck_size_ott.csv"

if os.path.exists(percorso_csv):
    print(f"Caricamento dati da: {percorso_csv}")
    df = pd.read_csv(percorso_csv)
else:
    print("File CSV non trovato. Generazione dati di esempio per l'illustrazione.")
    # Dati di esempio basati sulla nostra discussione (N=12000, 12 thread)
    data = {
        'Size': [1, 2, 3, 4, 5, 8, 16, 32],
        'Time': [26.2, 26.0, 25.58, 26.1, 26.1, 26.3, 28.5, 36.0]
    }
    df = pd.DataFrame(data)

# --- CREAZIONE DEL GRAFICO ---
# Creiamo la figura e gli assi
fig, ax = plt.subplots(figsize=(10, 6)) # Proporzioni ottimali per una relazione

# 1. Disegniamo la linea di tendenza
sns.lineplot(data=df, x='Size', y='Time', 
             color=COLORE_LINEA, linewidth=2.5, ax=ax)

# 2. Aggiungiamo i punti dati reali (per evidenziare i test effettuati)
sns.scatterplot(data=df, x='Size', y='Time', 
                color=COLORE_PUNTI, s=100, zorder=5, ax=ax)

# --- PERSONALIZZAZIONE ASSI E TITOLI ---
ax.set_title("Analisi Chunk Size (Schedule Dynamic)", pad=20, fontweight='bold')
ax.set_xlabel("Dimensione del Chunk", labelpad=10)
ax.set_ylabel("Differenza di tempo di esecuzione rispetto a size=1 (s)", labelpad=10)

# 3. TRUCCO FONDAMENTALE: Impostiamo le tacche X esattamente sui tuoi valori
# Di default Python userebbe una scala lineare sballata.
ax.set_xticks(df['Size'])
ax.set_xticklabels(df['Size']) # Assicuriamoci che i numeri siano scritti

# 4. EVIDENZIAMO IL PUNTO OTTIMALE (Chunk=3)
# Troviamo il valore minimo
min_time = df['Time'].min()
optimal_chunk = df[df['Time'] == min_time]['Size'].values[0]


# Pulizia finale
sns.despine(left=True, bottom=True) # Rimuove il bordo esterno per un look più moderno
plt.tight_layout() # Aggiusta automaticamente i margini

# --- SALVATAGGIO O VISUALIZZAZIONE ---
plt.savefig(os.path.join('grafici_finale', 'grafico_chunk_size.png'), dpi=300, bbox_inches='tight')
plt.close()
#plt.show()