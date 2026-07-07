# 203local Data Engine v0.3 — Field Dictionary Update

This update adds:

- `taxonomy/field_dictionary.xlsx`
- `scripts/field_dictionary_loader.py`

## How to install

Copy the folders/files into your existing:

`~/Documents/203local-data-engine`

Allow Finder to merge folders.

## How to test

In VS Code Terminal:

```bash
cd ~/Documents/203local-data-engine
python3 scripts/field_dictionary_loader.py
```

You should see:
- Loaded field dictionary: 104 fields
- Required fields count
- Website export fields count
