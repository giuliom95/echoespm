import requests
import threading

import server

url = 'http://127.0.0.1:5000'


if __name__=='__main__':

    serverThread = threading.Thread(target=server.app.run, name='flask')
    serverThread.daemon = True
    serverThread.start()

    server.dbconn.first_setup()

    # Wait until server threads boots successfully
    while True:
        try:
            requests.get(url)
        except:
            continue
        break

    print('Everything went fine.')