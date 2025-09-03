import pyxel as px
from .scene import Scene, Type
from utils.asset_manager import AssetManager
from utils.settings import g
from random import shuffle
from collections import deque


class PlayingScene(Scene):
  
  def __init__(self, manager):

    am = AssetManager()
    self.font = am.font

    self.manager = manager


  @property
  def type(self):
    return Type.PLAYING


  def setup(self, **kwargs):

    # ステージ情報があるかチェック
    if 'stage' not in kwargs:
      raise RuntimeError ('Playing scene needs stage data.')

    # ステージ情報
    self.stage = kwargs['stage']
    # シナリオ
    self.scenario = self.stage['scenario']
    # 行
    self.lines = self.scenario['lines']
    # ランダマイズ
    if self.scenario['randomize']:
      shuffle(self.lines)
    # キュー保存
    self.lines = deque(self.lines)
    # キューの最後にNoneを追加
    self.lines.append(None)

    # 全体のタイマー
    self.timer = g.max_timer * g.fps
    # 問題ごとのタイマー
    self.mini_timer = g.max_mini_timer * g.fps
    # ユーザの入力
    self.user_input = ''
    # 入力成功回数
    self.ok_counter = 0
    self.ok_characters = 0
    # 入力失敗回数
    self.ng_counter = 0
    self.ng_characters = 0


  
  def update(self):
    # タイマーを減算
    self.timer -= 1
    self.mini_timer -= 1
    # 時間が経過するとゲームオーバ
    if self.timer < 0 or self.mini_timer < 0:
      self.manager.change_scene(Type.GAMEOVER,
                                is_success=False, 
                                lines=self.lines,
                                timer=self.timer,
                                ok=self.ok_counter,
                                ng=self.ng_counter,
                                ok_characters=self.ok_characters,
                                ng_characters=self.ng_characters)

    # キー入力を取得
    self.get_user_input()
    # ユーザが入力を確定した時
    if px.btnp(px.KEY_RETURN):
      # 末尾の連続した空白を削除して
      self.user_input = self.user_input.rstrip()
      # 入力が正しければ
      if self.user_input == self.lines[0]['command']:

        # -----------------------------------------------#

        # 末尾に現在のラインを移動し，次のラインを取り出す
        self.lines.rotate(-1)

        # -----------------------------------------------#

        # 入力成功回数をカウントする
        self.ok_counter += 1
        # 入力成功した分の文字数をカウントする
        self.ok_characters += len(self.user_input)

        # -----------------------------------------------#

        # ユーザの入力をクリアする
        self.user_input = ''
        # タイマーをリセットする
        self.mini_timer = g.max_mini_timer * g.fps

        # -----------------------------------------------#

        # 問題が全て完了するとゲームオーバ
        if self.lines[0] is None:
          self.manager.change_scene(Type.GAMEOVER,
                                    is_success=True, 
                                    lines=self.lines,
                                    timer=self.timer,
                                    ok=self.ok_counter,
                                    ng=self.ng_counter,
                                    ok_characters=self.ok_characters,
                                    ng_characters=self.ng_characters)

      # 入力が誤っていれば
      else:
        # 入力失敗回数をカウントする
        self.ng_counter += 1
        self.ng_characters += len(self.user_input)
  
  
  def draw(self):

    # n行目
    n = 0

    # タイマー
    px.rect(0, 12*n,
            int(g.width*self.timer/(g.max_timer*g.fps)/g.display_scale), 12,
            px.COLOR_ORANGE)
    n += 1
    px.rect(0, 12*n,
            int(g.width*self.mini_timer/(g.max_mini_timer*g.fps)/g.display_scale), 12,
            px.COLOR_ORANGE)
    n += 1

    # 入力成功回数
    px.text(0, 12*n, f'OK: {self.ok_counter:02d}', px.COLOR_GREEN, self.font)
    n += 1
    # 入力失敗回数
    px.text(0, 12*n, f'NG: {self.ng_counter:02d}', px.COLOR_RED, self.font)
    n += 1
    
    # 横線
    bold = 3
    px.rect(0, 12*n, g.width / g.display_scale, bold, px.COLOR_WHITE)
    px.rect(0, g.height / g.display_scale - bold, g.width / g.display_scale, bold, px.COLOR_WHITE)
    # 縦線
    px.rect(0, 12*n, bold, g.height / g.display_scale, px.COLOR_WHITE)
    px.rect(g.width / g.display_scale - bold, 12*n, bold, g.height / g.display_scale, px.COLOR_WHITE)
    n += 2

    # 1つ前の行を取得
    if self.lines[-1] is not None:
      prompt = self.lines[-1]['prompt']
      command = self.lines[-1]['command']
      output = self.lines[-1]['output']

      # 1つ前の行のプロンプトを表示
      px.text(12+0, 12*n, prompt, px.COLOR_GRAY, self.font)
      # 1つ前の行のコマンドを表示(+1は空白)
      px.text(12+6*(len(prompt)+1), 12*n, self.visible_space(command), px.COLOR_GRAY, self.font)
      n += 1
      # 1つ前の行の結果を表示
      for o in output.splitlines():
        px.text(12+0, 12*n, o, px.COLOR_GRAY, self.font)
        n += 1
        # 画面の7割を超えたら表示しない
        if n > g.height / g.display_scale / 12 * 0.7:
          px.text(12+0, 12*n, '...', px.COLOR_GRAY, self.font)
          n += 1
          break
      n += 1
      
    # ラインがある場合
    if self.lines[0] is not None:
      line = self.lines[0]
      prompt = line['prompt']
      command = line['command']
      output = line['output']

      # 画面高さの半分の位置，前回のコマンドが長すぎる場合はその1行下の位置から開始
      n = int(max((g.height / g.display_scale / 12) * 0.5, n+1))

      # プロンプトを表示
      px.text(12+0, 12*n, prompt, px.COLOR_WHITE, self.font)
      # コマンドを表示(+1は空白)
      px.text(12+6*(len(prompt)+1), 12*n, self.visible_space(command), px.COLOR_WHITE, self.font)
      # ユーザの入力を表示
      px.text(12+6*(len(prompt)+1), 12*n, self.visible_space(self.user_input), px.COLOR_GREEN, self.font)
      n += 1
      # カーソルを表示
      px.text(12+6*(len(prompt)+1+len(self.user_input)), 12*n, '^',px.COLOR_GREEN, self.font)

    
  def get_user_input(self):
    # 英字+数字+記号
    self.user_input += px.input_text if px.input_keys != px.KEY_UNKNOWN else ''
    
    # 削除
    if px.btnp(px.KEY_BACKSPACE) and len(self.user_input) > 0:
      self.user_input = self.user_input[:-1]

  
  def visible_space(self, s, symbol=' '):
    return s.replace(' ', symbol) 
