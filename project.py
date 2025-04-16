import yfinance as yf
import json

""" 
    Importamos las librerias necesiria yfincance y json
    yfinance: donde sacamos el precio de los valores en el mercado financiero
    json: para para poder guardar y cargar archivos en Json

"""


current_user = None

"""
Creamos las Clases User Product y su hija Shares, creo las clases y las funciones
con el pensamiento de poder scalar el proyecto mas facilmente y porque en este caso solo
tenemos un tipo de usuario y un producto financiareo pero sabemos que hay muchos mas
ejempl: bonos cryptoactivos fondos....
"""


class User:
    def __init__(self, username, balance=0, portfolio=[]):
        self.username = username
        self.balance = balance
        self.portfolio = portfolio
        self.startacc = balance

    def info(self):
        total_shares = valor_shares()
        total_acc = (self.balance + total_shares) - self.startacc
        print(f"Tu Cuenta fue creada con el importe de:{self.startacc}")
        print(f"Tu Balanze acutal es de: {self.balance}")
        print(f"Tus Acciones Valen: {total_shares}")
        if total_acc >= 0:
            print(f"tus ganancias son de:{total_acc}")
        else:
            print(f"tus perdidas son de:{total_acc}")

    def buy(self, product):
        if isinstance(product, Shares):
            total_price = product.price * product.unit
            print(total_price)
            if self.balance >= total_price:
                self.portfolio.append(product)
                self.balance -= total_price
                print(f"Has Comprado: {product},{product.unit} unidades")
                print(f"Balance actual: {self.balance}€")
            else:
                print("Balance insuficiente para realizar compra.")
        else:
            print("El objeto proporcianod no es un producto válido.")

    def sell(self, product):

        if not isinstance(product, Product):
            return print("El objeto proporcionado no es un producto válido.")
        producto_en_portafolio = next(
            (p for p in self.portfolio if p.symbol == product.symbol), None)

        if producto_en_portafolio is None:
            return print("No tienes este producto en tu portafolio.")

        if product.unit > producto_en_portafolio.unit:
            return print(f"No tienes suficientes unidades de {product.symbol} para vender.")

        real_share = yf.Ticker(product.symbol)
        info = real_share.info
        price = info.get('regularMarketPrice', None)

        if price is None:
            return print("No se pudo obtener el precio actual del producto.")

        producto_en_portafolio.unit -= product.unit
        if producto_en_portafolio.unit == 0:
            self.portfolio.remove(producto_en_portafolio)

        total_venta = price * product.unit
        self.balance += total_venta

        print(
            f" Has vendido {product.unit} unidades de {product.symbol} por {total_venta:.2f}€")
        print(f" Balance actual: {self.balance:.2f}€")


class Product:
    def __init__(self, name, symbol, price):
        self.name = name
        self.symbol = symbol
        self.price = price

    def priceinfo(self):
        return self.price


class Shares(Product):
    def __init__(self, name, symbol, price, unit=0, dividend_yield=0.0):
        super().__init__(name, symbol, price)
        self.dividend_yield = dividend_yield
        self.unit = unit

    def __str__(self):
        return (f"Name: {self.name} Symbol: {self.symbol} Price: {self.price} x {self.unit}")


"""
Menu()
Generamos un menu por consola a travez de while donde tambien intetamos controlar de excepciones
"""


def Menu():

    global current_user

    while True:
        print("--------Demo Invest --------")
        print("1. Crear Usuario ")
        print("2. Eliminar Usuario ")
        print("3. Información de Usuario")
        print("4. Comprar Acciones")
        print("5. Mostrar Portfolio")
        print("6. Vender Productos")
        print("7. Guardar Archivo")
        print("8. Cargar Archivo")
        print("9. Salir")

        select = int(input("introduce una opcion:"))

        match select:
            case 1:

                try:
                    name = input("Nombre de usuario: ")
                    balance = int(input("Balance Inicial: "))
                    current_user = User(name, balance)
                    print("Usuario Registrado")
                except TypeError:
                    print("El Balance no es un numero")

            case 2:

                if current_user is None:
                    print("No hay ningún usuario cargado para eliminar.")
                else:
                    current_user = None
                    print("Usuario eliminado.")

            case 3:
                if current_user is None:
                    print("No hay ningún usuario cargado todavía.")
                else:
                    current_user.info()
            case 4:
                share = input(print("Accion que quieres comprar"))
                name, symbol, price = current_sharecryp(share)
                unit = int(input("Cuantas unidades:"))
                buyshare = Shares(name, symbol, price, unit)
                current_user.buy(buyshare)
                if buyshare:
                    print("accion comprada")
                else:
                    print("No has ingresado el nombre correctamente")

            case 5:
                print("Mostrando Resultados")
                current_user.info()

            case 6:

                for share in current_user.portfolio:
                    print(share)

                symbol = input("¿Qué acción quieres vender?: ").strip().upper()
                unit = int(input("¿Cuántas unidades quieres vender?: "))
                producto_para_vender = Shares(
                    name="", symbol=symbol, price=0, unit=unit)
                current_user.sell(producto_para_vender)

            case 7:
                save_data()
                print("Datos guardados correctamente")

            case 8:
                load_data()
                print("Datos cargados correctamente ")

            case 9:
                print("Salir")
                break

            case _:
                print("Selecciona una opcion del menu")


"""
current_sharecryp()
Donde validamos si la accion existe para luego poder incorporar al portfolio del cliente
"""


def current_sharecryp(ticker_symbol):

    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    price = info.get('regularMarketPrice', None)
    name = info.get('longName')
    symbol = info.get('symbol')
    print(f"Nombre: {name} Simbolo: {symbol} Price: {price}")
    return name, symbol, price


"""
save_data()
Funcion para guardar los datos a travez de un Json recogemos todos los datos de current_user
"""


def save_data():

    datos = {
        "Usuario": current_user.username,
        "Balance": current_user.balance,
        "Start": current_user.startacc,
        "Portfolio": [
            {"Name": asset.name, "Symbol": asset.symbol,
                "Price": asset.price, "Units": asset.unit}
            for asset in current_user.portfolio]
    }

    with open("CS50PF_DemoInvest\datos.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)


"""
load_data()
Funcion para cargar los datos a travez de un Json y cargamos todos los datos a current_user
"""


def load_data():

    global current_user
    name = ""
    balance = 0
    portfolio = []
    startacc = 0
    with open("CS50PF_DemoInvest\datos.json", "r") as archivo:
        datos_cargados = json.load(archivo)

    name = datos_cargados["Usuario"]
    balance = datos_cargados["Balance"]
    portfolio = datos_cargados["Portfolio"]
    startacc = datos_cargados["Start"]

    current_user = User(name, balance, portfolio=[])
    current_user.startacc = startacc

    for a in portfolio:
        if a not in current_user.portfolio:
            date = Shares(a["Name"], a["Symbol"], a["Price"], a["Units"])
            current_user.portfolio.append(date)

    return current_user


"""
sell_shares()
Validamos que la venta sea posible y usamos la funcion en la clase para terminar de vender
"""


def sell_shares():

    print(f"El balance actual es de {current_user.balance}")
    "Tus acciones son:"

    for a in range(len(current_user.portfolio)):
        valor_actual = yf.Ticker(
            current_user.portfolio[a].symbol.strip())
        info = valor_actual.info
        price = info.get('regularMarketPrice', None)
        print(
            f"{current_user.portfolio[a].symbol} Buy price:{current_user.portfolio[a].price} Valor Actual:{price}")

    symbol_to_sell = input(
        "Introduce el símbolo de la acción que quieres vender: ").strip().upper()
    producto_a_vender = next(
        (asset for asset in current_user.portfolio if asset.symbol.upper() == symbol_to_sell), None)

    if producto_a_vender:
        current_user.sell(producto_a_vender)
    else:
        print("No se encontró esa acción en tu portafolio.")


"""
valor_shares()
con esta funcion sacamos el valor actual de nuesto portfolio
"""


def valor_shares():

    total_valor = 0
    for a in range(len(current_user.portfolio)):
        valor_actual = yf.Ticker(current_user.portfolio[a].symbol.strip())
        info = valor_actual.info
        price = info.get('regularMarketPrice', None)
        total_valor += price * current_user.portfolio[a].unit

    return total_valor


def main():
    Menu()


if __name__ == "__main__":
    main()
