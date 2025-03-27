current_user = None


class User:
    def __init__(self, username, balance=0):
        self.username = username
        self.balance = balance
        self.portfolio = []

    def info(self):
        print(
            f"Nuestro Usuario: {self.username} y nuestro balance actuales es de {self.balance}€")

    def delete(self):
        if current_user != None:
            current_user = None
        else:
            print("No se ha cargado ningun usuario")


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
        print("4. Buy Cryptos")
        print("5. Buy Shares")
        print("6. Salir")

        select = int(input("introduce una opcion"))

        match select:
            case 1:
                try:
                    name = input("Nombre de usuario: ")
                    balance = input("Balance Inicial: ")
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
                print("Saliendo")
                break
            case _:
                print("opcion no valida vuelva a intetarlo")


def function_info():
    pass


def function_delete():
    pass


def main():
    Menu()


if __name__ == "__main__":
    main()
