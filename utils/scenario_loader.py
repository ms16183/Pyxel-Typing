from pathlib import Path
import tomllib

class ScenarioLoader:
  
  def __init__(self, dirpath):
    self.dirpath = dirpath
    
    
  def load(self) -> dict:

    base = Path(self.dirpath)
    tomls = sorted(base.glob('*.toml'))

    stages = {}
    for toml in tomls:
      with toml.open('rb') as fp:
        try:
          data = tomllib.load(fp)
          stages[data['meta']['title']] = data
        except tomllib.TOMLDecodeError as e:
          raise RuntimeError(f'Invalid scenario format: {e}') from e
    return stages
          
            

if __name__ == '__main__':
  sl = ScenarioLoader('../assets/scenarios')
  out = sl.load()
  from pprint import pprint
  pprint(out)

  for stage in out.values():
    print(f"---{stage['meta']['title']}---")
    meta = stage['meta']
    scenario = stage['scenario']
    randomize = scenario['randomize']
    lines = scenario['lines']
    print('Randomize:', randomize)
    for c in lines:
      line = f"{c['prompt']} {c['command']}"
      print(line)
      line = f"{c['output']}"
      print(line)

