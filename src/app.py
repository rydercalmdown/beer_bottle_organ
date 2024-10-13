import os
import sys
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

MIDI_DIRECTORY = 'midi'
ACTIVATE_ORGAN = False # set to true in rpi env

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('note')
def handle_note(data):
    note = data['note']
    state = data['state']
    if ACTIVATE_ORGAN:
        from controller import handle_note as controller_handle_note
        controller_handle_note(note, state)
    print(f"Note {note} {state}", flush=True)
    sys.stdout.flush()
    emit('note_feedback', {'message': f"Received: Note {note} {state}"})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True)
