from flask import Flask, request
from flask_socketio import SocketIO
import random
#from flask_cors import CORS
#import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = "password"

#cors = CORS(app, origins='*')
#app.config['CORS_HEADERS'] = 'Content-Type'

socketio = SocketIO(app, cors_allowed_origins="*")

test_lum1 = {"id":"id126", 'E': "ON"}
test_lum2 = {"id":"id127", 'E' : "ON"}
test_temperature1 = {"id":"id128", 'T' : "28"}
test_temperature2 = {"id":"id129", 'T' : "32"}

test_data ={"id126":test_lum1, "id127":test_lum2, "id128": test_temperature1, "id129": test_temperature2}
#Test 1000 elements
for i in range(500,1000):
    el = {'id': 'id' + str(i), 'T': '100'}
    test_data[el['id']] = el


@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

@socketio.on('get_elements')   
def get_elements():
    print ("Demande mise a jour elements client sid :", request.sid)
    #Renvoi de tous les elements seulement au client qui a demandé
    #socketio.emit("update_elements", {'elements' : ['blba,yoyo'], 'ui': 123}, room=request.sid)
    test_temperature1['T'] = str(int(test_temperature1['T']) + 1)
    for key, el in test_data.items():
        if 'T' in el:
            #print (el)
            #el['T'] = str(int(el['T']) + 1)
            el['T'] = str(random.randrange(0,100))


    socketio.emit('MESSAGE', test_data)

@socketio.on('connect')
def client_connect():
    print ("TTTTTTT")
    print('connect ', request.sid)
    socketio.emit('MESSAGE', test_data)

@socketio.on('update_element')
def update_element(data):
    print ("Update Element data", data )
    print ("Update Element id:", data['id'] )
    print ("Update Element valeur:", data['valeur'] )
    print ("Update Element attribut:", data['attribut'] )
    test_data[data['id']][data['attribut']]= str(data['valeur'])
    socketio.emit('MESSAGE', {data['id'] : test_data[data['id']]})


if __name__ == '__main__':
    #app.run(host="localhost", port=8000, debug=True)

    socketio.run(app ,host='0.0.0.0', port=2345, debug=True) # Attention en mode debug 2 instance sont lancés!
