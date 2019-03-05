import requests
import threading

import server

url = 'http://127.0.0.1:5000'

def test_content_type():
    print('#### BEGIN test_content_type ####')

    r = requests.get('{0}/content/shot'.format(url))
    assert r.status_code == 404

    r = requests.post('{0}/content/shot'.format(url))
    assert r.status_code == 204

    r = requests.post('{0}/content/shot'.format(url))
    assert r.status_code == 409

    r = requests.get('{0}/content/shot'.format(url))
    assert r.status_code == 200
    r_json = r.json()
    assert r_json['name'] == 'shot'


def test_content():
    print('#### BEGIN test_content ####')

    r = requests.get('{0}/content/shot/001_001'.format(url))
    assert r.status_code == 404

    r = requests.post('{0}/content/shottone/001_001'.format(url))
    assert r.status_code == 400

    r = requests.post('{0}/content/shot/001_001'.format(url))
    assert r.status_code == 204

    r = requests.post('{0}/content/shot/001_001'.format(url))
    assert r.status_code == 409

    r = requests.get('{0}/content/shot/001_001'.format(url))
    assert r.status_code == 200
    r_json = r.json()
    assert r_json['type'] == 'shot'
    assert r_json['name'] == '001_001'


def test_resource():
    print('#### BEGIN test_resource ####')

    # Try to access a non-existant resource 
    r = requests.get('{0}/content/shot/001_001/animation'.format(url))
    assert r.status_code == 404

    # Try to create a resource with errors in the request
    r = requests.post('{0}/content/shottone/001_001/animation'.format(url))
    assert r.status_code == 400
    r = requests.post('{0}/content/shot/001_002/animation'.format(url))
    assert r.status_code == 400

    # Create a valid resource
    r = requests.post('{0}/content/shot/001_001/animation'.format(url))
    assert r.status_code == 204

    # Try to create a duplicate resource
    r = requests.post('{0}/content/shot/001_001/animation'.format(url))
    assert r.status_code == 409

    # Access the given resource
    r = requests.get('{0}/content/shot/001_001/animation'.format(url))
    assert r.status_code == 200
    r_json = r.json()
    assert r_json['content']['type'] == 'shot'
    assert r_json['content']['name'] == '001_001'
    assert r_json['name'] == 'animation'


def test_version():
    print('#### BEGIN test_version ####')

    # Create layout and lighting resources
    requests.post('{0}/content/shot/001_001/layout'.format(url))
    requests.post('{0}/content/shot/001_001/lighting'.format(url))

    # Try to access non-existant version
    r = requests.get('{0}/content/shot/001_001/layout/v001'.format(url))
    assert r.status_code == 404

    # Try to create layout v001 with errors in the request
    r = requests.post('{0}/content/shottone/001_001/layout/v001'.format(url))
    assert r.status_code == 400
    r = requests.post('{0}/content/shot/001_002/layout/v001'.format(url))
    assert r.status_code == 400
    r = requests.post('{0}/content/shot/001_001/layouts/v001'.format(url))
    assert r.status_code == 400

    # Create a valid version
    r = requests.post('{0}/content/shot/001_001/layout/v001'.format(url))
    assert r.status_code == 204

    # Try to create version with wrong dependency
    payload = {'dependencies': ['shottone/001_001/layout/v001']}
    r = requests.post('{0}/content/shot/001_001/animation/v001'.format(url), data=payload)
    assert r.status_code == 400

    # Create a valid version with a dependency
    payload = {'dependencies': ['shot/001_001/layout/v001']}
    r = requests.post('{0}/content/shot/001_001/animation/v001'.format(url), data=payload)
    assert r.status_code == 204

    # Create a valid version with two dependencies
    payload = {'dependencies': ['shot/001_001/layout/v001', 'shot/001_001/animation/v001']}
    r = requests.post('{0}/content/shot/001_001/lighting/v001'.format(url), data=payload)
    assert r.status_code == 204

    # Try to create duplicate
    r = requests.post('{0}/content/shot/001_001/lighting/v001'.format(url), data=payload)
    assert r.status_code == 409

    # Access the given resource
    r = requests.get('{0}/content/shot/001_001/lighting/v001'.format(url))
    assert r.status_code == 200
    r_json = r.json()
    assert r_json['resource']['content']['type'] == 'shot'
    assert r_json['resource']['content']['name'] == '001_001'
    assert r_json['resource']['name'] == 'lighting'
    assert r_json['version'] == 1

    # Access the given and its dependencies
    r = requests.get('{0}/content/shot/001_001/lighting/v001?dependencies=1'.format(url))
    assert r.status_code == 200
    r_json = r.json()
    assert r_json['resource']['content']['type'] == 'shot'
    assert r_json['resource']['content']['name'] == '001_001'
    assert r_json['resource']['name'] == 'lighting'
    assert r_json['version'] == 1
    assert r_json['dependencies'][0]['resource']['content']['type'] == 'shot'
    assert r_json['dependencies'][0]['resource']['content']['name'] == '001_001'
    assert r_json['dependencies'][0]['resource']['name'] == 'animation'
    assert r_json['dependencies'][0]['version'] == 1
    assert r_json['dependencies'][1]['resource']['content']['type'] == 'shot'
    assert r_json['dependencies'][1]['resource']['content']['name'] == '001_001'
    assert r_json['dependencies'][1]['resource']['name'] == 'layout'
    assert r_json['dependencies'][1]['version'] == 1


def test_content_type_list():
    print('#### BEGIN test_content_type_list ####')

    r = requests.get('{0}/content/'.format(url))
    assert r.status_code == 200
    r_json = r.json()
    assert r_json[0]['name'] == 'shot'


def test_contents_list():
    print('#### BEGIN test_contents_list ####')

    r = requests.get('{0}/content/character/'.format(url))
    assert r.status_code == 404

    r = requests.get('{0}/content/shot/'.format(url))
    assert r.status_code == 200
    r_json = r.json()
    assert r_json[0]['name'] == '001_001'
    assert r_json[0]['type'] == 'shot'


def test_resources_list():
    print('#### BEGIN test_resources_list ####')

    r = requests.get('{0}/content/shot/001_002/'.format(url))
    assert r.status_code == 404

    r = requests.get('{0}/content/shot/001_001/'.format(url))
    assert r.status_code == 200
    r_json = r.json()
    assert len(r_json) == 3
    assert r_json[0]['content']['name'] == '001_001'
    assert r_json[0]['content']['type'] == 'shot'
    assert r_json[0]['name'] == 'animation'


def test_versions_list():
    print('#### BEGIN test_versions_list ####')

    r = requests.get('{0}/content/shot/001_001/finishing/'.format(url))
    assert r.status_code == 404

    r = requests.get('{0}/content/shot/001_001/lighting/'.format(url))
    assert r.status_code == 200
    r_json = r.json()
    assert len(r_json) == 1
    assert r_json[0]['version'] == 1
    
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

    test_content_type()
    test_content()
    test_resource()
    test_version()
    test_content_type_list()
    test_contents_list()
    test_resources_list()
    test_versions_list()

    print('Everything went fine.')