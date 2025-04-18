from project import User, Shares


def test_buy_shares_success():
    user = User("testuser", balance=1000)
    share = Shares(name="Apple", symbol="AAPL", price=100, unit=5)
    user.buy(share)

    assert len(user.portfolio) == 1
    assert user.balance == 1000 - (100 * 5)
    assert user.portfolio[0].symbol == "AAPL"


def test_calculate_portfolio_value_manually():
    fake_portfolio = [
        Shares("A", "AAA", 10, unit=2),
        Shares("B", "BBB", 5, unit=4)]

    total_value = sum(asset.price * asset.unit for asset in fake_portfolio)

    assert total_value == 40


def test_shares_str_representation():
    share = Shares("Apple", "AAPL", 150, unit=3)
    expected = "Name: Apple Symbol: AAPL Price: 150 x 3"
    assert str(share) == expected
