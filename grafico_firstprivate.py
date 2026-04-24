import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- STILE E CONFIGURAZIONE ---
# Manteniamo esattamente lo stesso stile dei tuoi grafici precedenti
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12
})

# --- CARICAMENTO DATI ---
# Inserisci i nomi corretti dei tuoi due file CSV
df_shared = pd.read_csv("risultati_ott/risultati_20000_fin.csv", skipinitialspace=True)
df_first = pd.read_csv("risultati_ott/risultati_20000_firstprivate.csv", skipinitialspace=True)

# Pulizia dei nomi delle colonne
df_shared.columns = df_shared.columns.str.strip()
df_first.columns = df_first.columns.str.strip()

# --- ELABORAZIONE DATI ---
# Creiamo il dataframe finale per il grafico
df = pd.DataFrame()
df['Thread'] = df_shared['Thread']

# Rimuoviamo eventuali virgolette dai nomi dello schedule (es. da "static" a static)
df['Schedule'] = df_shared['Schedule'].str.replace('"', '') 

# Calcoliamo la differenza: Time(firstprivate) - Time(shared)
# Un valore positivo significa che firstprivate è stato PIU' LENTO.
df['Differenza_Tempo'] = df_first['Time'] - df_shared['Time']

# --- CREAZIONE DEL GRAFICO ---
fig, ax = plt.subplots(figsize=(10, 6))

# Disegniamo le 3 linee (static, dynamic, guided)
sns.lineplot(
    data=df, 
    x='Thread', 
    y='Differenza_Tempo', 
    hue='Schedule', 
    marker='o',       # Aggiunge i pallini sui punti dati
    linewidth=2.5,
    markersize=8,
    ax=ax
)

# Aggiungiamo una linea di riferimento sullo ZERO
# Tutto ciò che sta sopra questa linea è tempo "sprecato" da firstprivate
ax.axhline(0, color='black', linestyle='--', linewidth=1.5, zorder=1)

# --- PERSONALIZZAZIONE ASSI ---
ax.set_title("Differenza Firstprivate - Shared (20000 corpi)", pad=20, fontweight='bold')
ax.set_xlabel("Numero di Thread", labelpad=10)
ax.set_ylabel("Rallentamento (s)", labelpad=10)

# Mettiamo l'asse X in scala logaritmica (base 2) per spaziare perfettamente i tuoi thread
ax.set_xscale('log', base=2)
thread_ticks = df['Thread'].unique()
ax.set_xticks(thread_ticks)
ax.set_xticklabels(thread_ticks)

# Miglioriamo l'aspetto della legenda
ax.legend(title='Schedule', frameon=True)

plt.tight_layout()

plt.savefig(os.path.join('grafici_finale', 'grafico_20000_sh_first.png'), dpi=300, bbox_inches='tight')
plt.close()

plt.show()