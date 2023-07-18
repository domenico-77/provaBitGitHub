import csv
import os

# Definisci il percorso del file CSV da creare
file_path = "output.csv"

# Definisci i dati da scrivere nel file CSV
data = [["ciao"]]
if os.path.isfile(file_path):
    data = [["ciao2"]]
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
else:
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


print("Il file CSV è stato creato correttamente.")
