# Docker container - Backend <stable version> :
from project root run

### _$ docker compose run --build_

it will creat a docker container with all the necessary python pacakages and will start the **FastApi** Server


# Install required python packages and start the server manually. skip this step youn are using docker.

from <project_root>/backend run to install the python dependen:
### _$ pip install -r requirements.py_

## Start FastAPI Server
_$ cd backend_ <br>
_$ uvicorn app:app --host 0.0.0.0 --port 8000_


## Flutter - Frontend
Open another terminal to start the bot <br>
cd to frontend<br>
_$ flutter run -d chrome --release --dart-define=API_BASE=http://localhost:8000_ <br>

## Streamlit - Frontend <no longer supported>
open another terminal and run the fronend <br>
_$ cd frontend_ <br>
_$ streamlit run streamlit.py_ <br>




