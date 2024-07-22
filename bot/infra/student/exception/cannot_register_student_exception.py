from typing import Union

from bot.domain.student.attribut.ni import NI


class CannotRegisterStudentException(RuntimeError):

    NI_UNION = Union[NI, int]

    MESSAGE = (
        "L'étudiant %s ne peut pas être inscrit et inséré dans la base de données."
    )

    def __init__(self, ni: NI_UNION):
        super().__init__(self.MESSAGE % repr(ni))
