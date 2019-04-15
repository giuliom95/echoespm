import requests
import threading

import server

url = 'http://127.0.0.1:5000'


def populate_db():
    server.dbconn.insertUser('pgabriel', 'Peter Gabriel', 'pgabriel@genesis.com')
    server.dbconn.insertUser('pcollins', 'Phil Collins', 'pcollins@genesis.com')

    server.dbconn.insertProject('TRES', 'Trespass')
    server.dbconn.insertProject('SEBTP', 'Selling England by the Pound')

    server.dbconn.insertContentType('TRES', 'shot')
    server.dbconn.insertContentType('TRES', 'character')

    server.dbconn.insertContent('TRES', 'shot', 'layout')
    server.dbconn.insertContent('TRES', 'shot', 'animation')
    server.dbconn.insertContent('TRES', 'shot', 'lighting')
    


if __name__=='__main__':

    serverThread = threading.Thread(target=server.app.run, name='flask')
    serverThread.daemon = True
    serverThread.start()

    server.dbconn.firstSetup()

    # Wait until server thread boots successfully
    while True:
        try:
            requests.get(url)
        except:
            continue
        break

    populate_db()

    print('Everything went fine.')