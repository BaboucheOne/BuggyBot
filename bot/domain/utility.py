class Utility:

    TRUE_BOOL_SET = {"true", "1", "yes", "y", "oui", "o"}

    @staticmethod
    def str_to_bool(s: str):
        if s.lower() not in Utility.TRUE_BOOL_SET:
            return False
        return True
