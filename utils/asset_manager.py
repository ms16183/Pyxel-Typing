import pyxel as px
import sys
import traceback

from .scenario_loader import ScenarioLoader

class AssetManager:

  # シングルトン
  _instance = None
  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance


  def __init__(self):

    if getattr(self, '_inited', False):
      return
    self._inited = True

    # アセットの一括ロード
    print("Assets are loaded.")
    try:
      # フォント
      self._font = px.Font('assets/fonts/umplus_j12r.bdf')

      # タイピング用文字列
      sl = ScenarioLoader('assets/scenarios')
      self._stages = sl.load()

    # アセットのロードエラー
    except Exception as e:
      traceback.print_exc(file=sys.stderr)
      print(f'Error: {e}', file=sys.stderr)

      
  @property
  def font(self):
    return self._font
  
  
  @property
  def stages(self, title=None):
    if title is None:
      return self._stages
    else:
      return self._stages[title]



    