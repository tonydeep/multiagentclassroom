"""
Simple web demo for Multi-Agent Classroom using Claude Agent SDK.
This is a simplified version for demonstration purposes.
"""
import os
import asyncio
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Store active dialogue managers
active_sessions = {}

# Sample problems
SAMPLE_PROBLEMS = [
    {
        "id": "1",
        "title": "Phương trình bậc hai",
        "problem": "Giải phương trình: x² + 5x + 6 = 0"
    },
    {
        "id": "2",
        "title": "Hệ phương trình tuyến tính",
        "problem": "Giải hệ phương trình:\n2x + y = 5\nx - y = 1"
    },
    {
        "id": "3",
        "title": "Bất đẳng thức",
        "problem": "Chứng minh: (a + b)² ≥ 4ab với mọi a, b ∈ R"
    }
]

# Simple learning script
SIMPLE_SCRIPT = {
    "1": {
        "id": "1",
        "name": "Hiểu vấn đề",
        "goal": "Hiểu rõ đề bài và xác định các thông tin cho trước",
        "tasks": [
            {"id": "1.1", "description": "Xác định dạng bài toán"},
            {"id": "1.2", "description": "Liệt kê các thông tin đã biết"}
        ]
    },
    "2": {
        "id": "2",
        "name": "Lập kế hoạch",
        "goal": "Đề xuất phương pháp giải",
        "tasks": [
            {"id": "2.1", "description": "Chọn công thức/phương pháp phù hợp"},
            {"id": "2.2", "description": "Vạch ra các bước giải"}
        ]
    },
    "3": {
        "id": "3",
        "name": "Thực hiện",
        "goal": "Giải bài toán theo kế hoạch",
        "tasks": [
            {"id": "3.1", "description": "Thực hiện các bước tính toán"},
            {"id": "3.2", "description": "Kiểm tra kết quả"}
        ]
    }
}


@app.route('/')
def index():
    """Main demo page."""
    return render_template('demo.html', problems=SAMPLE_PROBLEMS)


@app.route('/api/problems')
def get_problems():
    """Get list of sample problems."""
    return jsonify(SAMPLE_PROBLEMS)


@app.route('/api/start-session', methods=['POST'])
def start_session():
    """Start a new learning session."""
    try:
        data = request.json
        problem_id = data.get('problem_id', '1')
        user_name = data.get('user_name', 'Student')

        # Find the problem
        problem = next((p for p in SAMPLE_PROBLEMS if p['id'] == problem_id), SAMPLE_PROBLEMS[0])

        # Create session
        session_id = str(uuid.uuid4())

        # Create log directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)

        # Initialize dialogue manager
        from flow_sdk.dialogue_manager import ClaudeDialogueManager

        dialogue_manager = ClaudeDialogueManager(
            socketio=socketio,
            session_id=session_id,
            user_name=user_name,
            problem=problem['problem'],
            script=SIMPLE_SCRIPT,
            conversation="",
            participants=["Harry", "Hermione", "Ron"],
            current_stage_id="1",
            turn_number=0,
            filename=f"logs/{session_id}.log"
        )

        # Store in active sessions
        active_sessions[session_id] = dialogue_manager

        return jsonify({
            'success': True,
            'session_id': session_id,
            'problem': problem,
            'participants': ["Harry", "Hermione", "Ron"]
        })

    except Exception as e:
        print(f"Error starting session: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print(f"Client connected: {request.sid}")
    emit('connected', {'status': 'Connected to server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print(f"Client disconnected: {request.sid}")


@socketio.on('join_session')
def handle_join_session(data):
    """Join a specific session room."""
    session_id = data.get('session_id')
    if session_id:
        join_room(session_id)
        print(f"Client {request.sid} joined session {session_id}")
        emit('joined_session', {'session_id': session_id})


@socketio.on('send_message')
def handle_send_message(data):
    """Handle incoming message from user."""
    session_id = data.get('session_id')
    sender_name = data.get('sender_name', 'Student')
    message_text = data.get('message', '')

    print(f"Received message from {sender_name} in session {session_id}: {message_text}")

    if not session_id or session_id not in active_sessions:
        emit('error', {'error': 'Invalid session'})
        return

    # Get the dialogue manager
    dialogue_manager = active_sessions[session_id]

    # Process the message asynchronously
    # Note: We need to run this in the event loop
    async def process_and_send():
        try:
            result = await dialogue_manager.process_message(sender_name, message_text)
            if result:
                print(f"Agent {result['agent']} responded: {result['response'][:50]}...")
            else:
                print("No response generated")
        except Exception as e:
            print(f"Error processing message: {e}")
            import traceback
            traceback.print_exc()
            socketio.emit('error', {'error': str(e)}, room=session_id)

    # Run the async function
    asyncio.run(process_and_send())


@socketio.on('end_session')
def handle_end_session(data):
    """End a session."""
    session_id = data.get('session_id')

    if session_id and session_id in active_sessions:
        dialogue_manager = active_sessions[session_id]
        dialogue_manager.cancel()

        # Remove from active sessions
        del active_sessions[session_id]

        emit('session_ended', {'session_id': session_id})
        print(f"Session {session_id} ended")


if __name__ == '__main__':
    # Check for required environment variables
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("WARNING: ANTHROPIC_API_KEY not found in environment variables!")
        print("Please set it in your .env file or environment")

    print("=" * 60)
    print("Multi-Agent Classroom - Claude Agent SDK Demo")
    print("=" * 60)
    print("\nStarting server on http://localhost:5001")
    print("Make sure you have set ANTHROPIC_API_KEY in your .env file\n")

    # Run the app
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
