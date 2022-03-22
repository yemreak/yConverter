from requests import Session

from .models import Cache, PairCache


class YConverter:

    FIAT_BASE = "https://free.currconv.com"
    CRYPTO_BASE = "https://api.binance.com/api/v3/ticker/price"

    __cache: Cache
    __session: Session

    def __init__(self, api_key: str = "") -> None:
        self.__cache = Cache.from_file()
        self.__session = Session()
        if api_key:
            self.__cache.api_key = api_key
        assert self.__cache.api_key, "Get free API key from: https://free.currencyconverterapi.com/free-api-key"

        self.__fetch_currencies()
        self.__cache.save()

    def __fetch_currencies(self):
        self.__cache.fiat_currencies = set(
            self.__session.get(f"{YConverter.FIAT_BASE}/api/v7/currencies?apiKey={self.__cache.api_key}").json()
            ["results"].keys()
        )
        self.__cache.crypto_currencies = set([data["symbol"] for data in self.__session.get(YConverter.CRYPTO_BASE).json()])

    def get_price(self, source: str, destination: str) -> float:

        def is_fiat_currency() -> bool:
            return source in self.__cache.fiat_currencies and destination in self.__cache.fiat_currencies

        def is_crypto_currency() -> bool:
            return f"{source}{destination}" in self.__cache.crypto_currencies or f"{destination}{source}" in self.__cache.crypto_currencies

        source, destination = source.upper(), destination.upper()
        if is_fiat_currency():
            pair = f"{source}_{destination}"
            if self.__cache.is_cached(pair):
                return self.__cache.cached_pairs[pair].value
            else:
                pair = f"{destination}_{source}"
                if self.__cache.is_cached(pair):
                    return 1 / self.__cache.cached_pairs[pair].value
                else:
                    pair = f"{source}_{destination}"
                    url = f"{YConverter.FIAT_BASE}/api/v7/convert?q={pair}&compact=ultra&apiKey={self.__cache.api_key}"
                    price = float(self.__session.get(url).json()[pair])
                    self.__cache.cached_pairs[pair] = PairCache(pair, price, False)
                    self.__cache.save()
                    return price

        if is_crypto_currency():
            pair = f"{source}{destination}"
            if self.__cache.is_cached(pair):
                return self.__cache.cached_pairs[pair].value
            else:
                pair = f"{destination}{source}"
                if self.__cache.is_cached(pair):
                    return 1 / self.__cache.cached_pairs[pair].value
                else:
                    pair = f"{source}{destination}"
                    url = f"{YConverter.CRYPTO_BASE}?symbol={pair}"
                    price = float(self.__session.get(url).json()["price"])
                    self.__cache.cached_pairs[pair] = PairCache(pair, price, True)
                    self.__cache.save()
                    return price

        raise ValueError(f"{source} {destination} can't found in Fiat and Binance currencies")

    def convert(self, amount: float, source: str, destination: str) -> float:
        return amount * self.get_price(source, destination)
