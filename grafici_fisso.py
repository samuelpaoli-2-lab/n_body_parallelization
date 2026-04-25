import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

data_4000 = pd.read_csv("/home/samuel/progetto_parallellizzazione/risultati_ott/risultati_4000_fin_fisso.csv")

plt.figure(figsize=(10, 6))
g_4000=sns.lineplot(data=data_4000, x='Thread', y='Time', hue='Schedule', marker='o')
g_4000.set_xscale('log', base=2)
g_4000.set_xticks([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_4000.set_xticklabels([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_4000.grid(True)
g_4000.set_xlabel("Numero di Thread")
g_4000.set_ylabel("Tempo (s)")
g_4000.set_title("Tempi con 4000 corpi")
plt.savefig(os.path.join('grafici_finale', 'tempi_4000_fin_fisso.png'), dpi=300, bbox_inches='tight')
plt.close()

data_12000 = pd.read_csv("/home/samuel/progetto_parallellizzazione/risultati_ott/risultati_12000_fin_fisso.csv")

plt.figure(figsize=(10, 6))
g_8000=sns.lineplot(data=data_12000, x='Thread', y='Time', hue='Schedule', marker='o')
g_8000.set_xscale('log', base=2)
g_8000.set_xticks([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_8000.set_xticklabels([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_8000.grid(True)
g_8000.set_xlabel("Numero di Thread")
g_8000.set_ylabel("Tempo (s)")
g_8000.set_title("Tempi con 12000 corpi")
plt.savefig(os.path.join('grafici_finale', 'tempi_12000_fin_fisso.png'), dpi=300, bbox_inches='tight')
plt.close()

data_20000 = pd.read_csv("/home/samuel/progetto_parallellizzazione/risultati_ott/risultati_20000_fin_fisso.csv")

plt.figure(figsize=(10, 6))
g_12000=sns.lineplot(data=data_20000, x='Thread', y='Time', hue='Schedule', marker='o')
g_12000.set_xscale('log', base=2)
g_12000.set_xticks([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_12000.set_xticklabels([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_12000.grid(True)
g_12000.set_xlabel("Numero di Thread")
g_12000.set_ylabel("Tempo (s)")
g_12000.set_title("Tempi con 20000 corpi")
plt.savefig(os.path.join('grafici_finale', 'tempi_20000_fin_fisso.png'), dpi=300, bbox_inches='tight')
plt.close()

dataset_dict = {

    '4000': data_4000, 
    '12000': data_12000, 
    '20000': data_20000
}

lista_per_unione = []

for nome, df in dataset_dict.items():
    
    t1 = df[df['Thread'] == 1].set_index('Schedule')['Time']
    df['Speedup'] = df['Schedule'].map(t1) / df['Time']
    
    df['Dimensione'] = nome
    
    lista_per_unione.append(df)

df_totale = pd.concat(lista_per_unione)



# hue: cambia il COLORE in base allo Schedule
# style: cambia il MARKER/TRATTO in base alla Dimensione
sns.set_theme(style="whitegrid")
g_speedup = sns.relplot(
    data=df_totale, 
    x='Thread', 
    y='Speedup', 
    hue='Dimensione',    # Colore diverso per ogni dimensione
    style='Dimensione',  # Marker diverso per ogni dimensione (utile se stampi in bianco e nero)
    col='Schedule',      # <-- IL SEGRETO: crea un riquadro per ogni Schedule!
    kind='line', 
    markers=True, 
    height=5,            # Altezza di ogni singolo riquadro
    aspect=1.1           # Proporzione (larghezza leggermente maggiore dell'altezza)
)

# Impostazioni asse X (Log2 come volevi tu)
g_speedup.set(xscale='log') 
valori_thread = [1, 2, 4, 8, 12, 16, 32, 64, 128, 256]
g_speedup.set(xticks=valori_thread)
g_speedup.set_xticklabels(valori_thread, rotation=45)
g_speedup.set_axis_labels("Numero di Thread", "Speedup")
g_speedup.set_titles(col_template="Confronto speedup con schedule {col_name}")

g_speedup.savefig(os.path.join('grafici_finale', 'confronto_speedup_fin_fisso.png'), dpi=300, bbox_inches='tight')

plt.close()

lista_per_unione_eff = []

for nome, df in dataset_dict.items():
    
    df['Efficienza'] = df['Speedup'] / df['Thread']
    
    df['Dimensione'] = nome
    
    lista_per_unione_eff.append(df)

df_totale_eff = pd.concat(lista_per_unione_eff)

sns.set_theme(style="whitegrid")
g_eff = sns.relplot(
    data=df_totale_eff, 
    x='Thread', 
    y='Efficienza', 
    hue='Dimensione',    
    style='Dimensione',  
    col='Schedule',      
    kind='line', 
    markers=True, 
    height=5,           
    aspect=1.1           
)

g_eff.set(xscale='log') 
g_eff.set(xticks=valori_thread)
g_eff.set_xticklabels(valori_thread, rotation=45)
g_eff.set_axis_labels("Numero di Thread", "Efficienza (Speedup / Thread)")
g_eff.set_titles(col_template="Confronto efficienza con schedule {col_name}")

g_eff.savefig(os.path.join('grafici_finale', 'confronto_eff_fin_fisso.png'), dpi=300, bbox_inches='tight')

plt.close()