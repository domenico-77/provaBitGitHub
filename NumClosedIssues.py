import requests
import time

def main():
    # Imposta i tuoi dati di accesso
    headers = {
        "Authorization": "Bearer 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"
    }

    # Imposta i parametri per la chiamata API
    owner = "JabRef"
    repo = "jabref"
    state = "closed"  # Stato delle issue da considerare

    # Effettua la chiamata API per ottenere le issue
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    params = {
        "state": state,
        "per_page": 100  # Numero di issue per pagina (massimo 100)
    }

    try:
        issues = []
        page = 1

        while True:
            params["page"] = page

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            if response.status_code == 200:
                page_issues = response.json()

                # Aggiungi le issue della pagina corrente alla lista totale
                issues.extend(page_issues)

                # Se non ci sono più issue nella pagina corrente, abbiamo ottenuto tutte le issue chiuse
                if len(page_issues) == 0:
                    break

                # Passa alla pagina successiva
                page += 1

                # Rispetta il rate limit dell'API di GitHub
                remaining_requests = int(response.headers.get("X-RateLimit-Remaining"))
                if remaining_requests <= 0:
                    reset_time = int(response.headers.get("X-RateLimit-Reset"))
                    wait_time = reset_time - time.time() + 5  # Aggiungi 5 secondi per sicurezza
                    time.sleep(wait_time)
            else:
                print("Errore durante la chiamata API.")
                break

        # Esegui le operazioni desiderate con i dati delle issue
        for issue in issues:
            issue_number = issue["number"]
            issue_title = issue["title"]
            # Altri dettagli o elaborazioni delle issue...
            #print("issue num" + str(issue_number) + ": " + str(issue_title))

        total_issues = len(issues)
        print(f"Numero totale di issue"+state+": "+f"{total_issues}")
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la chiamata API: {str(e)}")

if __name__ == "__main__":
    main()
