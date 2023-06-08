import requests
import time

def get_pull_requests(owner, repo, access_token, state):
    # Imposta i tuoi dati di accesso
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Imposta i parametri per la chiamata API
    params = {
        "state": state,
        "per_page": 100  # Numero di pull request per pagina (massimo 100)
    }

    pull_requests = []
    page = 1

    # Effettua la chiamata API per ottenere le pull request
    while True:
        params["page"] = page
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        response = requests.get(url, headers=headers, params=params)

        # Controlla lo stato della risposta
        if response.status_code == 200:
            page_pull_requests = response.json()

            # Aggiungi le pull request della pagina corrente alla lista totale
            pull_requests.extend(page_pull_requests)

            # Se non ci sono più pull request nella pagina corrente, abbiamo ottenuto tutte le pull request
            if len(page_pull_requests) == 0:
                break

            # Passa alla pagina successiva
            page += 1

            # Verifica il rate limit dell'API di GitHub
            remaining_requests = int(response.headers.get("X-RateLimit-Remaining"))
            if remaining_requests <= 0:
                reset_time = int(response.headers.get("X-RateLimit-Reset"))
                wait_time = reset_time - time.time() + 5  # Aggiungi 5 secondi per sicurezza
                time.sleep(wait_time)
        else:
            print("Errore durante la chiamata API.")
            break

    # Esegui le operazioni desiderate con i dati delle pull request
    for pull_request in pull_requests:
        pull_request_number = pull_request["number"]
        pull_request_title = pull_request["title"]
        # Altri dettagli o elaborazioni delle pull request...
        #print("Pull Request num" + str(pull_request_number) + ": " + str(pull_request_title))

    total_pull_requests = len(pull_requests)
    print(f"Numero di pull request {state}: {total_pull_requests}")

def main():
    owner = "JabRef"
    repo = "jabref"
    access_token = "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"
    get_pull_requests(owner, repo, access_token, "open")  # Pull request aperte
    get_pull_requests(owner, repo, access_token, "closed")  # Pull request chiuse

if __name__ == "__main__":
    main()
