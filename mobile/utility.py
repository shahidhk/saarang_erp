import json,httplib

def send_push(message):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
           "channels": [
             "all"
           ],
           "data": {
             "alert": message
           }
         }), {
           "X-Parse-Application-Id": "c39soVyRy8MRGfSQO2hLF8GQkJpVi6VqDJQB9WBS",
           "X-Parse-REST-API-Key": "Cacz8ASDzgu1t5cFOICGcv4ZZ0IRF47AaSfPhQTw",
           "Content-Type": "application/json"
         })
    result = json.loads(connection.getresponse().read())
    return result