# BuggyBot
Simply a customs agent

# Directories

## Bot
This directory contains all the source code.
### Launching :rocket:
In production:
```commandline
python main.py --env prod
```

In development:
```commandline
python main.py --env dev
```

## Tools
This directory contains tools to help development. Add all python files that will help you to dev easier.

:warning: This directory should not be called from the `Bot` directory.

:arrow_right: You can use constants from the Bot directory if needed.

### Commands
To upload a new list of students provided by the department, run :
```commandline
python ./tools/update_students_list.py FILENAME.xlsx
```

# Contribution
- Download Python 3.8.10 via https://www.python.org/downloads/release/python-3810/
- Download MongoDB Community Server via https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.9-signed.msi
- Download Mongo MongoDB Compass via https://downloads.mongodb.com/compass/mongodb-compass-1.43.0-win32-x64.exe

:warning: Create two files `.env.dev` and `.env.prod` in the project root in order to interact with mongoDB. See section `.env setup` for more.

:warning: Do not forget to sync your requirements.txt. See section below.

## Adding package to project
Sync your requirements.txt with PyCharm via https://www.jetbrains.com/help/pycharm/managing-dependencies.html

## .env configuration
- At the root of the project `./BuggyBot` create two files and name them `.env.dev` and `env.prod`.
- Add the following lines:
```md
MONGODB_CONNECTION_STRING = "YOUR MONGODB CONNECTION STRING"
MONGODB_DATABASE_NAME = "YOUR MONGODB NAME"
STUDENT_COLLECTION_NAME = "YOUR STUDENT COLLECTION NAME"
DISCORD_TOKEN = "YOUR DISCORD BOT TOKEN"
SERVER_ID = "YOUR SERVER ID (RIGHT CLICK ON SERVER ICON AND COPY ID)"
```

Note: One file is dedicated for dev purposes (like having a local server) and the other to production (like giving the real connection string for the bd)

## Commands
To fix linter et format error run theses two commands
```commandline
ruff check . --fix
```
```commandline
black .
```
