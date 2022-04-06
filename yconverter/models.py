from dataclasses import dataclass, field
from os import environ
from pathlib import Path
from time import time

from ruamel.yaml import YAML, yaml_object

yaml = YAML()


@yaml_object(yaml)
@dataclass
class PriceInfo:

    FIAT_CACHE_TIME = 10 * 60
    CRPYTO_CACHE_TIME = 1 * 60

    value: float
    is_crypto: bool

    timestamp: float = field(init=False)

    def __post_init__(self):
        self.timestamp = time()

    def is_outdated(self) -> bool:
        cache_time = PriceInfo.FIAT_CACHE_TIME if self.is_crypto else PriceInfo.CRPYTO_CACHE_TIME
        return time() - self.timestamp > cache_time


@yaml_object(yaml)
@dataclass
class Cache:

    PATH = Path(f"{environ['HOME']}/yconverter.yml")

    api_key: str = field(default="")
    price_info: dict[str, PriceInfo] = field(default_factory=dict)

    @classmethod
    def from_file(cls):
        return yaml.load(Cache.PATH) if (Cache.PATH.exists() and Cache.PATH.read_text() != "") else cls()

    def is_cached(self, pair: str) -> bool:
        return pair in self.price_info and not self.price_info[pair].is_outdated()

    def is_fiat(self, pair: str) -> bool:
        return pair in self.price_info and not self.price_info[pair].is_crypto

    def is_crypto(self, pair: str) -> bool:
        return pair in self.price_info and self.price_info[pair].is_crypto

    def cache(self, pair: str, value: float, is_crypto: bool):
        self.price_info[pair.upper()] = PriceInfo(value, is_crypto)

    def get_price(self, pair: str) -> float:
        return self.price_info[pair].value

    def save(self):
        yaml.dump(self, Cache.PATH)
