import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

data_completo=pd.read_csv("/home/samuel/progetto_parallellizzazione/Relazione/dati512thread.CSV", encoding = "latin1")
data_completo.columns = data_completo.columns.str.replace(r'\[.*?\]', '', regex=True)
data_completo.columns = data_completo.columns.str.strip()

data=data_completo[['Time', 'P-core 0 Clock', 'P-core 1 Clock', 'E-core 2 Clock', 'E-core 3 Clock', 'E-core 4 Clock', 'E-core 5 Clock', 'E-core 6 Clock', 'E-core 7 Clock', 'E-core 8 Clock', 'E-core 9 Clock',
                    "P-core 0","P-core 1","E-core 2","E-core 3","E-core 4","E-core 5","E-core 6","E-core 7","E-core 8","E-core 9", 'PCH Temperatura']].copy()
data.drop(data.tail(2).index, inplace=True)

tempi_assoluti = pd.to_timedelta(data['Time'].astype(str))
# b) Sottrae il primissimo valore a tutti gli altri, e lo converte in secondi (es. 0.0, 1.5, 3.2...)
data['Time'] = (tempi_assoluti - tempi_assoluti.iloc[0]).dt.total_seconds()

# --- 3. SOTTOCAMPIONAMENTO (Downsampling) ---
# Manteniamo una riga ogni 10 per pulire il grafico
#data = data.iloc[::2]

# --- 4. LAVATRICE DELLE ALTRE COLONNE ---
# Creiamo una lista di tutte le colonne TRANNE 'Time' (che ormai è perfetta)
colonne_sensori = [col for col in data.columns if col != 'Time']

for colonna in colonne_sensori:
    if data[colonna].dtype == 'object':
        data[colonna] = data[colonna].astype(str).str.replace(',', '.').str.strip()
    data[colonna] = pd.to_numeric(data[colonna], errors='coerce')

# 5. Puliamo le eventuali righe rimaste vuote/corrotte
data = data.dropna()

data = data[data['Time'] >= 60]
data['Time'] = data['Time'] - data['Time'].iloc[0]

cores = [
    "P-core 0", "P-core 1", 
    "E-core 2", "E-core 3", "E-core 4", "E-core 5", 
    "E-core 6", "E-core 7", "E-core 8", "E-core 9"
]

palette = sns.color_palette("husl", 11)

colori_core = {core: palette[i] for i, core in enumerate(cores)}
colori_core['PCH Temperatura'] = palette[10] 

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

for core in cores:
    nome_colonna_clock = f"{core} Clock"
    sns.lineplot(
        data=data, x='Time', y=nome_colonna_clock, 
        ax=ax1, color=colori_core[core], label=core
    )

ax1.set_title('Frequenza di Clock vs Tempo', fontsize=14, fontweight='bold')
ax1.set_ylabel('Frequenza [MHz]')
ax1.grid(True, alpha=0.3)
ax1.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title="Core")

for core in cores:
    nome_colonna_temp = core
    sns.lineplot(
        data=data, x='Time', y=nome_colonna_temp, 
        ax=ax2, color=colori_core[core], label=core
    )

sns.lineplot(
    data=data, x='Time', y='PCH Temperatura', 
    ax=ax2, color=colori_core['PCH Temperatura'], 
    label='PCH Temperatura', linestyle='--' 
)

ax2.set_title('Temperatura vs Tempo', fontsize=14, fontweight='bold')
ax2.set_xlabel('Tempo [s]')
ax2.set_ylabel('Temperatura [°C]')
ax2.grid(True, alpha=0.3)
ax2.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title="Sensore")
ax1.axvline(x=56, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
ax2.axvline(x=56, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
ax1.axvline(x=4, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
ax2.axvline(x=4, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)

plt.tight_layout() 
#plt.show()
plt.savefig(os.path.join('grafici_finale', 'cpu_single.png'), dpi=300, bbox_inches='tight')
plt.close()

#delta 52 s er cpu_single.png