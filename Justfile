default:
    @just --list

# Install the package and its dependencies in editable mode
install:
    pip install -e .

# Run the demo: prune data/raw.bib -> data/raw_output.bib using the default field set
demo: install
    bibtex-clean data/raw.bib data/raw_output.bib

# Run the demo, adding extra fields to remove on top of the defaults (space separated, FIELD or FIELD:TYPE)
demo-custom *fields: install
    bibtex-clean data/raw.bib data/raw_output.bib {{ prepend("-f ", fields) }}

# Run the test suite
test: install
    pytest
