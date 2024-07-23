from typing import Union

from bot.domain.student.attribut.ni import NI
from bot.infra.student.exception.mongo_fail_operation_exception import (
    MongoFailOperationException,
)


class CannotUnregisterStudentException(MongoFailOperationException):

    NI_UNION = Union[NI, int]

    MESSAGE = "L'étudiant %s n'a pas été désenregistré."

    def __init__(self, ni: NI_UNION):
        super().__init__(self.MESSAGE % repr(ni))
