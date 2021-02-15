from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    return 'You want path: %s' % path

if __name__ == '__main__':
    app.run()
    