import random
from pathlib import Path

import genanki


class Anki:

    def __init__(self, deckname: str, deck: genanki.Deck, model: genanki.Model):
        self._deckname = deckname
        self._deck = deck
        self._model = model
        self._audio_files = []

    @staticmethod
    def create_deck(deckname: str, category: str | None = None):
        if category:
            deck_loc = f'{category}::{deckname}'
        else:
            deck_loc = deckname

        deck_id = random.randrange(1 << 30, 1 << 31)
        my_deck = genanki.Deck(
            deck_id,
            deck_loc
        )

        model = genanki.Model(
            random.randrange(1 << 30, 1 << 31),
            'Simple Model with Audio',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
                {'name': 'Audio'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><br>{{Audio}}',
                },
            ],
            css="""
                .card {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                }
                """
        )
        return Anki(deckname, my_deck, model)

    def add_note(self, front_text: str, back_text: str, audio_filepath: Path):

        my_note = genanki.Note(
            model=self._model,
            fields=[front_text, back_text, f'[sound:{audio_filepath.name}]']
        )

        self._deck.add_note(my_note)
        self._audio_files.append(audio_filepath)

    def package_notes(self, output_path: Path):
        output_path.mkdir(exist_ok=True)
        genanki.Package(self._deck, media_files=self._audio_files).write_to_file(
            f'{output_path}/{self._deckname}.apkg')
