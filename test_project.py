from project import User, Shares, save_data, load_data, current_user


def test_buy_shares_success():
    user = User("testuser", balance=1000)
    share = Shares(name="Apple", symbol="AAPL", price=100, unit=5)
    user.buy(share)

    assert len(user.portfolio) == 1
    assert user.balance == 1000 - (100 * 5)
    assert user.portfolio[0].symbol == "AAPL"


def test_value_shares_basic():

    global current_user
    current_user = User("tester", balance=500)
    current_user.portfolio.append(Shares("Apple", "AAPL", 0, unit=1))

    total = value_shares()
    assert isinstance(total, (int, float))


def test_save_and_load_user_data():
    global current_user
    current_user = User("demo", balance=300)
    current_user.portfolio.append(Shares("Microsoft", "MSFT", 50, unit=2))

    save_data()
    loaded_user = load_data()

    assert loaded_user.username == "demo"
    assert loaded_user.portfolio[0].symbol == "MSFT"
    assert loaded_user.portfolio[0].unit == 2
