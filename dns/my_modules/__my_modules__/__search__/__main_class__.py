from typing import TypeVar
T = TypeVar("T")
from .__sub__ import create_async_func
from .__from_global__ import from_global

class Searcher:
  def __init__(self):
    self.from_global = create_async_func(from_global)

searcher = Searcher()