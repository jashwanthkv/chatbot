from flask import Flask, request, jsonify
from flask_cors import CORS

from agent import agent


from custom_memory_manager import CustomMemoryManager

app = Flask(__name__)
CORS(app)

memory_manager = CustomMemoryManager()

@app.route('/')
def home():
    return "Welcome to the Book Assistant API powered by Agno + Gemini!"

@app.route('/api/perform-task', methods=['POST'])
def perform_task():
    try:
        data = request.json
        task = data.get("task") or data.get("prompt")
        user_id = data.get("user_id")

        if not task:
            return jsonify({"error": "Task is required"}), 400

        print("🟡 Received task:", task)

        # Retrieve memory before response
        if user_id:
            memories = memory_manager.get_recent_interactions(user_id)
            print(f"🟢 Retrieved past memory for {user_id}: {memories}")

        # Generate response from agent
        response = agent.print_response(task)
        print("✅ Agent response:", response)

        # Log interaction to memory
        if user_id:
            memory_manager.log_interaction(user_id, response)
            print(f"🟢 Memory updated for {user_id}")

        return jsonify({"result": response})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
