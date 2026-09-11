# ROPE

ROPE is a Python toolkit for RNA origami design, sequence optimization, and structure analysis. It keeps the blueprint-based logic of the earlier ROAD workflow, but presents it in a more accessible project structure with command-line tools that can be installed and used directly.

This is especially useful for academic and research workflows where the goal is to move from a blueprint to a designed RNA construct without needing to manage a collection of loose scripts or custom setup steps. ROPE is also designed to work well with parallel and project-based workflows, where multiple designs, sequence runs, or optimization jobs are handled in a clear folder structure.

Why ROPE is useful

- blueprint-driven design and analysis
- sequence optimization for target folding goals
- 3D structure building from modular RNA components
- a clear command-line workflow for research use
- compatibility with earlier naming conventions and older script-based habits

Available commands

The main commands available after installation are:

- `rope` — overview of the available tools
- `rope-build` — build a 3D structure from a blueprint
- `rope-fold` — run sequence optimization / folding workflow
- `rope-trace` — trace a blueprint into an extended dot-bracket representation
- `rope-analyse` — analyze a blueprint
- `rope-dragon` — continuous optimization workflow
- `rope-flip` — flip blueprint orientation
- `rope-library` — library helper workflow

Compatibility names are also kept available for convenience:

- `trace_pattern`
- `trace_analysis`
- `RNAbuild`
- `batch_revolvr`
- `flip_trace`

These are mainly for familiarity and smoother migration from earlier workflows.

Installation

Install ROPE from the repository root using the project installer:

```powershell
cd C:\ROPE
python install.py
```

Useful installer options:

```powershell
python install.py --help
python install.py --mode edit
python install.py --pip pipx
python install.py --force
```

- `--mode edit` installs in editable mode for development work
- `--pip pipx` uses `pipx` instead of `pip`. Used for some linux installtions as change of the system enveriomt is not allowed
- `--force` adds the force option when needed by pipx

This is intended to make the commands available on the command line directly, without extra setup steps for the user.

Known install problem

The most common issue is that the Python Scripts folder is not on the system `PATH`.

When that happens, the install completes successfully, but commands such as `rope` or `rope-build` are not found in the shell.

On Windows, pip will usually print the exact Scripts folder that needs to be added to `PATH` during installation.

If the commands are not found, do this:

1. Run the installer again:
   ```powershell
   python install.py
   ```
2. Check the output from pip carefully. It often shows the path to the Scripts directory, for example:
   ```text
   C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts
   ```
3. Open Windows Settings and search for "Environment Variables".
4. Open "Edit the system environment variables".
5. Click "Environment Variables".
6. Under "User variables", select `Path` and click "Edit".
7. Add the Scripts folder shown by pip.
8. Click "OK" and open a new terminal.
9. Try the tool overview:
   ```powershell
   rope
   ```
   `rope --help` shows the same overview.

If the command still does not work, make sure the same Python installation is used for both the install and the terminal.

Project layout

- `rope/tools/` — command-line entry points
- `rope/core/` — folding, tracing, build, and analysis logic
- `rope/io/` — file reading, blueprint parsing, and structure I/O
- `rope/model/` — data structures for RNA and modular components
- `rope/definitions/` — structural definitions and metadata
- `rope/utils/` — helper functions used across the toolkit

Adding modules to RNA_lib

To add a new module, place it under the RNA library folder and include a matching `module.toml` file:

```text
rope/data/RNA_lib/modules/<category>/<module_name>/
├── module.toml
├── <module_file>.pdb
└── optional variant files
```

The module definition should include the metadata, symbol, sequence, and default `.pdb` file. After the files are in place, run the validator so ROPE checks the new module and updates the generated module index:

```powershell
cd C:\ROPE
python rope\validation\validator.py
```

This validates the TOML metadata, checks the referenced `.pdb` files, and updates the package index so the new module is available to the build tools.