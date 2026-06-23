# ROPE

Overview
ROPE provides an end-to-end pipeline for RNA origami design:

Blueprint processing → parsing and transformation
Sequence optimization → generating sequences that fold into target structures
Structural analysis → evaluating folding and constraints
3D model construction → assembling PDB structures from modular components

The project closely follows the ROAD design philosophy while organizing functionality into reusable Python modules and scripts.

Project Structure
Core tools (Python equivalents of ROAD components)


RNAbuild.py
Generates 3D RNA structures (PDB files) from blueprint designs using modular building blocks.


revolvr.py
Sequence optimization engine that mutates candidate RNA sequences toward a target structure.


batch_revolvr.py
Runs multiple optimization jobs to generate diverse candidate sequences.


trace_pattern.py
Converts blueprints into dot-bracket notation and sequence constraints.


trace_analysis.py
Provides analysis and diagnostics for blueprint structures and variants.


flip_trace.py
Generates alternative orientations of a blueprint.


dragon.py
Extended infinatyly running version of batch_revolvr.py



Library Components
RNA_lib/
Contains structural building blocks used for 3D assembly:

modules/ → predefined RNA motifs (e.g. tetraloops, kissing loops, helices)
nucleotides/ → atomic PDB representations of A, U, C, G
pdb_file_cleaner.py → utilities for preparing structural files

utils/
Core internal infrastructure:

Geometry & spatial logic → dim3_utils.py, direction.py
RNA representations → nucleotide.py, def_class.py
Module handling → modules.py, module_mapper.py
Rendering / structure output → render_utils.py
Blueprint parsing & tracing → trace_utils.py
Core definitions → rope_def.py
File handling → file_utils.py


CLI / Entry Points

rope.bat → main entry wrapper
Individual .bat files → Windows-friendly entry points for each module

These scripts mirror the modular workflow and allow step-wise or automated execution.

Key Features

* Full Python implementation of the ROAD workflow
* Modular architecture separating design, analysis, and rendering
* Integrated 3D structure construction using PDB-based motifs
* Reusable utilities for RNA geometry and structure handling
* Batch sequence optimization workflows
* Extensible motif and module system (RNA_lib)


Relationship to ROAD
ROPE builds directly on the concepts introduced in ROAD:

Maintains the blueprint-based RNA origami design paradigm
Reimplements core tools (RNAbuild, Revolvr, trace utilities) in Python
Preserves compatibility with existing design workflows

At the same time, ROPE:

Consolidates functionality into a single Python ecosystem
Exposes internal logic as reusable modules (not just scripts)
Simplifies extension, experimentation, and integration

ROPE is intended as a natural evolution and research-friendly implementation of the ROAD methodology.
