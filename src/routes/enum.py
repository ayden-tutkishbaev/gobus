import enum

    
class Status(enum.Enum):
    ACTIVE = "active"
    REPAIRING = "repairing"
    OUT_OF_SERVICE = "out_of_service"
    ON_ORDER = "on_order"
    
    
class Direction(enum.Enum):
    HOME_TO_SCHOOL = 'home_to_school'
    SCHOOL_TO_HOME = 'school_to_home'