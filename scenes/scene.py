from abc import ABC, abstractmethod
from enum import Enum, auto
import pyxel as px


class Type(Enum):
  TITLE = auto()
  PLAYING = auto()
  GAMEOVER = auto()



class Scene(ABC):
  @abstractmethod
  def setup(self, **kwargs) -> None:
    raise NotImplementedError


  @abstractmethod
  def update(self) -> None:
    raise NotImplementedError


  @abstractmethod
  def draw(self) -> None:
    raise NotImplementedError

    
  @property
  @abstractmethod
  def type(self):
    raise NotImplementedError

    
