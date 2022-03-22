from pathlib import Path

from pytest import fixture, raises

from ..client import YConverter


@fixture
def client():
    return YConverter(Path(".key").read_text().strip())


def test_convert(client: YConverter):
    result1 = client.convert(1, "USD", "PHP")
    result2 = client.convert(1, "PHP", "USD")
    assert result1 == round(1 / result2, 8)

    result3 = client.convert(1, "USDT", "TRY")
    result4 = client.convert(1, "TRY", "USDT")
    assert result3 == round(1 / result4, 8)

    with raises(ValueError):
        result3 = client.convert(1, "US", "TRY")

    assert client.convert(1550000, "try", "usd")
