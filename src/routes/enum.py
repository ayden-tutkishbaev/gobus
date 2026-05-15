import enum

    
class Status(enum.Enum):
    ACTIVE = "active"
    REPAIRING = "repairing"
    OUT_OF_SERVICE = "out_of_service"
    ON_ORDER = "on_order"