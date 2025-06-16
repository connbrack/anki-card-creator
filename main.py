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
  audio_prefix = os.getenv('AUDIO_PREFIX')

  assert deckname is not None
  assert audio_prefix is not None

  with open(f'decks/{deckname}.json', 'r') as f:
    deck = json.load(f)

  with tempfile.TemporaryDirectory() as temp_dir:
    dir_path = Path(temp_dir).resolve()

    anki = Anki.create_deck(deckname)
    polly = Polly.create_from_env(dir_path)

    for i, card in enumerate(tqdm(deck)):
      french_text = card['French']
      english_text = card['English']
      audio_filename = f'{audio_prefix}_{deckname}-{i}.mp3'
      polly.create_audio(french_text, audio_filename, tempo=0.8)
      anki.add_note(french_text, english_text, dir_path / f'{audio_filename}.mp3')
      anki.add_note(english_text, french_text, dir_path / f'{audio_filename}.mp3')

    anki.package_notes(Path('packaged').resolve())

if __name__ == "__main__":
  main()
