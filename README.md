# bibtex-validator

A small Python toolkit for cleaning up BibTeX libraries — handy when preparing
reference lists for a systematic literature review (SLR), where you often want
to strip noisy fields (`file`, `note`, `keywords`, `url`, ...) before sharing
or archiving a `.bib` file.

## Requirements

- Python >= 3.13
- [`just`](https://github.com/casey/just) (optional, for the demo/dev recipes)

## Installation

```bash
pip install -e .
```

This installs the `bibtex` package and its dependencies, and puts the
`bibtex-clean` command on your `PATH`.

## Usage

```bash
bibtex-clean INPUT_FILE OUTPUT_FILE [OPTIONS]
```

Prune fields from `INPUT_FILE` and write the cleaned library to
`OUTPUT_FILE`.

```bash
bibtex-clean data/raw.bib data/raw_output.bib
```

By default this removes a standard set of noisy fields:

| Field      | Entry type      |
|------------|------------------|
| `file`     | any              |
| `note`     | any              |
| `keywords` | any              |
| `urldate`  | `inproceedings`  |
| `url`      | `inproceedings`  |
| `url`      | `article`        |
| `issn`     | `article`        |

### Options

| Option                  | Description                                                                                  |
|--------------------------|-----------------------------------------------------------------------------------------------|
| `-f`, `--field FIELD`    | Remove an additional field, on top of the defaults. Repeatable. Use `FIELD:TYPE` to scope removal to one entry type (e.g. `url:inproceedings`). |
| `--stats` / `--no-stats` | Print a summary of remaining fields per entry type after cleanup (default: on).                |
| `--help`                 | Show usage information.                                                                        |

### Examples

Also remove the `abstract` field, on top of the default set:

```bash
bibtex-clean data/raw.bib data/clean.bib -f abstract
```

Also remove `abstract` from `inproceedings` entries only:

```bash
bibtex-clean data/raw.bib data/clean.bib -f abstract:inproceedings
```

## Demo (via `just`)

A [`Justfile`](Justfile) is included to try the tool without remembering the
exact commands:

```bash
just demo
```

Runs `bibtex-clean` against the sample library in `data/raw.bib` and writes the
result to `data/raw_output.bib` using the default field set.

```bash
just demo-custom "note" "url:article"
```

Same demo, but with extra fields removed on top of the defaults.

```bash
just test
```

Runs the test suite.

Run `just --list` to see all available recipes.

## Development

Optional dependency groups are provided for development and testing:

```bash
pip install -e ".[dev,test]"
```
