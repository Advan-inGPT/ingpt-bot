# Docker container - Backend <stable version> :
from project root run

### _$ docker compose up --build_

This will create a docker container with all the necessary python pacakages and will start the **FastApi** Server


# Install required python packages and start the server manually. skip this step for backend if you are using docker.

from <project_root>/backend run to install the python dependen:
### _$ pip install -r requirements.txt_

## Start FastAPI Server
_$ cd backend_ <br>
_$ uvicorn app:app --host 0.0.0.0 --port 8000_


## Flutter - Frontend (web)
Open another terminal to start the bot <br>
cd to frontend<br>
_$ flutter run -d chrome --release --dart-define=API_BASE=http://localhost:8000_ <br>


## Flutter - Frontend (android)
Open another terminal to start the bot <br>
cd to frontend<br>

then launch the emulator 
### _$ flutter emulators --launch <emulator_id>_

run on the emulator
### _$ flutter run -d emulator-5554 --release --dart-define=API_BASE=http://10.0.2.2:8000_


## Streamlit - Frontend <no longer supported>
open another terminal and run the fronend <br>
_$ cd frontend_ <br>
_$ streamlit run streamlit.py_ <br>




