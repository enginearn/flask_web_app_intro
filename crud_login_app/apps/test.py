from pathlib import Path

print(Path(Path(__file__).parent, 'db.sqlite3'))
print(f'{Path(__file__).parent.parent}')

