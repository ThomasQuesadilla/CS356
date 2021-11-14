from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

frame = ""
pose = ""
@app.route('/')
def index():
    return "The connection is up!"

@app.route('/pose', methods=['GET', 'PUT'])
def transmit_pose():
    global pose
    if request.method == 'PUT':
        pose = request.data
    return pose

@app.route('/frame', methods=['GET', 'PUT'])
def transmit_frame():
    global frame
    if request.method == 'PUT':
        frame = request.data
    return frame

if __name__ == '__main__':
    # Fill in start
    # Change this to your server IP address and port
    socketio.run(app,host='10.197.249.134', port=5000)
    # Fill in end
