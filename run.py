#!/usr/bin/env python3
"""
Run script for Content Generator AI
"""

import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    # Change to the web directory and import app
    web_dir = os.path.join(project_root, 'web')
    sys.path.insert(0, web_dir)
    
    try:
        from web.app import app
        
        print("[INFO] Starting Content Generator AI...")
        print("[INFO] Open your browser and go to: http://localhost:5000")
        print("[INFO] Press Ctrl+C to stop the server\n")
        
        app.run(
            debug=True,
            host="0.0.0.0",
            port=5000,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n[INFO] Content Generator AI stopped. Goodbye!")
    except Exception as e:
        print(f"[ERROR] Error starting server: {e}")
        print("Make sure you have all dependencies installed and your .env file configured.")
