from dataclasses import dataclass, field
from os import environ
from pathlib import Path
from time import time

from ruamel.yaml import YAML, yaml_object

yaml = YAML()


@yaml_object(yaml)
@dataclass
class PairCache:

    FIAT_CACHE_TIME = 10 * 60
    CRPYTO_CACHE_TIME = 1 * 60

    pair: str
    value: float
    is_crypto: bool

    timestamp: float = field(init=False)

    def __post_init__(self):
        self.timestamp = time()

    def is_outdated(self) -> bool:
        cache_time = PairCache.FIAT_CACHE_TIME if self.is_crypto else PairCache.CRPYTO_CACHE_TIME
        return time() - self.timestamp > cache_time


@yaml_object(yaml)
@dataclass
class Cache:

    PATH = Path(f"{environ['HOME']}/currencyconverterapi.yml")

    api_key: str = field(default="")
    fiat_currencies: set[str] = field(default_factory=set)
    crypto_currencies: set[str] = field(default_factory=set)
    cached_pairs: dict[str, PairCache] = field(default_factory=dict)

    @classmethod
    def from_file(cls):
        return yaml.load(Cache.PATH) if (Cache.PATH.exists() and Cache.PATH.read_text() != "") else cls()

    def is_cached(self, pair: str) -> bool:
        return pair in self.cached_pairs and not self.cached_pairs[pair].is_outdated()

    def save(self):
        yaml.dump(self, Cache.PATH)
