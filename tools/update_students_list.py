import os
import argparse
import pandas as pd
from typing import Dict, Optional, List
from dotenv import dotenv_values
from pymongo import MongoClient
from constants import StudentListKey, UniProgram, Filename, StudentMongoDbKey

ARGUMENT_FILENAME_KEY = "csv_filename"
STUDENTS_LIST_COLUMNS_TO_KEEP: List[str] = [
    StudentListKey.NI,
    StudentListKey.PROGRAM_CODE,
    StudentListKey.LASTNAME,
    StudentListKey.FIRSTNAME,
    StudentListKey.NEW,
]

STUDENT_ALLOWED_PROGRAM = [
    UniProgram.IFT,
    UniProgram.GLO,
    UniProgram.CERTIFICATE,
    UniProgram.IIG,
]

STUDENT_NOUVEAU_COLUMN_MAPPING = {"Oui": True, "Non": False}
STUDENTS_LIST_RENAMING_MAPPING = {
    StudentListKey.NI: StudentMongoDbKey.NI,
    StudentListKey.FIRSTNAME: StudentMongoDbKey.FIRSTNAME,
    StudentListKey.LASTNAME: StudentMongoDbKey.LASTNAME,
    StudentListKey.PROGRAM_CODE: StudentMongoDbKey.PROGRAM_CODE,
    StudentListKey.NEW: StudentMongoDbKey.NEW,
}

MISSING_DISCORD_USER_ID = -1


def read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read CSV file and keep certain columns"
    )
    parser.add_argument(ARGUMENT_FILENAME_KEY, type=str, help="Path to the CSV file")
    return parser.parse_args()


def read_configurations() -> Dict[str, Optional[str]]:
    try:
        dot_env_filepath = get_dot_env_filepath()
        return dotenv_values(dot_env_filepath)
    except FileNotFoundError as e:
        print(f".env file is not found. {e}")
        exit(-1)


def connect_to_mongo_db(connection_url: str) -> MongoClient:
    try:
        return MongoClient(connection_url)
    except ConnectionError as e:
        print(f"Unable to connect to the MongoDB. {e}")
        exit(-1)


def read_students_csv(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path, usecols=STUDENTS_LIST_COLUMNS_TO_KEEP)


def rename_student_list_to_mongodb_schema(students_df: pd.DataFrame):
    students_df.rename(
        columns={
            StudentListKey.NI: StudentMongoDbKey.NI,
            StudentListKey.FIRSTNAME: StudentMongoDbKey.FIRSTNAME,
            StudentListKey.LASTNAME: StudentMongoDbKey.LASTNAME,
            StudentListKey.PROGRAM_CODE: StudentMongoDbKey.PROGRAM_CODE,
            StudentListKey.NEW: StudentMongoDbKey.NEW,
        },
        inplace=True,
    )


def filter_students_by_program(students_df: pd.DataFrame) -> pd.DataFrame:
    return students_df[
        students_df[StudentMongoDbKey.PROGRAM_CODE].isin(STUDENT_ALLOWED_PROGRAM)
    ].copy()


def map_nouveau_column(students_df: pd.DataFrame) -> pd.DataFrame:
    students_df.loc[:, StudentMongoDbKey.NEW] = students_df.loc[
        :, StudentMongoDbKey.NEW
    ].replace(STUDENT_NOUVEAU_COLUMN_MAPPING)
    return students_df


def get_nis_from_collection(collection) -> set:
    return set(
        col[StudentMongoDbKey.NI]
        for col in collection.find({}, {StudentMongoDbKey.NI: 1})
    )


def get_students_to_insert(students_df: pd.DataFrame, existing_nis: set) -> List:
    return [
        row.to_dict()
        for _, row in students_df.iterrows()
        if row[StudentMongoDbKey.NI] not in existing_nis
    ]


def insert_students_into_collection(collection, students_to_insert):
    if len(students_to_insert):
        collection.insert_many(students_to_insert)


def get_dot_env_filepath():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    root_directory = os.path.dirname(current_directory)
    return os.path.join(root_directory, Filename.ENV)


def main():
    arguments = read_arguments()
    configurations = read_configurations()

    client = connect_to_mongo_db(
        configurations["MONGODB_LOCALHOST_SERVER_CONNECTION_STRING"]
    )
    database = client[configurations["MONGODB_DB_NAME"]]
    students_collection = database["students"]

    students_df = read_students_csv(arguments.csv_filename)
    rename_student_list_to_mongodb_schema(students_df)

    filtered_students_df = filter_students_by_program(students_df)
    filtered_students_df = map_nouveau_column(filtered_students_df)
    existing_nis = get_nis_from_collection(students_collection)
    students_to_insert = get_students_to_insert(filtered_students_df, existing_nis)

    for student in students_to_insert:
        student[StudentMongoDbKey.DISCORD_USER_ID] = MISSING_DISCORD_USER_ID

    insert_students_into_collection(students_collection, students_to_insert)

    print(f"{len(students_to_insert)} new students inserted")
    print("Students table has been updated!")


if __name__ == "__main__":
    main()
