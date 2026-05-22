import enum


class PaymentType(str, enum.Enum):
    CASH = "cash"
    CASHLESS = "cashless"
    POS_TERMINAL = "pos_terminal"
    INSTALLMENTS = "installments"
    
    
class TariffType(str, enum.Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    DISCOUNTED = "discounted"