import enum
from sqlalchemy import Enum


# TBD
class Status(enum.Enum):
    ACTIVE = "Активный"
    REPAIRING = "На ремонте"
    OUT_OF_SERVICE = "Вышел из строя"
    ON_ORDER = "На спец. заказе"
    
    
class PaymentType(enum.Enum):
    CASH = "Наличный"
    CASHLESS = "Безналичный"
    POS_TERMINAL = "POS терминал"
    INSTALLMENTS = "В рассрочку"
    
    
class TariffType(enum.Enum):
    MONTHLY = "Помесячный"
    YEARLY = "Погодовой"
    DISCOUNTED = "Льготный"
    
    
class Role(str, enum.Enum):
    DRIVER = 'Водитель'
    BABYSITTER = 'Вожатая'
    
    
    