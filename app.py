# Required for socketIO to emit events from background threads.
# Must be first import in the file.
import eventlet
eventlet.monkey_patch()

from flask import Flask, request, Response
from flask import render_template, jsonify
from stream_code import getTwitterStream
import threading
from flask_socketio import SocketIO, emit


# create application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

class Thread(threading.Thread):
    
    def __init__(self, source):
        threading.Thread.__init__(self)
        self.source = source
        self.twitterStream = None
        
    def stop(self):
        print("stopping")
        if self.twitterStream:
            self.twitterStream.disconnect()

    def run(self):
        self.twitterStream = getTwitterStream(self.source, self.emitter)
        
        if self.source[0] == "@":
            val = self.source
            # to get twitter user-id for the specified username
            user_objects = api.lookup_users(screen_names=[self.source[1:]])
            print(user_objects[0].id_str)
            self.twitterStream.filter(follow=[user_objects[0].id_str])
        else:
            val = "#" + self.source[1:]
            print(val)
            self.twitterStream.filter(track=[val])

    def emitter(self, msg):
        print(msg)
        socketio.emit('twts', msg, namespace='/test')

t = None
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tweets/', methods=['GET'])
def tweets():
    global t
    source = request.args.get('source')
    print(source)
    #Thread(source).start()
    if t is not None:
        t.stop()
    t = Thread(source)
    t.start()
    return render_template('tweets.html', title="Displaying for: " + source)

@socketio.on('connect', namespace='/test')
def test_connect():
    print("IO connected")

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port=4444)
