from requests import Session

from .models import Cache


class YConverter:

    FIAT_BASE = "https://openexchangerates.org/api/latest.json"
    CRYPTO_BASE = "https://api.binance.com/api/v3/ticker/price"

    _cache: Cache
    _session: Session

    def __init__(self, api_key: str = "") -> None:
        self._cache = Cache.from_file()
        self._session = Session()
        if api_key:
            self._cache.api_key = api_key
        assert self._cache.api_key, "Get free API key from: https://openexchangerates.org/signup/free"

        if not self._cache.price_info:
            self.fetch_currencies()
            self._cache.save()

    def _fetch_fiat_currencies(self):
        for symbol, value in self._session.get(f"{YConverter.FIAT_BASE}?app_id={self._cache.api_key}"
                                               ).json()["rates"].items():
            self._cache.cache(f"USD{symbol}", value, False)

    def _fetch_crypto_currencies(self):
        for data in self._session.get(YConverter.CRYPTO_BASE).json():
            self._cache.cache(data["symbol"], float(data["price"]), True)

    def fetch_currencies(self):
        self._fetch_fiat_currencies()
        self._fetch_crypto_currencies()

    def convert(self, amount: float, source: str, destination: str) -> float:

        def load_price(pair: str) -> float:
            if self._cache.is_fiat(pair):
                self._fetch_fiat_currencies()
                self._cache.save()
                return self._cache.price_info[pair].value
            if self._cache.is_crypto(pair):
                self._fetch_crypto_currencies()
                self._cache.save()
                return self._cache.price_info[pair].value
            raise RuntimeError(f"{source} {destination} is not FIAT nor Crypto but it's cached.")

        pair = f"{source}{destination}".upper()
        if pair in self._cache.price_info:
            if not self._cache.price_info[pair].is_outdated():
                return amount * self._cache.get_price(pair)
            else:
                return amount * load_price(pair)
        else:
            pair = f"{destination}{source}".upper()
            if pair in self._cache.price_info:
                if not self._cache.price_info[pair].is_outdated():
                    return amount / self._cache.get_price(pair)
                else:
                    return amount / load_price(pair)
        raise ValueError(f"{source} {destination} can't found in Fiat and Binance currencies")
