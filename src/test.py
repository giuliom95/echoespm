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

    server.dbconn.insertResourceType('TRES', 'shot', 'layout')
    server.dbconn.insertResourceType('TRES', 'shot', 'animation')
    server.dbconn.insertResourceType('TRES', 'shot', 'lighting')

    server.dbconn.insertContent('TRES', 'shot', '001_001')
    server.dbconn.insertContent('TRES', 'shot', '001_002')
    server.dbconn.insertContent('TRES', 'shot', '002_001')

    server.dbconn.insertNewVersion('TRES', 'shot', '001_001', 'layout', 'pgabriel')
    server.dbconn.insertNewVersion('TRES', 'shot', '001_001', 'layout', 'pgabriel')
    server.dbconn.insertNewVersion('TRES', 'shot', '001_001', 'layout', 'pgabriel')
    server.dbconn.insertNewVersion('TRES', 'shot', '001_001', 'animation', 'pgabriel')
    server.dbconn.insertNewVersion('TRES', 'shot', '002_001', 'animation', 'pgabriel')
    


if __name__=='__main__':

    serverThread = threading.Thread(target=server.app.run, name='flask')
    serverThread.daemon = True
    serverThread.start()

    server.dbconn.firstSetup()

    populate_db()

    # Wait until server thread boots successfully
    while True:
        try:
            requests.get(url)
        except:
            continue
        break


    print('Everything went fine.')