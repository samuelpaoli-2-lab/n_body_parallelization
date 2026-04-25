Questa repository contiene l'implementazione in C++ e l'analisi prestazionale di un algoritmo di simulazione gravitazionale di un sistema N-corpi.

Il programma prevede due modalità di esecuzione: una è il benchmark e l'altra è la simulazione. La differenza è che nella simulazione c'è la registrazione dei dati calcolati nel file punti_prova_progetto.csv.

Per la modalità di benchmark basta eseguire il comando test_completo, per fare il test di teuue le configurazioni, oppure singolarmente:

test_4000

test_8000

test_12000

test_16000

test_20000

Per la modalita di simulazione invece  ci sono solo comandi delle singole quantita di corpi:

sim_4000

sim_8000

sim_12000

sim_16000

sim_20000


E' anche possibile visualizzare l'animazione grafica delle particelle in movimento, eseguendo il file python video.py nell'ambiente virtuale venv.
