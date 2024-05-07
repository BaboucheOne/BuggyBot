import argparse


class Context:

    def __init__(self, arguments: argparse.Namespace):
        self.arguments = arguments

    def get_env_path(self) -> str:
        return self.arguments.env

