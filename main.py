import json
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from tqdm import tqdm

from tools.anki import Anki
from tools.cli import select_deck_cli
from tools.polly import Polly

load_dotenv()


def main():

    category = os.getenv('CATEGORY')

    deckname = select_deck_cli()
    if deckname is None:
        return

    with open(f'decks/{deckname}.json', 'r', encoding="utf-8") as f:
        deck = json.load(f)

    with tempfile.TemporaryDirectory() as temp_dir:
        audio_dir = Path(temp_dir).resolve()

        anki = Anki.create_deck(deckname, category=category)
        polly = Polly.create_from_env()

        for i, card in enumerate(tqdm(deck)):
            french_text = card['French']
            english_text = card['English']
            audio_basename = f'{deckname}-{i}'
            polly.create_audio(french_text, audio_dir, audio_basename, tempo=0.8)
            anki.add_note(french_text, english_text, audio_dir, audio_basename)
            anki.add_note(english_text, french_text, audio_dir, audio_basename)

        anki.package_notes(Path('packaged').resolve())


if __name__ == "__main__":
    main()
