# ROPE agent guidance

## Ownership and collaboration

- ROPE is owned and directed by its maintainer. The AI's role is to help implement and explain work; the maintainer's understanding and decisions take priority.
- Before making code changes, create or update `plan.md` for the overall task. Include the goal, expected inputs and outputs, relevant existing files or functions, the proposed approach, and how the work will be verified. Read-only inspection is allowed while preparing the plan; wait for explicit maintainer approval before changing code.
- The plan approval and roughly-10-lines confirmation rules apply to code changes only. They do not require approval for requested edits to plans, TODO lists, contributor/agent guidance, or other project-workflow documentation. Keep plans at task level rather than planning every small function adjustment. For code changes, if the task scope or approach changes, or a proposed change is larger than roughly 20 lines or 1 function, explain the change and get confirmation before proceeding.
- Treat uppercase `TODO.md` as the canonical backlog. Work on one item at a time; avoid combining unrelated work and mark an item complete only when its intended behavior is implemented and verified.
- Main contributors should work from the shared ROPE repository, not personal forks. Create a separate task branch in that shared repository for each task. Keep unrelated tasks on separate branches and use a short branch name that identifies the task. If a task depends on unfinished work from another branch, tell the maintainer and agree whether to wait for that branch to merge or deliberately build on it.
- Treat the repository and branch workflow above as the default, not an unchangeable restriction: follow the user's explicit instructions for the current task if they choose a different workflow. Do not infer a user's role from GitHub credentials or inspect, expose, or request secrets. If role or repository access matters and is unclear, ask the user which workflow to use.
- Never delete or overwrite project files, user data, or generated results without explicit maintainer approval. Plan approval alone does not grant permission to delete or overwrite. Check and preserve pre-existing working-tree changes.
- Explain changes in plain language: what changed, why, how it works, what was checked, and any remaining uncertainty.

## Project structure and architecture

- Follow the existing project structure and coding patterns when they remain clear and correct. Prefer straightforward, explicit, cohesive code that the maintainer or a new maintainer can understand and safely change.
- `rope/tools/` contains user-facing command-line entry points; `rope/core/` contains reusable computation; `rope/io/` handles file and package I/O; `rope/model/` defines domain objects; `rope/definitions/` contains shared Python objects such as predefined lists, constants, and shared paths; `rope/data/` holds library and other runtime data; `rope/validation/` validates library modules and generated indexes.
- Keep core computation independent of command-line parsing and user-interface code. Reuse existing functions before adding new logic; avoid duplicating behavior between a CLI tool and a Python caller.
- Keep ROPE's command-line interface as a supported user interface, with reusable behavior implemented in Python functions that can be called without invoking command-line entry points. Keep core computation independent of command-line parsing and user-interface code.
- Keep Python modules focused. When a file starts to contain distinct responsibilities, consider splitting it into clearly named modules; around 500 lines is a prompt to review, not a strict limit.

## Code conventions

- Annotate every function and method parameter and return value with useful type hints, including `None` for functions that return no value. Do not annotate `self` or `cls`.
- Give every function and method a docstring that explains its purpose and the expected input and output formats. Document relevant units, file formats, accepted values, side effects, and raised exceptions when they are not obvious. Keep simple docstrings concise and follow the project's established style.


## Dependencies, data, and validation

- Reuse existing dependencies where practical. Discuss and justify new dependencies before adding them, including their effect on installation and packaging.
- Avoid machine-specific paths. Use paths derived from the package or project, or paths selected by the user.
- RNA library modules live under `rope/data/RNA_lib/modules/` and use `module.toml` metadata with referenced structure files. Follow the existing schema and examples rather than inventing a parallel format.
- The validator regenerates `rope/data/index` and `rope/data/variant_index`. Review the working tree before running it, preserve existing changes, and do not overwrite existing user changes without explicit approval.

## Verification

- Inspect the relevant implementation and available checks before changing behavior. Run focused tests or checks when available, and report exactly what was run.
- Do not assume a test framework or claim automated coverage that the repository does not provide. If behavior needs manual verification, describe the steps and results and identify any gaps.
- Keep `README.md`, `CONTRIBUTING.md`, and `TODO.md` accurate when a change alters setup, architecture, data formats, or remaining work.
