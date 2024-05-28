from bot.cog.exceptions.missing_arguments_exception import MissingArgumentsException


class Utility:

    TRUE_BOOL_SET = {"true", "1", "yes", "y", "oui", "o"}

    @staticmethod
    def str_to_bool(s: str):
        return s.lower() in Utility.TRUE_BOOL_SET

    @staticmethod
    def get_content_without_command(content: str):
        args = content.split()
        if len(args) < 2:
            raise MissingArgumentsException(0)
        return " ".join(args[1:])
