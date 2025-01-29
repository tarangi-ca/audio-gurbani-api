from enum import Enum

from utilities.schemas import CamelCaseBaseModel


class CreateHukamnamaEntity(CamelCaseBaseModel):
    melody: str
    writer: str
    page: int
    text: str


class MehlMapping(Enum):
    FIRST = "Guru Nanak Dev Ji"
    SECOND = "Guru Angad Dev Ji"
    THIRD = "Guru Amar Das Ji"
    FOURTH = "Guru Ram Das Ji"
    FIFTH = "Guru Arjan Dev Ji"
    SIXTH = "Guru Hargobind Ji"
    SEVENTH = "Guru Har Rai Ji"
    EIGHTH = "Guru Har Krishan Ji"
    NINTH = "Guru Tegh Bahadur Ji"
    TENTH = "Guru Gobind Singh Ji"
