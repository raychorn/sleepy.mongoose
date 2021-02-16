import sys
from flask import Flask, request, Response
from flask.ext.runner import Runner

pylib = '/home/raychorn/projects/python-projects/private_vyperlogix_lib3'
if (not any([f == pylib for f in sys.path])):
    sys.path.insert(0, pylib)
    
from vyperlogix.misc import _utils

import mujson as json

def handle_connect(**kwargs):
    from vyperlogix.decorators import __with
    @__with.database(environ=kwargs.get('data', {}))
    def get_mongo_client(db=None):
        return db
    return get_mongo_client(db=None)
        

vectors = {}
vectors['_connect'] = handle_connect


class MongoClient():
    mongoClient = None
    
    def __init__(self, client):
        self.client = client
        self.database = None
        self.collection = None
        
    def list_databases(self, kwargs=None):
        print('DEBUG: self.client -> {}'.format(self.client))
        print('DEBUG: kwargs -> {}'.format(kwargs))
        return [db for db in self.client.list_databases()]
    
    def _use(self, kwargs=None):
        resp = None
        print('DEBUG: kwargs -> {}'.format(kwargs))
        args = kwargs.get('args') if (kwargs is not None) else None
        if (args):
            assert len(args) == 2, 'Expected the args to have two items, the database and the command verb.'
            self.database = self.client[args[0]]
            the_func = getattr(self.database, args[-1])
            print('DEBUG: the_func -> {}'.format(the_func))
            if (callable(the_func)):
                resp = the_func()
            return resp
        return kwargs
        

app = Flask(__name__)
runner = Runner(app)

@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    the_response = {"path": path}
    print('request.method -> {}'.format(request.method))
    if (request.method in ['POST', 'PUT', 'DELETE']):
        try:
            d = request.get_json()
            print(json.dumps(d, indent=3))
            print('-'*30)
        except Exception as ex:
            print(_utils.formattedException(details=ex))
            
        for k,v in vectors.items():
            if (path.find(k) > -1):
                client = v(data=d) if (callable(v)) else None
                MongoClient.mongoClient = MongoClient(client)
    elif (request.method in ['GET']):
        the_path = path.split('/')
        the_func = getattr(MongoClient.mongoClient, the_path[0])
        print('DEBUG: the_path -> {}, the_func -> {}'.format(the_path, the_func))
        if (callable(the_func)):
            try:
                resp = the_func({'args': the_path[1:]})
                print('DEBUG: resp -> {}'.format(resp))
                the_response['/'.join(the_path)] = resp
            except Exception as ex:
                print(_utils.formattedException(details=ex))
    return Response(json.dumps(the_response), mimetype='application/json')

if (__name__ == '__main__'):
    #sys.argv.append('--help')
    if (not any([str(a).find('-p ') > -1 for a in sys.argv])):
        sys.argv.append('-p 27080')
    runner.run()
    