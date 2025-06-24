# Anki Deck Creator

Automates the creation of Anki flashcard decks with audio generated via Amazon Polly.

## Features

- Load vocabulary decks from JSON files.
- Generate speech audio for each flashcard using Amazon Polly.
- Create Anki flashcards with associated audio.
- Package and export the deck for easy import into Anki.
- Command-line interface to select decks.

## Setup

1. Install requirements `pip install -r requirements.txt`.
2. Setup aws polly and get api keys.
3. Create `.env` file from template and fill in aws credentials.
4. Optionally fill in category name so your decks appear in group.

## Run

```bash
main.py
```

## Prompt template:

Use this template to create decks via chatgpt or any other app. Copy json contents into file in decks directory.

```
Create a french language study plan for anki as a json in this format

[
  {
    "English": "Some phrase in english",
    "French": "The same phrase in french"
  }
]

I want this deck to include the following topics. Please include at least 50 examples.
```
