# Required for socketIO to emit events from background threads.
# Must be first import in the file.
import eventlet
eventlet.monkey_patch()

from flask import Flask, request, Response
from flask import render_template, jsonify
from stream_code import main
import threading
from flask_socketio import SocketIO, emit


# create application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

class Thread(threading.Thread):
    def __init__(self, trackers):
        threading.Thread.__init__(self)
        self.trackers = trackers

    def run(self):
        main(self.trackers, self.emitter)

    def emitter(self, msg):
        print(msg)
        socketio.emit('twts', msg, namespace='/test')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tweets/', methods=['GET'])
def tweets():
    source = request.args.get('source')
    print(source)
    Thread(source).start()
    return render_template('tweets.html', title="Displaying for: " + source)

@socketio.on('connect', namespace='/test')
def test_connect():
    print("IO connected")

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port=4444)
