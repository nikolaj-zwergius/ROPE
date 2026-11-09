# ROPE TODO

Tasks are ordered by priority. Related steps are nested only when they belong
to one larger task.

- [ ] [High] Validate that the sequence and ligands fit within the PDB length.
- [ ] [High] Validate that every listed ligand is present in the PDB.
- [ ] [High] Support ions as either ligands to copy over or as their own class.
- [ ] [High] Add a 120-degree kissing-loop module to the RNA library.
- [ ] [High] Support AKL and 120-degree kissing loops in Revolvr and Multimer `@` labels.
  - [ ] Add the kissing-loop lists needed for both loop types.
  - [ ] Update Revolvr and Multimer to recognize and use those lists.
  - [ ] Check both tools with representative blueprints.

- [ ] [Medium] Add funtionally to generate multiple variants from one blueprint.
  - [] define how the syntax in the blueprint should work
- [ ] [Medium] Support modified nucleic acids in the ViennaRNA folding workflow, while preserving standard RNA behavior.
- [ ] [Medium] Build every state defined for a module.
  - [ ] Define how a states are desribed in the module.toml (look at how ligands are used)


- [ ] [Low] Add a JSON file format. Agree on what data it represents and its format before implementation.
  - [ ] Define and detail the file format.
- [ ] [Low] Integrate ROPE-Studio with ROPE while keeping ROPE usable on its own.




# Completed

- [x] [Medium] Type-hint all functions and methods; document non-obvious behavior, side effects, assumptions, and errors, and state class contracts and subclass requirements where needed. Keep docstrings concise and omit them when names, signatures, and straightforward code already explain the behavior.
- [x] [Medium] Review function and variable names for spelling errors. For each file, check callers and public uses before renaming; preserve compatibility or confirm breaking changes with the maintainer.


# unformated
