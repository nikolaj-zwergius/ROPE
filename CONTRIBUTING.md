# Working on ROPE

ROPE is maintained and directed by its maintainer. This guide is for
maintainer-directed work, including AI-assisted changes. The maintainer decides
the scope and expected behavior of changes; a plan or implementation is not
self-approved.

## Team workflow

- Main contributors should work from the shared ROPE repository, not personal
  forks. Create a separate Git branch in the shared ROPE repository for each
  task, with a short name that describes the task. Keep unrelated work on
  separate branches.
- If a task depends on unfinished work on another branch, tell the maintainer
  and agree whether to wait for that branch to merge or deliberately base the
  new branch on it.
- Keep each branch focused on its approved task. Explain any dependencies when
  handing the work back for review, and wait for maintainer review before
  treating the work as accepted.

## Setup

ROPE requires Python 3.10.12 or newer. The project installer installs from the
repository's `pyproject.toml`:

```shell
python install.py --mode edit
```

Editable mode is intended for development. The runtime dependencies and
installed command names are declared in `pyproject.toml`. Use the README's
installation section for the supported end-user installation workflow.

## Project structure

- `rope/tools/` contains command-line wrappers and argument parsing.
- `rope/core/` contains reusable design, tracing, build, analysis, and variant
  logic.
- `rope/api.py` exposes Python-level entry points. Check its current contents
  before relying on an operation being part of the public API.
- `rope/io/` contains blueprint, module, TOML, index, and structure I/O.
- `rope/model/` contains domain objects and typed records.
- `rope/definitions/` contains shared Python objects, such as predefined lists,
  constants, and shared paths.
- `rope/validation/` contains RNA library validation and index generation.
- `rope/data/` contains the RNA library, module definitions, and generated
  indexes.

Prefer implementing behavior in reusable Python functions and calling those
functions from the CLI wrappers.

## Adding an RNA library module

Follow the existing instructions and example in `README.md`. In general, a
module belongs in a category folder under
`rope/data/RNA_lib/modules/<category>/<module-name>/`, with a `module.toml`
definition and the referenced structure file(s). Use the metadata schema in
existing module definitions; do not guess at fields or create a separate
format.

The validator checks module definitions and files, then rewrites the generated
`rope/data/index` and `rope/data/variant_index`. Before running it:

- Check `git status` and preserve existing changes to module data and indexes.
- Confirm with the maintainer before overwriting existing user changes.
- After validation, inspect the index diffs and ensure only intended entries
  changed.