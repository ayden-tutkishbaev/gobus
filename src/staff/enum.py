import enum


class StaffRole(str, enum.Enum):
    DRIVER = 'driver'
    BABYSITTER = 'babysitter'
    
    
class ViolationType(str, enum.Enum):
    LATE = 'late'
    MISCONDUCT = 'misconduct'
    ACCIDENT = 'accident'