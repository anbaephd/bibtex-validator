from pathlib import Path

import pytest
from click.testing import CliRunner

from bibtex.cli import DEFAULT_FIELDS_TO_REMOVE, _parse_field_spec, main
from bibtex.core import BibFile

SAMPLE_BIB = """@article{smith2020,
\ttitle = {A Title},
\tauthor = {Smith, John},
\tyear = {2020},
\turl = {http://example.com},
\tissn = {1234-5678},
\tnote = {some note},
}

@inproceedings{doe2021,
\ttitle = {Another Title},
\tauthor = {Doe, Jane},
\tyear = {2021},
\turl = {http://example.org},
\turldate = {2021-01-01},
\tabstract = {an abstract},
}
"""


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def sample_bib_file(tmp_path: Path) -> Path:
    path = tmp_path / "sample.bib"
    path.write_text(SAMPLE_BIB)
    return path


def test_parse_field_spec_without_entry_type():
    assert _parse_field_spec("note") == ("note", None)


def test_parse_field_spec_with_entry_type():
    assert _parse_field_spec("url:inproceedings") == ("url", "inproceedings")


def test_parse_field_spec_strips_whitespace():
    assert _parse_field_spec(" url : inproceedings ") == ("url", "inproceedings")


def test_main_applies_default_fields(runner: CliRunner, sample_bib_file: Path, tmp_path: Path):
    output_file = tmp_path / "output.bib"
    result = runner.invoke(main, [str(sample_bib_file), str(output_file)])

    assert result.exit_code == 0, result.output

    bf = BibFile(output_file)
    for entry in bf.entries:
        field_keys = {field.key for field in entry.fields}
        for field_key, entry_type in DEFAULT_FIELDS_TO_REMOVE:
            if entry_type is None or entry_type == entry.type:
                assert field_key not in field_keys


def test_main_prints_stats_by_default(runner: CliRunner, sample_bib_file: Path, tmp_path: Path):
    output_file = tmp_path / "output.bib"
    result = runner.invoke(main, [str(sample_bib_file), str(output_file)])

    assert result.exit_code == 0
    assert "Counter(" in result.output


def test_main_no_stats_suppresses_output(runner: CliRunner, sample_bib_file: Path, tmp_path: Path):
    output_file = tmp_path / "output.bib"
    result = runner.invoke(main, [str(sample_bib_file), str(output_file), "--no-stats"])

    assert result.exit_code == 0
    assert result.output.strip() == ""


def test_main_extra_field_added_on_top_of_defaults(
    runner: CliRunner, sample_bib_file: Path, tmp_path: Path
):
    output_file = tmp_path / "output.bib"
    result = runner.invoke(
        main, [str(sample_bib_file), str(output_file), "-f", "abstract:inproceedings"]
    )

    assert result.exit_code == 0, result.output

    bf = BibFile(output_file)
    inproceedings = next(e for e in bf.entries if e.type == "inproceedings")
    assert all(field.key != "abstract" for field in inproceedings.fields)
    # defaults are still applied alongside the extra field
    assert all(field.key != "url" for field in inproceedings.fields)


def test_main_rejects_nonexistent_input(runner: CliRunner, tmp_path: Path):
    missing = tmp_path / "missing.bib"
    output_file = tmp_path / "output.bib"
    result = runner.invoke(main, [str(missing), str(output_file)])

    assert result.exit_code != 0
    assert "does not exist" in result.output


def test_main_rejects_non_bib_input_extension(
    runner: CliRunner, sample_bib_file: Path, tmp_path: Path
):
    bad_input = tmp_path / "sample.txt"
    bad_input.write_text(SAMPLE_BIB)
    output_file = tmp_path / "output.bib"

    result = runner.invoke(main, [str(bad_input), str(output_file)])

    assert result.exit_code != 0
    assert ".bib extension" in result.output


def test_main_rejects_non_bib_output_extension(
    runner: CliRunner, sample_bib_file: Path, tmp_path: Path
):
    output_file = tmp_path / "output.txt"
    result = runner.invoke(main, [str(sample_bib_file), str(output_file)])

    assert result.exit_code != 0
    assert ".bib extension" in result.output
