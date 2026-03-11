from pathlib import Path

from bibtex.core import BibFile


def main() -> None:

    filename_input = Path("/Users/anbae/phd/projects/bibtex-validator/data/raw.bib")
    filename_output = Path(
        "/Users/anbae/phd/projects/bibtex-validator/data/raw_output.bib"
    )

    bf = BibFile(filename_input)

    bf.remove_bib_field("file")
    bf.remove_bib_field("address")
    bf.remove_bib_field("abstract")
    bf.remove_bib_field("inproceedings", "copyright")
    bf.remove_bib_field("article", "url")
    # bf.remove_bib_field("title", "inproceedings")
    # bf.remove_bib_field("urldate", "inproceedings")
    # bf.remove_bib_field("urldate", "outproceedings")
    # bf.remove_bib_field("year", "misc")
    bf.write_bib_file(filename_output)

    print(bf.get_stats())


if __name__ == "__main__":
    main()
