import csv
import os

# Definisci il percorso del file CSV da creare
file_path = os.path.join(os.getcwd(),"output/outut.csv")

# Estrai il percorso della directory dal percorso del file
directory = os.path.dirname(file_path)

# Verifica se la directory esiste, altrimenti crea la directory
if not os.path.exists(directory):
    os.makedirs(directory)

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
print(str(os.getcwd()))

