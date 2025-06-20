from pathlib import Path


def select_deck_cli() -> str | None:
  deck_dir = Path('decks')

  if not deck_dir.exists():
    deck_dir.mkdir()
    print('Directory was created [decks/]. To use place .json decks in directory')
    return None

  files = list(deck_dir.glob('*.json'))

  if not files:
    print("No json files found in decks dir.")
    return None

  print("Select a deck:")
  for idx, file in enumerate(files, 1):
    print(f"{idx}. {file.stem}")

  while True:
    try:
      choice = int(input("Enter the number of the deck you want to select: "))
      if 1 <= choice <= len(files):
        print()
        selected_file = files[choice - 1]
        return selected_file.stem

      print(f"Please enter a number between 1 and {len(files)}.")
    except ValueError:
      print("Invalid input. Please enter a number.")
