import os
import json
import shutil
from pathlib import Path

import tempfile
from tqdm import tqdm
from dotenv import load_dotenv

from tools.polly import Polly
from tools.anki import Anki

load_dotenv()

def main():

  deckname = os.getenv('DECKNAME')
  category = os.getenv('CATEGORY')
  audio_prefix = os.getenv('AUDIO_PREFIX')

  assert deckname is not None
  assert audio_prefix is not None

  with open(f'decks/{deckname}.json', 'r') as f:
    deck = json.load(f)

  with tempfile.TemporaryDirectory() as temp_dir:
    dir_path = Path(temp_dir).resolve()

    anki = Anki.create_deck(deckname, category=category)
    polly = Polly.create_from_env(dir_path)

    for i, card in enumerate(tqdm(deck)):
      french_text = card['French']
      english_text = card['English']
      audio_basename = f'{audio_prefix}_{deckname}-{i}'
      polly.create_audio(french_text, audio_basename, tempo=0.8)
      anki.add_note(french_text, english_text, dir_path / f'{audio_basename}.mp3')
      anki.add_note(english_text, french_text, dir_path / f'{audio_basename}.mp3')

    anki.package_notes(Path('packaged').resolve())

if __name__ == "__main__":
  main()
