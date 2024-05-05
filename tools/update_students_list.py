import argparse
import pandas as pd
from typing import Dict, Optional, List
from dotenv import dotenv_values
from pymongo import MongoClient
from constants import StudentListKey, UniProgram

ARGUMENT_FILENAME_KEY = "csv_filename"
STUDENTS_LIST_COLUMNS_TO_KEEP: List[str] = [
    StudentListKey.NI,
    StudentListKey.PROGRAM_CODE,
    StudentListKey.LASTNAME,
    StudentListKey.FIRSTNAME,
    StudentListKey.NEW,
]

print(STUDENTS_LIST_COLUMNS_TO_KEEP)

STUDENT_ALLOWED_PROGRAM = [UniProgram.IFT, UniProgram.GLO, UniProgram.CERTIFICATE]
STUDENT_NOUVEAU_COLUMN_MAPPING = {"Oui": True, "Non": False}

MISSING_DISCORD_USER_ID = -1


def read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read CSV file and keep certain columns"
    )
    parser.add_argument(ARGUMENT_FILENAME_KEY, type=str, help="Path to the CSV file")
    return parser.parse_args()


def read_configurations() -> Dict[str, Optional[str]]:
    try:
        return dotenv_values("../.env")
    except FileNotFoundError as e:
        print(f".env file is not found. {e}")
        exit(-1)


def connect_to_mongo_db(connection_url: str) -> MongoClient:
    try:
        return MongoClient(connection_url)
    except ConnectionError as e:
        print(f"Unable to connect to the MongoDB. {e}")
        exit(-1)


if __name__ == "__main__":
    arguments = read_arguments()
    configurations = read_configurations()

    client = connect_to_mongo_db(
        configurations["MONGODB_LOCALHOST_SERVER_CONNECTION_STRING"]
    )
    database = client[configurations["MONGODB_DB_NAME"]]
    students = database["students"]

    students_list = pd.read_excel(
        arguments.csv_filename, usecols=STUDENTS_LIST_COLUMNS_TO_KEEP
    )
    filtered_students_list = students_list[
        students_list[StudentListKey.PROGRAM_CODE].isin(STUDENT_ALLOWED_PROGRAM)
    ].copy()

    filtered_students_list.loc[:, StudentListKey.NEW] = filtered_students_list.loc[
        :, StudentListKey.NEW
    ].replace(STUDENT_NOUVEAU_COLUMN_MAPPING)

    existing_nis = set(
        col[StudentListKey.NI] for col in students.find({}, {StudentListKey.NI: 1})
    )
    students_to_insert = [
        row.to_dict()
        for _, row in filtered_students_list.iterrows()
        if row[StudentListKey.NI] not in existing_nis
    ]

    for student in students_to_insert:
        student[StudentListKey.DISCORD_USER_ID] = MISSING_DISCORD_USER_ID

    if len(students_to_insert):
        students.insert_many(students_to_insert)

    print(f"{len(students_to_insert)} new students inserted")
    print("Students tables has been updated!")
