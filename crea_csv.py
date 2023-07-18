import csv

# Definisci il percorso del file CSV da creare
file_path = "output.csv"

# Definisci i dati da scrivere nel file CSV
data = [["ciao"]]

# Scrivi i dati nel file CSV
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("Il file CSV è stato creato correttamente.")
