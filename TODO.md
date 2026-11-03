# ROPE TODO

Use this file as the canonical active backlog. Work on one item at a time and
confirm behavior or output details with the maintainer where the request leaves
them open.

Priority is P1 (high), P2 (medium), or P3 (low). Difficulty is an estimate from
1 (small, well-understood change) to 5 (large or uncertain work); it describes
implementation effort and uncertainty, not importance.


- [ ] [P1][Difficulty: 2/5] Add a 120-degree kissing-loop module to the RNA library, following existing metadata and structure-file conventions.
- [ ] [P1] [Difficulty: 4/5] Add support for AKL and 120-degree kissing loops in Revolvr and Multimer `@` labels.
  - [ ] [Difficulty: 3/5] Add kissing-loop lists for AKL and the 120-degree kissing loop so `@` labels can identify and use both.
  - [ ] [Difficulty: 3/5] Update Revolvr to accept and handle AKL and 120-degree kissing-loop `@` labels.
  - [ ] [Difficulty: 3/5] Update Multimer to accept and handle AKL and 120-degree kissing-loop `@` labels.
  - [ ] [Difficulty: 2/5] Verify both tools with representative blueprints and report unsupported or invalid label cases clearly.

- [ ] [P2] [Difficulty: 4/5] Implement generation of multiple variants from one blueprint. Confirm the expected inputs, variant-selection behavior, and output format with the maintainer before settling the interface.

- [ ] [P2] [Difficulty: 4/5] Add ViennaRNA support for modified nucleic acids.
  - [ ] [Difficulty: 2/5] Check ViennaRNA's supported modified-nucleotide inputs and confirm the target modifications and expected behavior with the maintainer.
  - [ ] [Difficulty: 4/5] Integrate the confirmed representation into ROPE's folding workflow without changing behavior for standard RNA sequences.
  - [ ] [Difficulty: 3/5] Add focused tests for modified and standard sequences, including clear errors for unsupported modifications.

- [ ] [P2] [Difficulty: 4/5] Add multistate support to structure building so every defined state for a module is built.
  - [ ] [Difficulty: 2/5] Confirm how module states are represented and how separate state structures should be named or returned.
  - [ ] [Difficulty: 4/5] Update the build logic to produce a structure for each defined state while preserving current behavior for single-state modules.
  - [ ] [Difficulty: 3/5] Add tests for single-state modules, two-state modules, and invalid or missing state data.

- [ ] [P2] [Difficulty: 4/5] Add type hints to all ROPE functions and methods.
  - [ ] [Difficulty: 3/5] Audit function and method parameters and return values, including `None`, generators, callbacks, and file/path types.
  - [ ] [Difficulty: 3/5] Add precise annotations using existing domain types where possible; avoid introducing unnecessary dependencies or speculative types.
  - [ ] [Difficulty: 2/5] Run available syntax, import, and type checks, and resolve issues introduced by the annotations.

- [ ] [P2] [Difficulty: 3/5] Add comments and documentation where code intent is not clear.
  - [ ] [Difficulty: 2/5] Identify non-obvious algorithms, assumptions, units, side effects, and format conventions that need explanation.
  - [ ] [Difficulty: 3/5] Add concise comments that explain intent or constraints without restating the code.

- [ ] [P2] [Difficulty: 4/5] Correct spelling in function and variable names across ROPE without introducing unintended behavior or API breakage.
  - [ ] [Difficulty: 3/5] Identify misspelled names and find their callers, serialized uses, and public references before renaming.
  - [ ] [Difficulty: 4/5] Rename approved internal symbols and update all references; preserve or deliberately migrate externally used names with maintainer approval.
  - [ ] [Difficulty: 3/5] Run focused checks and search for remaining references to renamed symbols.

- [ ] [P3] [Difficulty: 4/5] Define and add JSON file-format support.
  - [ ] [Difficulty: 2/5] Confirm what data the JSON format represents, its users, and whether it complements or replaces an existing format.
  - [ ] [Difficulty: 4/5] Agree a versioned schema and compatibility expectations with the maintainer before implementation.
  - [ ] [Difficulty: 4/5] Implement reading and/or writing for the agreed schema, with validation and format documentation.
  - [ ] [Difficulty: 3/5] Add tests for valid files, invalid data, and compatibility/version behavior.

- [ ] [P3] [Difficulty: 5/5] Plan and implement integration of ROPE-Studio with ROPE.
  - [ ] [Difficulty: 3/5] Agree with the maintainer on the desired relationship, user workflow, and which repository owns the integrated application.
  - [ ] [Difficulty: 4/5] Define the Python API and packaging boundary so the GUI uses ROPE functionality directly and ROPE remains usable independently.
  - [ ] [Difficulty: 5/5] Implement the approved integration in small, separately reviewable steps, preserving the existing CLI and GUI workflows.
  - [ ] [Difficulty: 4/5] Verify installation, direct Python integration, and the agreed GUI and CLI workflows.
