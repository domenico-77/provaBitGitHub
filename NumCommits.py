import requests
import time

def get_commits(owner, repo, access_token):
    # Imposta i tuoi dati di accesso
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Effettua la chiamata API per ottenere i commit
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {
        "per_page": 100,  # Numero di commit per pagina (massimo 100)
        "page": 1
    }

    commit_count = 0

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            commits = response.json()

            # Esegui le operazioni desiderate con i dati dei commit
            for commit in commits:
                commit_sha = commit["sha"]
                commit_message = commit["commit"]["message"]
                # Altri dettagli o elaborazioni dei commit...
                #print("Commit SHA: " + commit_sha)
                #print("Commit Message: " + commit_message)
                commit_count += 1

            # Verifica se ci sono altre pagine di commit
            if "Link" in response.headers:
                links = response.headers["Link"]
                if "rel=\"next\"" not in links:
                    break
            else:
                break

            # Incrementa il numero di pagina per la prossima chiamata
            params["page"] += 1

            # Rispetta il rate limit dell'API di GitHub
            remaining_requests = int(response.headers.get("X-RateLimit-Remaining"))
            if remaining_requests <= 0:
                reset_time = int(response.headers.get("X-RateLimit-Reset"))
                wait_time = reset_time - time.time() + 5  # Aggiungi 5 secondi per sicurezza
                time.sleep(wait_time)
        else:
            print("Errore durante la chiamata API.")
            break

    print(f"Numero totale di commit: {commit_count}")

def main():
    owner = "JabRef"
    repo = "jabref"
    access_token = "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"
    get_commits(owner, repo, access_token)

if __name__ == "__main__":
    main()
