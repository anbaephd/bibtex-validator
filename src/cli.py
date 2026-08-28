from pathlib import Path

import click

from bibtex.core import BibFile

DEFAULT_FIELDS_TO_REMOVE: list[tuple[str, str | None]] = [
    ("file", None),
    ("note", None),
    ("keywords", None),
    ("urldate", "inproceedings"),
    ("url", "inproceedings"),
    ("url", "article"),
    ("issn", "article"),
]


def _parse_field_spec(spec: str) -> tuple[str, str | None]:
    if ":" in spec:
        field_key, entry_type = spec.split(":", 1)
        return field_key.strip(), entry_type.strip()
    return spec.strip(), None


def _validate_bib_extension(
    ctx: click.Context, param: click.Parameter, value: Path
) -> Path:
    if value.suffix != ".bib":
        raise click.BadParameter(f"'{value}' must have a .bib extension.")
    return value


@click.command()
@click.argument(
    "input_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    callback=_validate_bib_extension,
)
@click.argument(
    "output_file",
    type=click.Path(dir_okay=False, path_type=Path),
    callback=_validate_bib_extension,
)
@click.option(
    "--field",
    "-f",
    "fields",
    multiple=True,
    help=(
        "Additional field to remove, optionally scoped to an entry type as "
        "FIELD:TYPE (e.g. 'url:inproceedings'). Repeatable. Added on top of "
        "the standard SLR cleanup set."
    ),
)
@click.option(
    "--stats/--no-stats", default=True, help="Print field/entry stats after cleanup."
)
def main(input_file: Path, output_file: Path, fields: tuple[str, ...], stats: bool) -> None:
    """Prune fields from an INPUT_FILE bibtex library and write the result to OUTPUT_FILE.

    \b
    Arguments:
      INPUT_FILE   Path to the bibtex library to read.
      OUTPUT_FILE  Path to write the cleaned bibtex library to. Must not be
                   the same file as INPUT_FILE.
    """
    bf = BibFile(input_file)

    field_specs = DEFAULT_FIELDS_TO_REMOVE + [_parse_field_spec(f) for f in fields]

    for field_key, entry_type in field_specs:
        bf.remove_bib_field(field_key, entry_type)

    bf.write_bib_file(output_file)

    if stats:
        click.echo(bf.get_stats())


if __name__ == "__main__":
    main()
