#!/usr/bin/env python3
"""
Test script to demonstrate the segment REMARK functionality.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from utils.modules import Broccoli
from RNA_lib.pdb_file_cleaner import add_segment_remarks_to_pdb


def main():
    print("=" * 80)
    print("Testing Segment REMARK Addition for Broccoli Module")
    print("=" * 80)
    print()
    
    print(f"Module: {Broccoli.name}")
    print(f"Symbol: {Broccoli.symbol}")
    print(f"File: {Broccoli.file}")
    print(f"Segments: {Broccoli.segments}")
    print(f"Spacers: {Broccoli.spacer}")
    print(f"Full Sequence: {Broccoli.sequence}")
    print()
    
    print("Segment Mapping:")
    print("-" * 80)
    
    residue_num = 1
    for seg_idx, segment in enumerate(Broccoli.segments):
        print(f"  Residues {residue_num}-{residue_num + len(segment) - 1}: "
              f"Segment {seg_idx + 1} ({len(segment)} nt) - {segment}")
        residue_num += len(segment)
        
        if seg_idx < len(Broccoli.spacer):
            spacer = Broccoli.spacer[seg_idx]
            print(f"  Residues {residue_num}-{residue_num + len(spacer) - 1}: "
                  f"Spacer ({len(spacer)} nt) - {spacer}")
            residue_num += len(spacer)
    
    print()
    print("Output REMARK Format:")
    print("-" * 80)
    print("  Segment 1: REMARK 51")
    print("  Spacer:    REMARK 49")
    print("  Segment 2: REMARK 52")
    print()
    
    # Generate the output
    input_file = "RNA_lib/modules/Brocolli.pdb"
    output_file = "Broccoli_with_remarks.pdb"
    
    print(f"Processing: {input_file}")
    print(f"Output: {output_file}")
    print()
    
    add_segment_remarks_to_pdb(
        file_path=input_file,
        segments=Broccoli.segments,
        spacers=Broccoli.spacer,
        output_path=output_file
    )
    
    # Display the first 50 lines
    print("Generated PDB (first 50 lines):")
    print("-" * 80)
    with open(output_file, 'r') as f:
        lines = f.readlines()[:50]
        for i, line in enumerate(lines, 1):
            print(f"{i:3d}: {line.rstrip()}")
    
    print()
    print(f"Total lines in output: {len(lines)}")
    print()
    print("✓ Test completed successfully!")


if __name__ == "__main__":
    main()
