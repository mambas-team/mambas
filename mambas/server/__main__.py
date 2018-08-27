from mambas.server.database import MambasDatabase
from mambas.server.webserver import MambasWebserver

def main():
    database = MambasDatabase()
    webserver = MambasWebserver(database)
    # TODO: make dynamic, remove debug flag
    webserver.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    main()