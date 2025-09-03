from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class GlobalSettings:
  
  width: int = 960
  height: int = 720
  display_scale: int = 2
  fps: int = 30
  title: str = 'Linux Typing'
  line_height: int = 12

  max_timer: int = 60
  max_mini_timer: int = 10
  



g = GlobalSettings()


if __name__ == '__main__':
  print(g)
  print(g.title)
  print(f'size: {g.width}x{g.height}')

