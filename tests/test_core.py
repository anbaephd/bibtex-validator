from collections import Counter
from pathlib import Path

import pytest

from bibtex.core import BibEntry, BibField, BibFile

SAMPLE_BIB = """@article{smith2020,
\ttitle = {A Title},
\tauthor = {Smith, John},
\tyear = {2020},
\turl = {http://example.com},
\tissn = {1234-5678},
}

@inproceedings{doe2021,
\ttitle = {Another Title},
\tauthor = {Doe, Jane},
\tyear = {2021},
\turl = {http://example.org},
\turldate = {2021-01-01},
}
"""


@pytest.fixture
def sample_bib_file(tmp_path: Path) -> Path:
    path = tmp_path / "sample.bib"
    path.write_text(SAMPLE_BIB)
    return path


def test_bibfield_holds_key_and_value():
    field = BibField("author", "{Smith, John}")
    assert field.key == "author"
    assert field.value == "{Smith, John}"


def test_bibentry_str_formats_as_bibtex_entry():
    entry = BibEntry(
        type="article",
        id="smith2020",
        fields=[BibField("title", "{A Title}"), BibField("year", "{2020}")],
    )
    assert str(entry) == (
        "@article{smith2020,\n"
        "\ttitle = {A Title},\n"
        "\tyear = {2020},\n"
        "}"
    )


def test_bibfile_parses_entries(sample_bib_file: Path):
    bf = BibFile(sample_bib_file)

    assert len(bf.entries) == 2
    types = sorted(entry.type for entry in bf.entries)
    assert types == ["article", "inproceedings"]

    article = next(e for e in bf.entries if e.type == "article")
    assert article.id == "smith2020"
    field_keys = {field.key for field in article.fields}
    assert field_keys == {"title", "author", "year", "url", "issn"}


def test_bibfile_write_raises_on_same_filename(sample_bib_file: Path):
    bf = BibFile(sample_bib_file)
    with pytest.raises(ValueError):
        bf.write_bib_file(sample_bib_file)


def test_bibfile_write_produces_readable_output(sample_bib_file: Path, tmp_path: Path):
    bf = BibFile(sample_bib_file)
    output_path = tmp_path / "output.bib"
    bf.write_bib_file(output_path)

    written = BibFile(output_path)
    assert len(written.entries) == len(bf.entries)


def test_remove_bib_field_without_entry_type_removes_from_all(sample_bib_file: Path):
    bf = BibFile(sample_bib_file)
    bf.remove_bib_field("url")

    for entry in bf.entries:
        assert all(field.key != "url" for field in entry.fields)


def test_remove_bib_field_with_entry_type_scopes_removal(sample_bib_file: Path):
    bf = BibFile(sample_bib_file)
    bf.remove_bib_field("url", "article")

    article = next(e for e in bf.entries if e.type == "article")
    inproceedings = next(e for e in bf.entries if e.type == "inproceedings")

    assert all(field.key != "url" for field in article.fields)
    assert any(field.key == "url" for field in inproceedings.fields)


def test_remove_bib_field_leaves_other_fields_untouched(sample_bib_file: Path):
    bf = BibFile(sample_bib_file)
    bf.remove_bib_field("issn", "article")

    article = next(e for e in bf.entries if e.type == "article")
    remaining_keys = {field.key for field in article.fields}
    assert "issn" not in remaining_keys
    assert "title" in remaining_keys


def test_get_stats_counts_fields_per_entry_type(sample_bib_file: Path):
    bf = BibFile(sample_bib_file)
    stats = bf.get_stats()

    assert isinstance(stats, Counter)
    assert stats[("article", "title")] == 1
    assert stats[("inproceedings", "urldate")] == 1
    assert ("article", "urldate") not in stats
