import requests
import matplotlib.pyplot as plt

def get_code_stats(owner, repository, start_date, end_date):
    url = f"https://api.github.com/repos/{owner}/{repository}/commits"
    params = {
        "since": start_date,
        "until": end_date,
        "per_page": 100
    }
    headers = {
        "Authorization": "token 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"
    }
    
    code_stats = {
        "sloc": 0
    }
    
    page = 1
    
    while True:
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            page_commits = response.json()
            
            for commit in page_commits:
                if start_date <= commit["commit"]["committer"]["date"][:10] <= end_date:
                    commit_url = commit["url"]
                    commit_response = requests.get(commit_url, headers=headers)
                    
                    if commit_response.status_code == 200:
                        commit_data = commit_response.json()
                        files = commit_data["files"]
                        for file in files:
                            code_stats["sloc"] += file["additions"] - file["deletions"]
            
            # Check if there are more pages
            link_header = response.headers.get("Link")
            if link_header is None or 'rel="next"' not in link_header:
                break
            
            # Get the URL of the next page
            next_url = get_next_page_url(link_header)
            if next_url is None:
                break
            
            # Prepare the request for the next page
            url = next_url
            page += 1
        else:
            print(f"Error in request: {response.status_code}")
            return None
    
    return code_stats

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
    plt.ylabel('Numero di righe modificate (aggiunte + rimosse)')
    plt.title('Grafico delle righe di codice modificate')
    plt.show()

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
        
        stats = get_code_stats(owner, repository, start_date, end_date)
        print("Calculated commits from "+start_date+" to "+end_date)
        if stats:
            print(f"Number of Source Lines of Code (SLOC) added in the selected period: {stats['sloc']}")
            y_value.append(stats['sloc'])
        else:
            print("Number of Source Lines of Code (SLOC) added in the selected period: 0")
            y_value.append(0)

    plot_points(x_value, y_value)
