import requests
import matplotlib.pyplot as plt

def get_issue_stats(owner, repository, start_date, end_date):
    url = f"https://api.github.com/repos/{owner}/{repository}/issues"
    params = {
        "state": "closed",
        "sort": "created",
        "direction": "asc",
        "per_page": 100
    }
    headers = {
        "Authorization": "token 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"
    }
    
    issue_stats = {
        "issues_resolved": 0
    }
    
    page = 1
    
    while True:
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            page_issues = response.json()
            
            for issue in page_issues:
                issue_created_date = issue["created_at"][:10]
                issue_closed_date = issue["closed_at"]
                if start_date <= issue_created_date <= end_date and issue_closed_date is not None:
                    issue_stats["issues_resolved"] += 1
            
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
    
    return issue_stats

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
    plt.xlabel('Tempo in mesi')
    plt.ylabel('Numero di Issue risolte')
    plt.title('Grafico delle Issue risolte')
    plt.show()

if __name__ == "__main__":
    owner = "JabRef"
    repository = "jabref"
    month = 1
    year = 2016
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
        
        stats = get_issue_stats(owner, repository, start_date, end_date)
        print(f"Calculated issues from {start_date} to {end_date}")
        if stats:
            print(f"Number of issues resolved in the selected period: {stats['issues_resolved']}")
            y_value.append(stats['issues_resolved'])
        else:
            print("The number of issues resolved in the selected period is: 0")
            y_value.append(0)

    plot_points(x_value, y_value)
