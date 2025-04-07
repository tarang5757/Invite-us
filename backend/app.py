import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, url_for, request, jsonify, redirect, session
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
import os
import shutil
import subprocess
import uuid
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configure SocketIO with explicit CORS settings
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='eventlet',
    logger=True,
    engineio_logger=True  # Enable logging for debugging
)

# New API endpoints for React/Next.js frontend
@app.route('/api/generate-room', methods=['GET'])
def generate_room():
    """Generate a new unique room ID."""
    room_id = str(uuid.uuid4())
    return jsonify({"room_id": room_id})

@app.route('/api/join-room', methods=['POST'])
def join_room_route():
    """Handle API request to join a room."""
    try:
        data = request.get_json()
        print("here", data)
        room_id = data.get('room_id')
        username = data.get('username')
        
        if not room_id or not username:
            return jsonify({"error": "Room ID and username are required"}), 400
        
        # Store in session
        session['room_id'] = room_id
        session['username'] = username
        
        return jsonify({
            "success": True, 
            "room_id": room_id, 
            "username": username
        })
    except Exception as e:
        app.logger.error(f"Error in join_room_route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/compile', methods=['POST'])
def api_compile():
    """API version of compile for Next.js frontend"""
    data = request.get_json()
    code = data.get('codeVal')
    inputVal = data.get('inputVal')
    langType = data.get('langType')

    output = code_exe(langType, code, inputVal)
    return jsonify({'result': output})

# Original routes - keep these for backward compatibility
@app.route('/')
def index():
    """Render the home page with an optional room ID."""
    room_id = request.args.get('room_id', '')
    return render_template('home.html', room_id=room_id)

@app.route('/compile', methods=['POST'])
def compile():
    """Compile and execute code received from the frontend."""
    data = request.get_json()
    code = data.get('codeVal')
    inputVal = data.get('inputVal')
    langType = data.get('langType')

    output = code_exe(langType, code, inputVal)
    return jsonify({'result': output})

@app.route('/editor/<string:room_id>', methods=['GET', 'POST'])
def editor(room_id):
    """Render the editor page for a specific room."""
    if request.method == 'POST':
        username = request.form.get('username')
        return render_template('editor.html', room_id=room_id, userName=username)
    return redirect(url_for("index", room_id=room_id))

# Socket.IO event handlers - these should work with both frontends
@socketio.on('join')
def handle_join(data):
    """Handle user joining a room."""
    room = data['room']
    userName = data['userName']
    join_room(room)
    emit('request_users', {'room': room, 'userName': userName}, to=room, skip_sid=True)
    emit('request_editors', {'room': room}, to=room, skip_sid=True)

@socketio.on('requested_users')
def requested_users(data):
    """Handle user request to get the list of users in the room."""
    room = data['room']
    users = data['users']
    emit('create_users', {'room': room, 'users': users}, to=room, skip_sid=True)

@socketio.on('requested_editors')
def requested_editors(data):
    """Handle request to get the list of current editors."""
    room = data['room']
    currentEditors = data['currentEditors']  # This is an array of [textEditorId, content, fileName]
    fileCount = data['fileCount']
    emit('create_editors', {'room': room, 'currentEditors': currentEditors, 'fileCount': fileCount}, to=room, skip_sid=True)

@socketio.on('update_text')
def handle_update(data):
    """Broadcast text updates to all users in the room."""
    room = data['room']
    emit('update_text', data, to=room, skip_sid=True)

@socketio.on('create_new_file')
def create_new_file(data):
    """Handle creation of a new file in the editor."""
    emit('create_new_file', data, to=data['room'], skip_sid=True)

@socketio.on('delete_file')
def delete_file(data):
    """Handle file deletion request."""
    emit('delete_file', data, to=data['room'], skip_sid=True)

@socketio.on('rename_file')
def rename_file(data):
    """Handle file renaming request."""
    emit('rename_file', data, to=data['room'], skip_sid=True)

def code_exe(language, code, inputVal):
    """Execute the given code in a secure temporary environment."""
    if language not in ["cpp", "py", 'java']:
        return "Error: Invalid File Extension. Use cpp or py or java."

    sessionId = str(uuid.uuid4())
    folderPath = os.path.join("temp", sessionId)
    os.makedirs(folderPath, exist_ok=True)

    fileName = f"{language}_code.{language}"
    filePath = os.path.join(folderPath, fileName)

    # Write code to the temporary file
    with open(filePath, "w") as f:
        f.write(code)

    try:
        if language == "py":
            execute = subprocess.run(["python3", filePath], timeout=10, input=inputVal, capture_output=True, text=True)
        elif language == "cpp":
            compileCmd = ["g++", "-o", f"{folderPath}/output", filePath]
            compileProcess = subprocess.run(compileCmd, capture_output=True, text=True)
            if compileProcess.returncode != 0:
                return compileProcess.stderr
            execute = subprocess.run([f"./{folderPath}/output"], timeout=10, input=inputVal, capture_output=True, text=True)
        
        elif language == "java":
            # Extract main class name from the code
            class_match = re.search(r'public\s+class\s+(\w+)', code)
            if class_match:
                className = class_match.group(1)
            else:
                # Fall back to filename-based class name if regex fails
                javaFileName = os.path.basename(filePath)
                className = javaFileName.replace(".java", "")

            # Compile Java code
            compileCmd = ["javac", filePath]
            compileProcess = subprocess.run(compileCmd, capture_output=True, text=True)
            if compileProcess.returncode != 0:
                shutil.rmtree(folderPath)
                return compileProcess.stderr  # Return compilation errors

            # Run compiled Java class dynamically
            executeCmd = ["java", "-cp", folderPath, className]
            execute = subprocess.run(executeCmd, timeout=10, input=inputVal, capture_output=True, text=True)
        
        # Clean up temp files
        shutil.rmtree(folderPath)
        return execute.stderr if execute.returncode != 0 else execute.stdout

    except subprocess.TimeoutExpired:
        shutil.rmtree(folderPath)
        return "Error: Code execution timed out."

if __name__ == '__main__':
    os.makedirs("temp", exist_ok=True)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)