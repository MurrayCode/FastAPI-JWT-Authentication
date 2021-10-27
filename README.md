FastAPI backend with JWT authentication


Setup

    create virtual enviroment (python3 -m virtualenv venv)
    run venv (source venv/bin/activate)
    install dependancies (pip3 install -r requirements.txt)
    
Create Database

    Open python shell in terminal 
    enter the following:
        import services.database
        services.database.create_database()

Run Server

    Make sure venv is activated (source venv/bin/activate)
    Run start.sh in terminal (./start.sh)