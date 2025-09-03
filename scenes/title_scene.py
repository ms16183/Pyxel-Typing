import pyxel as px
from .scene import Scene, Type
from utils.asset_manager import AssetManager
from utils.settings import g
from collections import deque


class TitleScene(Scene):
  
  def __init__(self, manager):

    # アセットのロード
    assets = AssetManager()
    self.font = assets.font
    self.stages = assets.stages
    self.stages = deque(self.stages.values())

    self.manager = manager


  @property
  def type(self):
    return Type.TITLE


  def setup(self):
    pass

  
  def update(self):
    # 選択したステージをPLAYINGシーンに渡して遷移
    if px.btnp(px.KEY_RETURN):
      self.manager.change_scene(Type.PLAYING, stage=self.stages[0])

    # ステージを選択
    elif px.btnp(px.KEY_LEFT) or px.btnp(px.KEY_UP):
      self.stages.rotate(1)

    # ステージを選択
    elif px.btnp(px.KEY_RIGHT) or px.btnp(px.KEY_DOWN):
      self.stages.rotate(-1)
      
  
  
  def draw(self):

    stage = self.stages[0]
    stage_title = stage['meta']['title']
    stage_description = stage['meta']['description']

    px.text(0, 12*0, f"タイトル", px.COLOR_WHITE, self.font)
    px.text(0, 12*1, f"ステージ選択(← →)", px.COLOR_WHITE, self.font)
    px.text(0, 12*2, f"ステージ: {stage_title}", px.COLOR_WHITE, self.font)
    px.text(0, 12*3, f"説明: {stage_description}", px.COLOR_WHITE, self.font)
    

