import yfinance as yf
import json


""" 
    We import the necessary libraries: yfinance and json.
    yfinance: used to fetch real-time market prices for financial assets.
    json: used to save and load data in JSON format.
"""


current_user = None

"""
We define the classes User, Product, and its subclass Shares. 
The classes and functions are designed with scalability in mind, 
since currently we only have one type of user and one financial product, 
but we know there are many others (e.g., bonds, crypto assets, mutual funds...).
"""


class User:
    def __init__(self, username, balance=0, portfolio=[]):
        self.username = username
        self.balance = balance
        self.portfolio = portfolio
        self.startacc = balance

    def info(self):

        total_shares = value_shares()
        total_acc = (self.balance + total_shares) - self.startacc
        print(
            f"Your account was created with an initial balance of: {self.startacc}$")
        print(f"Your current balance is: {self.balance}$")
        print(f"Your shares are worth: {total_shares}$")
        if total_acc >= 0:
            print(f"Your total gain is: {total_acc}$")
        else:
            print(f"Your total loss is: {total_acc}$")

    def buy(self, product):

        if isinstance(product, Shares):
            total_price = product.price * product.unit
            print(total_price)
            if self.balance >= total_price:
                self.portfolio.append(product)
                self.balance -= total_price
                print(f"Purchased: {product}, {product.unit} units")
                print(f"Updated balance: {self.balance}$")
            else:
                print("Insufficient balance to complete the purchase.")
        else:
            print("The provided object is not a valid product.")

    def sell(self, product):

        if not isinstance(product, Product):
            return print("The provided object is not a valid product.")
        product_in_portfolio = next(
            (p for p in self.portfolio if p.symbol == product.symbol), None)

        if product_in_portfolio is None:
            return print("You do not own this product in your portfolio.")

        if product.unit > product_in_portfolio.unit:
            return print(f"You do not have enough units of {product.symbol} to sell.")

        real_share = yf.Ticker(product.symbol)
        info = real_share.info
        price = info.get('regularMarketPrice', None)

        if price is None:
            return print("Failed to retrieve the current price for the product.")

        product_in_portfolio.unit -= product.unit
        if product_in_portfolio.unit == 0:
            self.portfolio.remove(product_in_portfolio)

        total_sale = price * product.unit
        self.balance += total_sale

        print(
            f"You sold {product.unit} units of {product.symbol} for {total_sale:.2f}$")
        print(f"Updated balance: {self.balance:.2f}$")


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
Generates a console-based menu using a while loop, with basic exception handling for user input.
"""


def Menu():

    global current_user

    while True:
        print("-------- Demo Invest --------")
        print("1. Create User")
        print("2. Delete User")
        print("3. Show User Information")
        print("4. Buy Shares")
        print("5. Show Portfolio")
        print("6. Sell Shares")
        print("7. Save Data")
        print("8. Load Data")
        print("9. Exit")

        try:
            select = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        match select:
            case 1:
                try:
                    name = input("Username: ")
                    balance = int(input("Initial Balance: "))
                    current_user = User(name, balance)
                    print("User successfully created.")
                except ValueError:
                    print("Balance must be a valid number.")

            case 2:
                if current_user is None:
                    print("No user currently loaded to delete.")
                else:
                    current_user = None
                    print("User deleted.")

            case 3:
                if current_user is None:
                    print("No user is currently loaded.")
                else:
                    current_user.info()

            case 4:
                share = input(
                    "Enter the symbol of the stock you want to buy: ")
                name, symbol, price = current_sharecryp(share)
                try:
                    unit = int(input("How many units?: "))
                    buyshare = Shares(name, symbol, price, unit)
                    current_user.buy(buyshare)
                    print("Share purchased.")
                except ValueError:
                    print("Invalid number of units.")

            case 5:
                print("Displaying portfolio summary:")
                for asset in current_user.portfolio:
                    print(asset)

            case 6:
                for share in current_user.portfolio:
                    print(share)

                symbol = input(
                    "Which stock would you like to sell?: ").strip().upper()
                try:
                    unit = int(
                        input("How many units would you like to sell?: "))
                    product_to_sell = Shares(
                        name="", symbol=symbol, price=0, unit=unit)
                    current_user.sell(product_to_sell)
                except ValueError:
                    print("Invalid number of units.")

            case 7:
                save_data()
                print("Data successfully saved.")

            case 8:
                load_data()
                print("Data successfully loaded.")

            case 9:
                print("Exiting program.")
                break

            case _:
                print("Please select a valid option from the menu.")


"""
get_share_info()
Validates whether the stock symbol exists and retrieves its information 
before adding it to the user's portfolio.
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
Saves all current_user data to a JSON file for later retrieval.
"""


def save_data():

    data = {
        "Username": current_user.username,
        "Balance": current_user.balance,
        "Start": current_user.startacc,
        "Portfolio": [
            {
                "Name": asset.name,
                "Symbol": asset.symbol,
                "Price": asset.price,
                "Units": asset.unit
            }
            for asset in current_user.portfolio
        ]
    }

    with open("CS50PF_DemoInvest\datos.json", "w") as file:
        json.dump(data, file, indent=4)


"""
load_data()
Loads user data from a JSON file and restores all information into current_user.
"""


def load_data():

    global current_user
    name = ""
    balance = 0
    portfolio = []
    startacc = 0

    with open("CS50PF_DemoInvest\datos.json", "r") as file:
        loaded_data = json.load(file)

    name = loaded_data["Username"]
    balance = loaded_data["Balance"]
    portfolio = loaded_data["Portfolio"]
    startacc = loaded_data["Start"]

    current_user = User(name, balance, portfolio=[])
    current_user.startacc = startacc

    for item in portfolio:
        if item not in current_user.portfolio:
            share = Shares(item["Name"], item["Symbol"],
                           item["Price"], item["Units"])
            current_user.portfolio.append(share)

    return current_user


def sell_shares():
    """
    sell_shares()
    Validates whether the sale is possible and calls the User class method to complete the transaction.
    """

    print(f"Current balance: {current_user.balance}€")
    print("Your current shares:")

    for asset in current_user.portfolio:
        market_data = yf.Ticker(asset.symbol.strip())
        info = market_data.info
        price = info.get('regularMarketPrice', None)
        print(f"{asset.symbol} - Buy price: {asset.price}€, Current price: {price}$")

    symbol_to_sell = input(
        "Enter the symbol of the stock you want to sell: ").strip().upper()

    product_to_sell = next(
        (asset for asset in current_user.portfolio if asset.symbol.upper() == symbol_to_sell), None)

    if product_to_sell:
        current_user.sell(product_to_sell)
    else:
        print("That stock was not found in your portfolio.")


def value_shares():
    """
    value_shares()
    Calculates the current total market value of the user's portfolio.
    """

    total_value = 0
    for asset in current_user.portfolio:
        market_data = yf.Ticker(asset.symbol.strip())
        info = market_data.info
        price = info.get('regularMarketPrice', None)
        if price is not None:
            total_value += price * asset.unit

    return total_value


def main():
    Menu()


if __name__ == "__main__":
    main()
