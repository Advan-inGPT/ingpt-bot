# Install requirements

### _$ pip install -r requirements.py_

# To run

## Start FastAPI Server
_$ cd backend_ <br>
_$ uvicorn app:app --host 0.0.0.0 --port 8000_

## Flutter
Open another terminal to start the bot <br>
cd to mas_bot_web (under mas-bot home directory) <br>
_$ flutter run -d chrome --release --dart-define=API_BASE=http://localhost:8000_ <br>

## Streamlit
open another terminal and run the fronend <br>
_$ cd frontend_ <br>
_$ streamlit run mas-bot.py_ <br>
