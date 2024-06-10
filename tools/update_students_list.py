import os
import argparse
import pandas as pd
from typing import List
from pymongo import MongoClient

from bot.config.constants import ConfigurationFilename
from bot.config.dotenv_configuration import DotEnvConfiguration
from bot.domain.constants import UniProgram
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.infra.constants import StudentMongoDbKey
from constants import StudentCsvKey
from tools.common import get_configuration, add_configuration_argument

ARGUMENT_FILENAME_KEY = "csv_filename"
STUDENTS_LIST_COLUMNS_TO_KEEP: List[str] = [
    StudentCsvKey.NI,
    StudentCsvKey.PROGRAM_CODE,
    StudentCsvKey.LASTNAME,
    StudentCsvKey.FIRSTNAME,
    StudentCsvKey.NEW,
]

STUDENT_ALLOWED_PROGRAM = [
    UniProgram.IFT,
    UniProgram.GLO,
    UniProgram.CERTIFICATE,
    UniProgram.IIG,
]

STUDENT_NOUVEAU_COLUMN_MAPPING = {"Oui": True, "Non": False}
STUDENTS_LIST_RENAMING_MAPPING = {
    StudentCsvKey.NI: StudentMongoDbKey.NI,
    StudentCsvKey.FIRSTNAME: StudentMongoDbKey.FIRSTNAME,
    StudentCsvKey.LASTNAME: StudentMongoDbKey.LASTNAME,
    StudentCsvKey.PROGRAM_CODE: StudentMongoDbKey.PROGRAM_CODE,
    StudentCsvKey.NEW: StudentMongoDbKey.NEW_ADMITTED,
}


def read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read CSV file and keep certain columns"
    )
    parser.add_argument(ARGUMENT_FILENAME_KEY, type=str, help="Path to the CSV file")
    add_configuration_argument(parser)

    return parser.parse_args()


def read_configurations(filename: str) -> DotEnvConfiguration:
    return DotEnvConfiguration(filename)


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
            StudentCsvKey.NI: StudentMongoDbKey.NI,
            StudentCsvKey.FIRSTNAME: StudentMongoDbKey.FIRSTNAME,
            StudentCsvKey.LASTNAME: StudentMongoDbKey.LASTNAME,
            StudentCsvKey.PROGRAM_CODE: StudentMongoDbKey.PROGRAM_CODE,
            StudentCsvKey.NEW: StudentMongoDbKey.NEW_ADMITTED,
        },
        inplace=True,
    )


def filter_students_by_program(students_df: pd.DataFrame) -> pd.DataFrame:
    return students_df[
        students_df[StudentMongoDbKey.PROGRAM_CODE].isin(STUDENT_ALLOWED_PROGRAM)
    ].copy()


def map_nouveau_column(students_df: pd.DataFrame) -> pd.DataFrame:
    students_df.loc[:, StudentMongoDbKey.NEW_ADMITTED] = students_df.loc[
        :, StudentMongoDbKey.NEW_ADMITTED
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
    return os.path.join(root_directory, ConfigurationFilename.DEVELOPMENT)


def main():
    arguments = read_arguments()
    configuration: DotEnvConfiguration = get_configuration(arguments)

    client = connect_to_mongo_db(configuration.mongodb_connection_string)
    database = client[configuration.mongodb_database_name]
    students_collection = database[configuration.student_collection_name]

    students_df = read_students_csv(arguments.csv_filename)
    rename_student_list_to_mongodb_schema(students_df)

    filtered_students_df = filter_students_by_program(students_df)
    filtered_students_df = map_nouveau_column(filtered_students_df)
    existing_nis = get_nis_from_collection(students_collection)
    students_to_insert = get_students_to_insert(filtered_students_df, existing_nis)

    for student in students_to_insert:
        student[StudentMongoDbKey.DISCORD_USER_ID] = DiscordUserId.INVALID_DISCORD_ID

    insert_students_into_collection(students_collection, students_to_insert)

    client.close()

    print(f"{len(students_to_insert)} new students inserted")
    print("Students table has been updated!")


if __name__ == "__main__":
    main()
