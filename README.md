# PTUA11_PyGame
Role Playing Game based on PyGame with databases.

## Installation
#### Create virtual environment in project's root directory:
```commandline
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

* Add venv python.exe as the project interpreter. Settings(Ctrl+Alt+S)->Add Interpreter->Add Local Interpreter->Existing->...->Then
choose the path to python.exe in your venv folder
 [C:\Users\user\PycharmProjects\PTUA11_PyGame\venv\Scripts\python.exe]
## Setting environment variables
##### Set these variables in Shell or use a `.env` file for that

See [.env.example](.env.example) file.
```Shell
APP_NAME=RPG Debug
SQLALCHEMY_TRACK_MODIFICATIONS=False
FPS=60
```

## Loading database
```commandline
python seed_db.py
```
## Running
##### Running the game:
```commandline
python game.py
```