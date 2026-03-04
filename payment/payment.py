from abc import ABC, abstractmethod
from typing import Dict, Type

class PaymentStrategy(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CardPayment(PaymentStrategy):
    def process(self, amount: float) -> bool:
        print(f"Procesando ${amount} con Tarjeta de Crédito... ¡Aprobado!")
        return True

class PayPalPay(PaymentStrategy):
    def process(self, amount: float) -> bool:
        print(f"Redirigiendo a PayPal por ${amount}... ¡Completado!")
        return True


# Principio de Abierto/Cerrads.procesaro OCP
# Patrón de diseño Factory para obtener la estrategia de pago adecuada sin modificar el código existente
class PaymentFactory:
    _strategies: Dict[str, Type[PaymentStrategy]] = {
        "tarjeta": CardPayment,
        "paypal": PayPalPay,
    }

    @classmethod
    def GetStrategy(cls, method: str) -> PaymentStrategy:
        StrategyClass = cls._strategies.get(method.lower())
        if not StrategyClass:
            raise ValueError(f"Método de pago '{method}' no soportado")
        return StrategyClass() # Instanciamos y devolvemos

class PaymentProcesser:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def pay(self, amount: float) -> bool:
        return self.strategy.process(amount)