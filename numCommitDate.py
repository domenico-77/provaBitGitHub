import requests
import matplotlib.pyplot as plt

def get_commits(owner, repository, start_date, end_date):
    url = f"https://api.github.com/repos/{owner}/{repository}/commits"
    params = {
        "since": start_date,
        "until": end_date,
        "per_page": 100  # Imposta il numero massimo di commit per pagina
    }
    headers = {
        "Authorization": "token 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"
    }
    
    commits = []
    page = 1
    
    while True:
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            page_commits = response.json()
            
            # Aggiungi solo i commit nel periodo specificato
            filtered_commits = [
                commit for commit in page_commits
                if start_date <= commit["commit"]["committer"]["date"][:10] <= end_date
            ]
            
            commits.extend(filtered_commits)
            
            # Controlla se ci sono altre pagine
            link_header = response.headers.get("Link")
            if link_header is None or 'rel="next"' not in link_header:
                break
            
            # Ottieni l'URL della pagina successiva
            next_url = get_next_page_url(link_header)
            if next_url is None:
                break
            
            # Prepara la richiesta per la pagina successiva
            url = next_url
            page += 1
        else:
            print(f"Errore nella richiesta: {response.status_code}")
            return None
    
    return commits

def get_next_page_url(link_header):
    links = link_header.split(", ")
    for link in links:
        url, rel = link.split("; ")
        url = url[1:-1]  # Rimuovi i caratteri < e >
        rel = rel[5:-1]  # Rimuovi le virgolette attorno a rel=
        if rel == "next":
            return url
    return None

def plot_points(x_values, y_values):
    plt.plot(x_values, y_values)
    plt.xlabel('Valori di x')
    plt.ylabel('Valori di y')
    plt.title('Grafico a dispersione')
    #plt.switch_backend('TkAgg')
    plt.show()

# Utilizzo dell'esempio di funzione get_commits
'''owner = "JabRef"
repository = "jabref"
start_date = "2012-01-01"
end_date = "2014-12-31"

commits = get_commits(owner, repository, start_date, end_date)



if commits:
    print(f"Il numero di commit nel periodo selezionato è: {len(commits)}")'''
    #for commit in commits:
        #print(commit["sha"], commit["commit"]["message"])

if __name__ == "__main__":
    owner = "JabRef"
    repository = "jabref"
    month = 1
    year = 2013
    day_start = 1
    day_end_30 = 30
    day_end_31 = 31
    day_end_28 = 28
    day_end_29 = 29
    x_value=[]
    y_value=[]
    for month in range(1, 13):
        x_value.append(month)
        if month <= 9:
            month2 = "0" + str(month)
        else:
            month2 = str(month)

        start_date = str(year)+"-"+month2+"-0"+str(day_start)

        if month in [11, 4, 6, 9]:
            end_date = str(year)+"-"+month2+"-"+str(day_end_30)
        elif month == 2:
            if year%4 == 0:
                end_date = str(year)+"-"+month2+"-"+str(day_end_29)
            else:
                end_date = str(year)+"-"+month2+"-"+str(day_end_28)
        else:
            end_date = str(year)+"-"+month2+"-"+str(day_end_31)
        
        commits = get_commits(owner, repository, start_date, end_date)
        print("ho calcolato i connit fatti da "+start_date+"fino a "+end_date)
        if commits:
            print(f"Il numero di commit nel periodo selezionato è: {len(commits)}")
            y_value.append(len(commits))
        else:
            print("Il numero di commit nel periodo selezionato è:0")
            y_value.append(0)

        
    plot_points(x_value, y_value)


