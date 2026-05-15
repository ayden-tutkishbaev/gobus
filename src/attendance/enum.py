import enum


class KidStatus(str, enum.Enum):
    PRESENT = 'present'
    ABSENT = 'absent'
    NOT_MARKED = 'not_marked'