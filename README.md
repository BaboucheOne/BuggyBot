# BuggyBot
Simply a customs agent

#Directories

##Bot
This directory contains all the source code.

##Tools
This directory contains tools to help development. Add all python files that will help you to dev easier.

:warning: This directory should not be called from the `Bot` directory.

:arrow_right: You can use constants from the Bot directory if needed.

# Contribution
- Download Python 3.8.10 via https://www.python.org/downloads/release/python-3810/
- Download MongoDB Community Server via https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.9-signed.msi
- Download Mongo MongoDB Compass via https://downloads.mongodb.com/compass/mongodb-compass-1.43.0-win32-x64.exe

:warning: Create a `.env` in the project root in order to interact with mongoDB. See section `.env setup` for more.

:warning: Do not forget to sync your requirements.txt. See section below.

## Adding package to project
Sync your requirements.txt with PyCharm via https://www.jetbrains.com/help/pycharm/managing-dependencies.html

## .env configuration
- At the root of the project `./BuggyBot` create a file and name it `.env`.
- Add the following lines:
```md
MONGODB_LOCALHOST_SERVER_CONNECTION_STRING = "YOUR MONGODB CONNECTION STRING"
MONGODB_DB_NAME = "YOUR MONGODB NAME"
```

##Commands
To fix linter et format error run theses two commands
```md
> ruff check . --fix
> black .
```
