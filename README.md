# A-FILM-A CINEMA

Servicio de cartelera que se encarga de mostrar las peliculas disponibles en el cine.

El diagrama de clases está estructurado de la siguiente manera con las entidades de este servicio.

## DIAGRAMA DE CLASES

> **[ AQUÍ VA EL DIAGRAMA UML - INSERTA TU IMAGEN O CÓDIGO AQUÍ ]**

---

La construcción de este servicio se desarrolló la mayor parte en Python con la librería de fastAPI que genera el yml automáticamente en cuanto se crean los endpoints de cartelera.

**Documentación OpenAPI:** https://a-film-a.onrender.com/docs

La información de las películas se obtiene de una API externa (TMDB) y el servicio está montado en un servidor Render. Se montó el servicio en Render ya que al estructurar bien el repositorio en GitHub, se puede montar de forma automática.

### Para poder hacer uso del servicio:

El servicio, se accede desde el link:
https://a-film-a.onrender.com/

**Importante:** en caso de que salga una página de estado de render; hay que esperar unos segundos en lo que inicia el servidor, ya que al ser una versión gratis detecta cuando no hay nadie haciendo solicitudes al servicio y se apaga.

De parte de frontend se hizo una página web sencilla de un solo salto, para no complicar el frontend y hacer enfoque en el backend.

---

## Estructura de carpetas

El backend se encuentra en este repositorio y está compuesto de la siguiente manera:

```text
peliculas/
├── public/
│   └── index.html
├── payment/
│   ├── __init__.py
│   └── payment.py
├── services/
│   ├── __init__.py
│   └── services.py
├── main.py
├── requirements.txt
├── Dockerfile
└── README.md
```

Para la revisión del backend todos los archivos se encuentran en este repositorio.

---

## Cosas a destacar de este proyecto:

Agregué un patrón de diseño Strategy para crear estrategias de los pagos y resulte en el principio OCP, donde el procesador de pagos está abierto a la extensión pero cerrado para la modificación, para poder extender los diferentes métodos de pago según lo requiera el aplicativo:

### ESTRATEGIAS PAYMENT

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

class TarjetaStrategy(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        # Lógica para procesar pago con Tarjeta
        print(f"Cobrando ${amount} con Tarjeta.")
        return True

class PaypalStrategy(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        # Lógica para procesar pago con PayPal
        print(f"Cobrando ${amount} con PayPal.")
        return True
```

Después de estas estrategias agregamos un Factory para poder ir construyendo los métodos de pago con su debido algoritmo en su estrategia.

### PaymentFactory

```python
class PaymentFactory:
    @staticmethod
    def GetStrategy(method: str) -> PaymentStrategy:
        if method.lower() == "tarjeta":
            return TarjetaStrategy()
        elif method.lower() == "paypal":
            return PaypalStrategy()
        else:
            raise ValueError(f"Método de pago '{method}' no soportado.")

class PaymentProcesser:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def pay(self, amount: float) -> bool:
        return self.strategy.pay(amount)
```