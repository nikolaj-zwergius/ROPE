# ROPE Project Structure

ROPE is a Python toolkit for RNA origami design, sequence optimization, and
structure analysis. This diagram gives a visual overview of the repository and
the main responsibilities of its folders.

```text
ROPE/
├── rope/                          Python package
│   ├── tools/                     Command-line entry points
│   ├── core/                      Reusable design and computation logic
│   ├── io/                        Blueprint, TOML, PDB, and package I/O
│   ├── model/                     RNA and structural domain objects
│   ├── definitions/               Shared definitions and constants
│   ├── utils/                     Shared helper utilities
│   ├── validation/                Module and structure validation
│   ├── data/                      Packaged runtime data
│   │   ├── RNA_lib/
│   │   │   ├── modules/           RNA modules, metadata, and PDB structures
│   │   │   └── nucleotides/       Standard nucleotide PDB structures
│   │   ├── index                  Generated module index
│   │   ├── variant_index          Generated variant index
│   │   ├── kl_compatibility       Kissing-loop compatibility data
│   │   ├── kl_list                Kissing-loop list data
│   │   └── module_metadata.toml   Shared module metadata
│   ├── api.py                     Package-level API
│   ├── helper.py                  Command overview
│   └── version.py                 Package version
├── install.py                     Project installer
├── pyproject.toml                 Package configuration and CLI registrations
├── README.md                      Overview, installation, and usage
├── CONTRIBUTING.md                Contribution guidance
└── TODO.md                        Project backlog
```

## Architecture and implementation

ROPE is divided by responsibility: command-line tools orchestrate work,
reusable modules implement domain operations, I/O translates between files and
in-memory representations, and packaged data supplies reusable RNA structures.

```text
Command-line user
       │
       ▼
rope/tools/       Parse options and orchestrate a task
       │
       ▼
rope/core/        Trace, analyze, optimize, map, and build
       │                   │
       ▼                   ▼
rope/model/       rope/io/             rope/data/
Domain objects    File formats          Module metadata and coordinates
       └───────────────┬───────────────────┘
                       ▼
                Results and reports
```

This is the intended separation of concerns, not a strict dependency rule
enforced everywhere in the current code. In particular, inspect the actual
call path before refactoring an established tool.

### Core representations

- **Blueprint grid:** `generate_np_pattern` reads a blueprint into a padded
  two-dimensional NumPy character array. Grid mapping and backbone traversal
  use this representation.
- **Traced design:** `trace_backbone` walks the grid and produces nucleotide
  sequence order, a dot-bracket-like pairing string, and coordinate maps. This
  converts the spatial blueprint into a sequence-indexed representation used
  by analysis, folding, and building.
- **Pairing map:** `map_structure` converts the pairing string into partner
  indices. Separate bracket types support crossing pairs.
- **Module mapping:** the build path assigns library module symbols to traced
  positions. The builder aligns the selected module coordinates along the
  backbone and writes the PDB structure.

These are important hand-off points. A change to blueprint interpretation or
tracing may affect several tools, so check the consumers of both the traced
sequence and pairing data.

### Design principles

- Keep command-line parsing and user-facing orchestration in `rope/tools/`;
  place reusable domain behavior in `rope/core/` or a focused package module.
- Represent structural modules as data: `module.toml` describes a module and
  references coordinate files, which the loader and builder consume.
- Keep design interpretation separate from 3D realization. Tracing and
  sequence-level analysis do not require assembling a PDB model.
- Centralize shared domain rules such as nucleotide alphabets, pairing tables,
  structural markers, and common paths rather than redefining them per tool.

### Where to make common changes

- **Blueprint or trace semantics:** start with `rope/core/grid_mapping.py`
  and `rope/core/trace_logic.py`; then inspect analysis, folding, and building
  code that consumes the traced representation.
- **Sequence optimization:** inspect `rope/core/revolvr.py` and the relevant
  command in `rope/tools/`. Keep candidate generation and scoring reusable
  independently of command-line arguments.
- **3D assembly:** follow `rope/core/Build_logic.py` with module mapping,
  loading, caching, and PDB output.
- **RNA library content:** add metadata and coordinate files under
  `rope/data/RNA_lib/modules/`, following a neighboring module. Run
  `rope-library` or `python rope/validation/validator.py` to validate module
  data and regenerate indexes; review generated changes before keeping them.
- **File formats and reporting:** keep parsing and serialization in `rope/io/`
  rather than embedding format details in command-line entry points.

There are no dedicated test files in the repository at present. The library
validator is an available focused check for module-data changes. For algorithm
changes, add or run an appropriate automated check when a test harness is
available, and distinguish manual checks from automated verification.

### Implementation maturity

Command registration does not necessarily mean a feature is complete.
`rope-variant`, for example, currently calls a placeholder implementation.
Inspect the implementation and current backlog before planning work based on a
tool's name or help text.

## Main package areas

- `rope/tools/` contains user-facing command-line entry points for building,
  tracing, analysis, folding/optimization, library operations, variants, and
  multimer workflows.
- `rope/core/` contains reusable computation, including build, trace, analysis,
  module mapping, and variant generation.
- `rope/io/` handles blueprint, TOML, PDB, package, and index input/output.
- `rope/model/` defines modules, nucleotides, structural elements, and related
  data structures.
- `rope/data/` contains RNA structures, module definitions, and generated
  indexes distributed with the package.
- `rope/validation/` checks RNA library modules and structures.

RNA library module folders generally contain a `module.toml` definition and
one or more PDB structure files. The validator checks these files and maintains
the generated indexes.

Command-line commands are registered in `pyproject.toml` and implemented under
`rope/tools/`. Reusable behavior belongs in the core or another appropriate
package module so it can also be called without invoking a command-line tool.
