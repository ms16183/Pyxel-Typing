import pyxel as px
from scenes.scene_manager import SceneManager
from utils.settings import g

class App:
  
  def __init__(self):

    print(g)

    TITLE = g.title
    FPS = g.fps
    SCALE = g.display_scale
    WIDTH = g.width
    HEIGHT = g.height

    px.init(WIDTH//SCALE, HEIGHT//SCALE, title=TITLE, fps=FPS, display_scale=SCALE)
    px.mouse(True)
    px.perf_monitor(False)

    sm = SceneManager()
    px.run(sm.update, sm.draw)

    

if __name__ == '__main__':
  print("Creating app.")
  app = App()

