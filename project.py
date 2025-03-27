class User:
    def __init__(self, username, balance=0):
        self.username = username
        self.balance = balance
        self.portfolio = []

    def info(self):
        print(
            f"Nuestro Usuario: {self.username} y nuestro balance actuales es de {self.balance}€")


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


def main():
    Usuario1 = User("Nauzet", 1000)
    Usuario1.info()


def function_1():
    pass


def function_2():
    pass


def function_n():
    pass


if __name__ == "__main__":
    main()
