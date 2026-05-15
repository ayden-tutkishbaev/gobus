import enum


class PaymentType(str, enum.Enum):
    CASH = "Наличный"
    CASHLESS = "Безналичный"
    POS_TERMINAL = "POS терминал"
    INSTALLMENTS = "В рассрочку"
    
    
class TariffType(str, enum.Enum):
    MONTHLY = "Помесячный"
    YEARLY = "Погодовой"
    DISCOUNTED = "Льготный"