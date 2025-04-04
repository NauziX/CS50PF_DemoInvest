import yfinance as yf


current_user = None


class User:
    def __init__(self, username, balance=0):
        self.username = username
        self.balance = balance
        self.portfolio = []

    def info(self):
        print(
            f"Nuestro Usuario: {self.username} y nuestro balance actuales es de {self.balance}€")
        print("Portfolia actual: ")
        for asset in self.portfolio:
            print(f"- {asset}")

    def buy(self, product):
        if isinstance(product, Product):
            if self.balance >= product.price:
                self.portfolio.append(product)
                self.balance -= product.price
                print(f"Has Comprado: {product}")
                print(f"Balance actual: {self.balance}€")
            else:
                print("Balance insuficiente para realizar compra.")
        else:
            print("El objeto proporcianod no es un producto válido.")

    def sell(self, product):

        if isinstance(product, Product):
            self.portfolio.remove(product)
            self.balance += product.price
            print(f"Has Comprado: {product}")
            print(f"Balance actual: {self.balance}€")
        else:
            print("El objeto proporciando no es un producto válido.")


class Product:
    def __init__(self, name, symbol, price):
        self.name = name
        self.symbol = symbol
        self.price = price

    def __str__(self):
        return (f"Name: {self.name} Symbol: {self.symbol} Price: {self.price}")


class Crypto(Product):
    def __init__(self, name, symbol, price, blockchain):
        super().__init__(name, symbol, price)
        self.blockchain = blockchain


class Shares(Product):
    def __init__(self, name, symbol, price, dividend_yield=0.0):
        super().__init__(name, symbol, price)
        self.dividend_yield = dividend_yield


def Menu():

    global current_user

    while True:
        print("--------Demo Invest --------")
        print("1. Crear Usuario ")
        print("2. Eliminar Usuario ")
        print("3. Información de Usuario")
        print("4. Comprar Acciones")
        print("5. Mostrar Valor")
        print("6. Vender Productos")
        print("7. Guardar Archivo")
        print("8. Salir")

        select = int(input("introduce una opcion"))

        match select:
            case 1:
                try:
                    name = input("Nombre de usuario: ")
                    balance = int(input("Balance Inicial: "))
                    current_user = User(name, balance)
                    print("Usuario Registrado")
                except TypeError:
                    print("El Balance es un numero")

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
                buyshare = Shares(name, symbol, price)
                current_user.buy(buyshare)
                if buyshare:
                    print("accion comprada")
                else:
                    print("No has ingresado el nombre correctamente")

            case 5:
                print("Mostrar Valor")
                share = input("Que Acción/Cryptomoneda quieres verificar")
                current_sharecryp(share)

            case 6:
                for share in current_user.portfolio:
                    print(share)
                break
            case 7:
                print("Salir")
                break


def current_sharecryp(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    price = info.get('regularMarketPrice', None)
    name = info.get('longName')
    symbol = info.get('symbol')
    print(f"Nombre: {name} Simbolo: {symbol} Price: {price}")
    return name, symbol, price


def function_delete():
    pass


def main():
    Menu()


if __name__ == "__main__":
    main()
