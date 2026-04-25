import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

data_4000_fisso = pd.read_csv("/home/samuel/progetto_parallellizzazione/risultati_ott/risultati_4000_fin_fisso.csv")
data_4000 = pd.read_csv("/home/samuel/progetto_parallellizzazione/risultati_ott/risultati_4000_fin.csv")

df_4000=pd.DataFrame()
df_4000['Thread']=data_4000['Thread']
df_4000['Schedule']=data_4000['Schedule']
df_4000['Time']=data_4000_fisso['Time']-data_4000['Time']

plt.figure(figsize=(10, 6))
g_4000=sns.lineplot(data=df_4000, x='Thread', y='Time', hue='Schedule', marker='o')
g_4000.set_xscale('log', base=2)
g_4000.set_xticks([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_4000.set_xticklabels([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_4000.grid(True)
g_4000.set_xlabel("Numero di Thread")
g_4000.set_ylabel("Tempo (s)")
g_4000.set_title("Differenza fra portatile e pc fisso (4000 corpi)")
plt.savefig(os.path.join('grafici_finale', 'confronto_tempi_fin_4000.png'), dpi=300, bbox_inches='tight')
plt.close()

data_12000_fisso = pd.read_csv("/home/samuel/progetto_parallellizzazione/risultati_ott/risultati_12000_fin_fisso.csv")
data_12000 = pd.read_csv("/home/samuel/progetto_parallellizzazione/risultati_ott/risultati_12000_fin.csv")

df_12000=pd.DataFrame()
df_12000['Thread']=data_12000['Thread']
df_12000['Schedule']=data_12000['Schedule']
df_12000['Time']=data_12000_fisso['Time']-data_12000['Time']

plt.figure(figsize=(10, 6))
g_12000=sns.lineplot(data=df_12000, x='Thread', y='Time', hue='Schedule', marker='o')
g_12000.set_xscale('log', base=2)
g_12000.set_xticks([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_12000.set_xticklabels([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_12000.grid(True)
g_12000.set_xlabel("Numero di Thread")
g_12000.set_ylabel("Tempo (s)")
g_12000.set_title("Differenza fra portatile e pc fisso (12000 corpi)")
plt.savefig(os.path.join('grafici_finale', 'confronto_tempi_fin_12000.png'), dpi=300, bbox_inches='tight')
plt.close()

data_20000_fisso = pd.read_csv("/home/samuel/progetto_parallellizzazione/risultati_ott/risultati_20000_fin_fisso.csv")
data_20000 = pd.read_csv("/home/samuel/progetto_parallellizzazione/risultati_ott/risultati_20000_fin.csv")

df_20000=pd.DataFrame()
df_20000['Thread']=data_20000['Thread']
df_20000['Schedule']=data_20000['Schedule']
df_20000['Time']=data_20000_fisso['Time']-data_20000['Time']

plt.figure(figsize=(10, 6))
g_20000=sns.lineplot(data=df_20000, x='Thread', y='Time', hue='Schedule', marker='o')
g_20000.set_xscale('log', base=2)
g_20000.set_xticks([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_20000.set_xticklabels([1, 2, 4, 8, 12, 16, 32, 64, 128, 256])
g_20000.grid(True)
g_20000.set_xlabel("Numero di Thread")
g_20000.set_ylabel("Tempo (s)")
g_20000.set_title("Differenza fra portatile e pc fisso (20000 corpi)")
plt.savefig(os.path.join('grafici_finale', 'confronto_tempi_fin_20000.png'), dpi=300, bbox_inches='tight')
plt.close()
