from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import sys
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.agent import app as content_agent_app  # Assuming agent.py compiles your LangGraph app

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_in_production'  # Replace for production

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'web', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic")
        image = request.files.get("image")
        platforms = request.form.getlist("platforms")
        schedule_option = request.form.get("schedule_option")
        schedule_time = request.form.get("schedule_time")

        if not topic or not platforms:
            flash("Topic and platform selection are required.")
            return redirect(url_for("index"))

        # Handle uploaded image
        image_path = None
        if image and image.filename != "":
            filename = image.filename
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(image_path)

        # Determine schedule time
        final_schedule_time = None
        if schedule_option == "later" and schedule_time:
            final_schedule_time = schedule_time

        # Run LangGraph agent
        initial_state = {
            "topic": topic,
            "platforms": platforms,
            "schedule_time": final_schedule_time,
            "caption": None,
            "content": None,
            "image_url": None,
            "retrieved_docs": None
        }

        try:
            final_state = content_agent_app.invoke(initial_state)
            flash("Post content generated successfully.")
            flash(f"Caption: {final_state.get('caption', 'No caption generated')}")
            flash(f"Content: {final_state.get('content', 'No content generated')}")
            flash(f"Image URL: {final_state.get('image_url', 'No image generated')}")
            
            # If this is an AJAX request, return JSON
            if request.headers.get('Content-Type') == 'application/json' or request.is_json:
                return jsonify({
                    'success': True,
                    'caption': final_state.get('caption', ''),
                    'content': final_state.get('content', ''),
                    'image_url': final_state.get('image_url', ''),
                    'message': 'Content generated successfully!'
                })
                
        except Exception as e:
            error_message = f"Error generating content: {str(e)}"
            flash(error_message)
            
            # If this is an AJAX request, return JSON error
            if request.headers.get('Content-Type') == 'application/json' or request.is_json:
                return jsonify({
                    'success': False,
                    'error': error_message
                }), 500

        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def api_generate():
    """API endpoint for generating content"""
    print("[DEBUG] /api/generate endpoint hit")
    try:
        data = request.get_json()
        print(f"[DEBUG] Received data: {data}")
        
        if not data or not data.get('topic') or not data.get('platforms'):
            return jsonify({
                'success': False,
                'error': 'Topic and platforms are required'
            }), 400

        # Run LangGraph agent
        initial_state = {
            "topic": data.get('topic'),
            "platforms": data.get('platforms'),
            "schedule_time": data.get('schedule_time'),
            "caption": None,
            "content": None,
            "image_url": None,
            "retrieved_docs": None
        }

        final_state = content_agent_app.invoke(initial_state)
        
        return jsonify({
            'success': True,
            'caption': final_state.get('caption', ''),
            'content': final_state.get('content', ''),
            'image_url': final_state.get('image_url', ''),
            'message': 'Content generated successfully!'
        })

    except Exception as e:
        print("[ERROR] An exception occurred in /api/generate:")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
