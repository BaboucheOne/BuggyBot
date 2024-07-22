class RoleNotFoundException(RuntimeError):

    MESSAGE = (
        "Le programme %s n'a pas d'équivalent pour un rôle Discord. "
        "Il sera donc impossible d'ajouter le rôle à la personne."
    )

    def __init__(self, role_name: str):
        super().__init__(self.MESSAGE % role_name)
