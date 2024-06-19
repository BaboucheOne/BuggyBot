# BuggyBot
Simply a customs agent

# Building :hammer_and_wrench:
## :ship: Docker
1. Install docker for [windows](https://docs.docker.com/desktop/install/windows-install/), [macos](https://docs.docker.com/desktop/install/mac-install/) or [linux](https://docs.docker.com/desktop/install/linux-install/).
2. Run the following command `docker build --tag buggybot .`
3. Launch the image.

:warning: Make sure to modify `.env.dev` or `.env.prod`.

:warning: Default dockerfile launch Buggybot in **production**.

## :computer: On machine
1. Download [Python 3.10](https://www.python.org/downloads/release/python-3100/)
2. Download [MongoDB Community Server](https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.9-signed.msi)
3. Download [Mongo MongoDB Compass](https://downloads.mongodb.com/compass/mongodb-compass-1.43.0-win32-x64.exe)

:warning: Create two files `.env.dev` and `.env.prod` in the project root in order to interact with mongoDB. See section `.env setup` for more.

:warning: Do not forget to [sync your requirements.txt with PyCharm](https://www.jetbrains.com/help/pycharm/managing-dependencies.html).

## :gear: .env configuration
1. At the root of the project `./BuggyBot` create two files and name them `.env.dev` and `env.prod`.
2. Add the following lines for both configuration:
    ```md
    MONGODB_CONNECTION_STRING = "YOUR MONGODB CONNECTION STRING"
    MONGODB_CONNECTION_TIMEOUT_MS = YOUR TIMEOUT TIME IN MS
    MONGODB_DATABASE_NAME = "YOUR MONGODB NAME"
    STUDENT_COLLECTION_NAME = "YOUR STUDENT COLLECTION NAME"
    DISCORD_TOKEN = "YOUR DISCORD BOT TOKEN"
    SERVER_ID = YOUR SERVER ID (RIGHT CLICK ON SERVER ICON AND COPY ID)
    LOGGER_FILENAME = "YOUR LOG FILENAME"
    ```

:information_source: One file is dedicated for dev purposes (like having a local server) and the other to production (like giving the real connection string for the bd).

:information_source: If the log file is not present, it will be created automatically.

# Launching :rocket:
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
To upload a new list of students provided by the department, run:
```commandline
python ./tools/update_students_list.py FILENAME.xlsx
```

To non registered migrate members :
This command enables you to migrate members to the new bot. It will register automatically members present on the discord.
```commandline
python ./tools/migrate_discord_students.py
```
It can happen that certain members cannot be migrated du to their name being too long or that we found duplicates.
If this happens, script will ask you if you want to contact them by hand or automatically by sending them a message asking them to register.

:information_source: Note: Most of the tools commands uses `dev` by default. If you when to use the tool in production, simply add `--env prod` at the end of the command.

## Commands
To fix linter et format errors run theses two commands:
```commandline
ruff check . --fix
```
```commandline
black .
```
