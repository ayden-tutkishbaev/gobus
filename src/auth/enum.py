import enum


class Role(str, enum.Enum):
    SUPERADMIN = 'superadmin'
    ADMIN = 'admin'
    BABYSITTER = 'babysitter'
    DRIVER = 'driver'
    PARENT = 'parent'
    
    
class UserRole(str, enum.Enum):
    BABYSITTER = 'babysitter'
    DRIVER = 'driver'