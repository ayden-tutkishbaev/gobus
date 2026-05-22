import enum


class Role(str, enum.Enum):
    USER = 'user'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'
    
    
class UserRole(str, enum.Enum):
    USER = 'user'
    ADMIN = 'admin'
