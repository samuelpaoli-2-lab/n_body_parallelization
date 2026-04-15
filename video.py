import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Leggi i dati (il tuo CSV ora dovrà avere X1,Y1 fino a X1000, Y1000... 
# per questo spesso si cambia formato per i big data, ma per 1000 regge ancora)
df = pd.read_csv("punti_prova_progetto.csv")

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor('black')
ax.set_xlim(-800, 800) # Limiti della "scatola"
ax.set_ylim(-800, 800)

# Creiamo un singolo oggetto "scatter" (molto più veloce per la scheda video)
scatter = ax.scatter([], [], c='white', s=2) # s=2 è la dimensione dei puntini

def update(frame):
    # Estraiamo tutte le X e tutte le Y per questo frame
    # (Questo presuppone che tu abbia salvato le colonne come X0, Y0, X1, Y1...)
    x_data = df.iloc[frame, 1::2] # Prende le colonne dispari (X) saltando il Tempo
    y_data = df.iloc[frame, 2::2] # Prende le colonne pari (Y)
    
    # Aggiorniamo le posizioni di tutti i puntini in un colpo solo!
    scatter.set_offsets(list(zip(x_data, y_data)))
    return scatter,

ani = FuncAnimation(fig, update, frames=len(df), interval=20, blit=True)
plt.show()



#source env_video/bin/activate
#deactivate