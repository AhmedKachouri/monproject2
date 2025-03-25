import sys
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def process_logs():
    logging.info("Début du traitement des logs...")

    paths = []  # Liste des chemins des requêtes
    total_bytes = 0  # Total des octets envoyés
    total_time = 0  # Somme des temps de traitement
    failed_requests = 0  # Nombre de requêtes échouées (404, 500)
    largest_resource = ("", 0)  # (path, bytes_sent)

    for line in sys.stdin:
        parts = line.strip().split()
        if len(parts) != 4:
            logging.warning(f"Ligne ignorée (format incorrect) : {line.strip()}")
            continue

        path, code, bytes_sent, time_ms = parts
        code = int(code)
        bytes_sent = int(bytes_sent)
        time_ms = int(time_ms)

        paths.append(path)

        # Marquer les requêtes échouées
        if code in [404, 500]:
            path = f"!{path}"
            failed_requests += 1

        # Calcul des statistiques
        total_bytes += bytes_sent
        total_time += time_ms

        # Trouver la ressource la plus grande
        if bytes_sent > largest_resource[1]:
            largest_resource = (path, bytes_sent)

        # Afficher la ligne
        print(path)

    # Afficher les statistiques
    print("\n--- Statistiques ---")
    print(f"Plus grand fichier: {largest_resource[0]} ({largest_resource[1]} bytes)")
    print(f"Nombre de requêtes échouées: {failed_requests}")
    print(f"Total des octets envoyés: {total_bytes} bytes")
    print(f"Total en KB: {total_bytes / 1024:.2f} KB")
    print(f"Temps moyen de traitement: {total_time / len(paths):.2f} ms")

    logging.info("Fin du traitement.")

# Exécution du script
if __name__ == "__main__":
    process_logs()
