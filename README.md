## Metode Numerik Apps 

### Feature
- Calculate the value from real

### Requirement
- Python ^3.9

### Installation 
- clone project
- create virtual env with following command (ubuntu or popos)
  ```
  python3 -m venv venv
  ```
- activate the virtual env with :
  ```
  . venv/bin/activate
  ```  
- pip install -U pip & pip install -r requirements.txt
- set env variable : 

```
FLASK_APP_NAME=metode-numerik-app
FLASK_ENV=<your deployment environment>
FLASK_DEBUG=<0 | 1>
```
- copy ``config/config.py.example`` to ``config/config.py``
- copy ``.env.example`` to ``.env`` (if you are using .env file)

### Running
```
flask run
```
