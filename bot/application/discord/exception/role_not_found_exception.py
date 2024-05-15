class RoleNotFoundException(Exception):

    MESSAGE = "Role %s not found."

    def __init__(self, role_name):
        super().__init__(self.MESSAGE % role_name)
