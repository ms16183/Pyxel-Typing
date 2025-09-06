import pyxel as px
from .scene import Scene, Type
from utils.asset_manager import AssetManager
from utils.settings import g

class GameoverScene(Scene):
  
  def __init__(self, manager):

    am = AssetManager()
    self.font = am.font

    self.manager = manager


  @property
  def type(self):
    return Type.GAMEOVER


  def setup(self, **kwargs):
    # ステージ情報があるかチェック
    if 'is_success' not in kwargs:
      raise RuntimeError ('Playing scene needs is_success.')
    if 'lines' not in kwargs:
      raise RuntimeError ('Playing scene needs lines.')
    if 'timer' not in kwargs:
      raise RuntimeError ('Playing scene needs time.')
    if 'ok' not in kwargs:
      raise RuntimeError ('Playing scene needs OK and NG.')
    if 'ng' not in kwargs:
      raise RuntimeError ('Playing scene needs OK and NG.')
    if 'ok_characters' not in kwargs:
      raise RuntimeError ('Playing scene needs characters.')
    if 'ng_characters' not in kwargs:
      raise RuntimeError ('Playing scene needs characters.')
    

    # 結果
    self.is_success = kwargs['is_success']
    self.timer = kwargs['timer']
    self.lines = kwargs['lines']
    self.ok = kwargs['ok']
    self.ok_characters = kwargs['ok_characters']
    self.ng = kwargs['ng']
    self.ng_characters = kwargs['ng_characters']

    # スコア = (正しい打鍵数 - 誤った打鍵数) / 合計打鍵数
    self.sum_characters = sum([len(l['command']) for l in self.lines if l is not None])
    self.score = int(max(self.ok_characters - self.ng_characters, 0) * 100 / self.sum_characters)
  
  def update(self):
    if px.btnp(px.KEY_RETURN):
      self.manager.change_scene(Type.TITLE)
      
  
  def draw(self):

    # n行目
    n = 0
    
    if self.is_success:
      px.text(0, 12*n, f'リザルト: 成功', px.COLOR_WHITE, self.font)
    else:
      px.text(0, 12*n, f'リザルト: 失敗', px.COLOR_WHITE, self.font)
    n += 2
    px.text(0, 12*n, f'OK: {self.ok}', px.COLOR_GREEN, self.font)
    n += 1
    px.text(0, 12*n, f'NG: {self.ng}', px.COLOR_RED, self.font)
    n += 1
    px.text(0, 12*n, f'スコア: {self.score}点', px.COLOR_WHITE, self.font)
    n += 1
    px.text(0, 12*n, f'完了時間: {g.max_timer - self.timer / g.fps:.1f}秒', px.COLOR_WHITE, self.font)
    n += 2
    px.text(0, 12*n, 'Enterでタイトルへ', px.COLOR_WHITE, self.font)
    n += 1
    

