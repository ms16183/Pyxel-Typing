import pyxel as px

from .scene import Scene, Type
from .title_scene import TitleScene
from .playing_scene import PlayingScene
from .gameover_scene import GameoverScene
from utils.settings import g
from utils.asset_manager import AssetManager


class SceneManager:
  
  def __init__(self):

    self.scenes = []
    self.scenes.append(TitleScene(self))
    self.scenes.append(PlayingScene(self))
    self.scenes.append(GameoverScene(self))

    self.target = self.scenes[0].type

  
  def change_scene(self, to: Type, **kwargs) -> None:
    print('Change to:', to)
    print('assert:', kwargs)
    self.target = to

    for scene in self.scenes:
      if scene.type == self.target:
        scene.setup(**kwargs)
        break
    
    
  def update(self):
    for scene in self.scenes:
      if scene.type == self.target:
        scene.update()
        break
      

  def draw(self):
    px.cls(px.COLOR_BLACK)
    for scene in self.scenes:
      if scene.type == self.target:
        scene.draw()
        break


