import sys
from flask import Flask, request
from flask.ext.runner import Runner

pylib = '/home/raychorn/projects/python-projects/private_vyperlogix_lib3'
if (not any([f == pylib for f in sys.path])):
    sys.path.insert(0, pylib)
    
from vyperlogix.misc import _utils

import mujson as json

app = Flask(__name__)
runner = Runner(app)

@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    print('request.method -> {}'.format(request.method))
    if (request.method in ['POST', 'PUT', 'DELETE']):
        try:
            d = request.get_json()
            print(json.dumps(d, indent=3))
            print('-'*30)
        except Exception as ex:
            print(_utils.formattedException(details=ex))
    return 'You want path: %s' % path

if (__name__ == '__main__'):
    #sys.argv.append('--help')
    if (not any([str(a).find('-p ') > -1 for a in sys.argv])):
        sys.argv.append('-p 27080')
    runner.run()
    