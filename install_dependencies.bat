@echo off
echo Installing Content Generator AI dependencies...
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing Python packages...
pip install --upgrade pip
pip install flask
pip install requests
pip install beautifulsoup4
pip install langchain
pip install langchain-openai
pip install python-dotenv
pip install tweepy
pip install openai
pip install faiss-cpu
pip install pytz
pip install "langgraph>=0.2.0"
pip install "pydantic[email]"
pip install werkzeug

echo.
echo Dependencies installed successfully!
echo.
echo To run the application:
echo 1. Make sure your virtual environment is activated
echo 2. Run: python run.py
echo 3. Open your browser to http://localhost:5000
echo.
pause
