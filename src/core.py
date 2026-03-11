from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BibField:
    key: str
    value: str


@dataclass
class BibEntry:
    type: str
    id: str
    fields: list[BibField] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        entry_str = f"@{self.type}{{{self.id},\n"
        for field in self.fields:
            entry_str += f"\t{field.key} = {field.value},\n"
        entry_str += "}"
        return entry_str


@dataclass
class BibFile:
    filename: Path
    entries: list[BibEntry] = field(default_factory=lambda: [])
    raw_entries: list[list[str]] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.raw_entries = self.parse_bib_file()
        self.entries = [self.parse_entry(entry) for entry in self.raw_entries]
        self.entries = sorted(self.entries, key=lambda x: x.type)

    def parse_bib_file(self) -> list[list[str]]:
        with open(self.filename, "r") as f:
            content = f.read().splitlines()

        # find start line of entry
        start_lines = [i for i, line in enumerate(content) if line.startswith("@")]
        # find end line of entry
        end_lines = [i for i, line in enumerate(content) if line.startswith("}")]

        # split into list of list for each entry
        return [content[start:end] for start, end in zip(start_lines, end_lines)]

    def parse_entry(self, entry: list[str]) -> BibEntry:
        # extract entry type and key
        first_line = entry[0]
        type, id = first_line.split("{")
        type = type[1:].lower()
        id = id[:-1]

        fields = []
        for line in entry[1:]:
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip().lower(), value.strip().rstrip(",")
            fields.append(BibField(key, value))

        return BibEntry(type, id, fields)

    def write_bib_file(self, filename: Path) -> None:
        if filename == self.filename:
            raise ValueError("Output filename cannot be the same as input filename.")
        with open(filename, "w") as f:
            f.write("\n\n".join([str(i) for i in self.entries]) + "\n")

    def remove_bib_field(self, field_key: str, entry_type: str = None) -> None:
        entries = []
        for entry in self.entries:
            if entry_type is not None and entry.type != entry_type:
                entry.fields
            else:
                entry.fields = [
                    field for field in entry.fields if field.key != field_key
                ]

            entries.append(entry)

        self.entries = entries

    def get_stats(self) -> Counter:
        x = [
            (entry.type, field.key) for entry in self.entries for field in entry.fields
        ]
        return Counter(x)
