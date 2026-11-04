from __future__ import annotations
import numpy as np
from pathlib import Path
from rope.model.StructuralElement import StructuralElement
from rope.definitions.rope_def import FOLDER,structural_markers
from rope.utils.dim3_utils import get_sugar_cords
from rope.model.range_dict import RangeDict


class Module(StructuralElement):
    """PDB-backed module with sequence-checked build coordinates.

    The first PDB residue is the attachment anchor; later residues provide the
    build coordinates. When a sequence is supplied and the source file exists,
    its marker-stripped length must match the parsed build-residue count. A
    missing source file produces length zero. Subclasses that support inversion
    must override :meth:`inverted`.
    """

    def __init__(
        self,
        name: str,
        file: str | Path,
        symbol: str,
        sequence: str | None = None,
        priority: int = 0,
        nonstandard: bool = False,
        ligand: str | None = None,
    ) -> None:
        super().__init__(name, file, symbol)
        self.name = name
        self.file = file
        self.symbol = symbol
        self.sequence = sequence
        self.nonstandard = nonstandard
        self.generate_cords()
        self.ligand = ligand

        if ligand is not None:
            self.ligand_coords,self.ligand_lines = self.get_ligand_coords()
        self.set_len()
        
        self.priority = priority

        self.segments = NotImplemented

        
    def inverted(self) -> Module:
        """Subclass hook; raise ``NotImplementedError`` until inversion is supported."""
        raise NotImplementedError

    def set_len(self) -> None:
        if self.sequence is not None:
            for mark in structural_markers:
                self.sequence = self.sequence.replace(mark, "")
            self.len = len(self.sequence)
        elif self.build_cords is not None:
            self.len = len(self.build_cords)
        else:
            self.len = 1
        if not self.file_found:
            self.len = 0
            return
        if len(self.build_cords) != self.len:
            raise Exception(f"{self.name}: Length of pdb {len(self.build_cords)} is not the same as Length of Module elements {self.len}")
        

    def _generate_cords(
        self,
    ) -> tuple[
        np.ndarray,
        list[np.ndarray],
        list[list[str]],
        np.ndarray,
        list[dict[str, tuple[float, float, float]]],
        bool,
    ]:
        """Read the module PDB into start, residue, and final coordinates.

        The first PDB residue is the attachment point and is not included in
        the build-residue lists. Coordinates from each later residue are
        converted to float32 arrays; atom dictionaries and original lines are
        retained alongside them.

        Returns:
            Start coordinates, per-residue coordinates and source lines,
            final-residue coordinates, atom-coordinate dictionaries, and a
            file-found flag.

        Raises:
            FileNotFoundError: If the module PDB cannot be opened.
            ValueError: If residue identifiers or coordinates are invalid.
        """
        start_res_id = None
        start_res_coord = {}
        other_res_coord = []
        other_res_lines = []
        current_res_id = None
        try:
            with open(self.file, 'r') as f:
                for line in f:
                    if line.startswith('ATOM'):
                        if start_res_id is None:
                            start_res_id = int(line[22:26])
                        elif int(line[22:26]) != start_res_id:
                            if int(line[22:26]) != current_res_id:
                                other_res_coord.append({})
                                other_res_lines.append([])
                                current_res_id = int(line[22:26])
                            other_res_coord[-1][line[12:16].strip()] = (float(line[30:38]), float(line[38:46]), float(line[46:54])) 
                            other_res_lines[-1].append(line)
                        if int(line[22:26]) == start_res_id:
                            start_res_coord[line[12:16].strip()] = (float(line[30:38]), float(line[38:46]), float(line[46:54]))
            sugar_coord = get_sugar_cords(start_res_coord)
            last_coord = get_sugar_cords(other_res_coord[-1])
            other_res_coord_dict = other_res_coord.copy()

            for i in range(len(other_res_coord)):
                other_res_coord[i] = np.array(list(other_res_coord[i].values()), dtype=np.float32)
        except FileNotFoundError:

            print(f"File {self.file} not found. Please check the file path {FOLDER/self.file}.")
            raise
            return None, None, None, None,None,False
        return sugar_coord, other_res_coord, other_res_lines, last_coord,other_res_coord_dict,True


    def get_ligand_coords(
        self,
    ) -> tuple[list[np.ndarray], list[list[str]]]:
        """Read ligand residues matching ``self.ligand`` from the module PDB.

        Returns:
            A pair containing float32 coordinate arrays and original PDB lines
            for each matching ligand residue. No matches produce two empty
            lists.

        Raises:
            FileNotFoundError: If the module PDB cannot be opened.
            ValueError: If a matching residue's identifiers or coordinates
                are invalid.
        """
        other_res_coord = []
        other_res_lines = []
        current_res_id = None
        try:
            with open(FOLDER/self.file, 'r') as f:
                for line in f:
                    if not line.startswith('ATOM') and not line.startswith("HETATM"):
                        continue
                    if line[17:20] == self.ligand:
                        if int(line[22:26]) != current_res_id:
                            other_res_coord.append({})
                            other_res_lines.append([])
                            current_res_id = int(line[22:26])
                        other_res_coord[-1][line[12:16].strip()] = (float(line[30:38]), float(line[38:46]), float(line[46:54])) 
                        other_res_lines[-1].append(line)
            other_res_coord_dict = other_res_coord.copy()

            for i in range(len(other_res_coord)):
                other_res_coord[i] = np.array(list(other_res_coord[i].values()), dtype=np.float32)
            
            return other_res_coord,other_res_lines
        except FileNotFoundError:
            print(f"File {self.file} not found. Please check the file path.")
            raise
        
    def _copy_state(self, variant: Module) -> None:
        self.name = variant.name
        self.file = variant.file
        self.symbol = variant.symbol
        self.sequence = variant.sequence
        if self.ligand is not None:
            self.ligand = variant.ligand
            self.ligand_coords = variant.ligand_coords
            self.ligand_lines = variant.ligand_lines
        self.len = variant.len
        self.start_cord = variant.start_cord
        self.build_cords = variant.build_cords
        self.build_lines = variant.build_lines
        self.last_coord = variant.last_coord
        self.coord_dict = variant.coord_dict

    def __str__(self) -> str:
        return f"Module: {self.name}"

    def __repr__(self) -> str:
        return f"Module: {self.name}"


class segmented_module(Module):
    """Module with separately addressable structural segments and spacers.

    The spacer list must contain exactly one fewer entry than the segment
    sequence, and each segment's sequence length must match its parsed PDB
    residues. :meth:`change_elements` temporarily exposes one segment through
    the standard coordinate attributes until :meth:`reset_elements` is called.
    """

    def __init__(
        self,
        name: str,
        file: str | Path,
        symbol: str,
        sequence: list[str],
        spacer: list[str],
        priority: int,
        ligand: str | None = None,
    ) -> None:
        try:
            assert type(sequence) == list
            assert type(spacer) == list
            assert len(spacer) == len(sequence)-1
        except:
            print(type(sequence),type(spacer),len(spacer),len(sequence)-1)
            raise AssertionError
        spaced_sequences = []
        
        for i in range(len(sequence)):
            spaced_sequences.append(sequence[i])
            if i != len(sequence)-1:
                spaced_sequences.append(spacer[i])
        spaced_sequences = "".join(spaced_sequences)
        super().__init__(name, file, symbol, spaced_sequences,priority=priority,ligand=ligand)
        self.segments = sequence
        self.segments_len = len(sequence)
        self.spacer = spacer
        self.generate_segment_cords()
        assert len(self.build_cords) == len(self.sequence)
        for i in range(len(self.segment_build_cords)):
            for mark in structural_markers:
                self.segments[i] = self.segments[i].replace(mark, "")
            try:
                assert len(self.segment_build_cords[i])==len(self.segments[i])
            except AssertionError:
                print(f"Length of segment sequence {i} of module {self.name} is  {len(self.segments[i])}, but only {len(self.segment_build_cords[i])} residues were found")
                raise

        self.full_start_cord = self.start_cord
        self.full_build_cords = self.build_cords
        self.full_build_lines = self.build_lines
        self.full_last_coord = self.last_coord
        self.full_coord_dict =  self.coord_dict
        self.full_sequence = self.sequence

    def generate_segment_cords(self, invers: bool = False) -> None:
        self.segment_start_cord,self.segment_build_cords,self.segment_build_lines,self.segment_last_coord,self.segment_coord_dict = self._generate_segment_cords(invers)
        return

    def _generate_segment_cords(
        self, invers: bool
    ) -> tuple[
        list[np.ndarray],
        list[list[np.ndarray]],
        list[list[list[str]]],
        list[np.ndarray],
        list[list[dict[str, tuple[float, float, float]]]],
    ]:
        """Parse the PDB into segment-level coordinate groups.

        Residue ranges are derived from segment and spacer lengths. Only ATOM
        records in those ranges are retained; when ``invers`` is true, the
        parsed segment groups are reversed before their coordinates are built.

        Args:
            invers: Whether to reverse the order of the parsed segment groups.

        Returns:
            Per-segment start sugars, residue coordinate arrays, original
            residue lines, final sugars, and atom-coordinate dictionaries.

        Raises:
            FileNotFoundError: If the module PDB cannot be opened.
            ValueError: If a residue identifier or coordinate is invalid.
        """
        segment_sugar_coord = []
        segment_other_res_coord = []
        segment_other_res_lines = []
        segment_last_coord = []
        segment_other_res_coord_dict = []
        start_res_coord = []
        segment_other_res_coord_list = []

        segment_range = RangeDict()
        current = 1
        element = 0
        
        if invers:
            current =1
        
        for seg in self.segments:
            
            segment_range[range(current,current+len(seg)+1)] = element
            if element >= len(self.spacer):
                break
            current += len(seg)
            current += len(self.spacer[element])
            element += 1
        
        
        try:
            segment_coords = [[] for i in range(len(segment_range))]
            line_count = 0
            with open(FOLDER/self.file, 'r') as f:
                for line in f:
                    if not line.startswith('ATOM'):
                        continue
                    if int(line[22:26]) in segment_range:
                        segment_coords[segment_range[int(line[22:26])]].append(line)
        
        except FileNotFoundError:
            print(f"File {self.file} not found. Please check the file path.")
            raise
        seq_index = 0
        if invers:
            segment_coords = segment_coords[::-1]
            
        for seg in segment_coords:
            start_res_id = None
            segment_sugar_coord.append([])
            segment_other_res_coord.append([])
            segment_other_res_lines.append([])
            segment_last_coord.append([])
            segment_other_res_coord_dict.append([])
            segment_other_res_coord_list.append([])
            start_res_coord.append([])
            current_res_id = None
            
            for line in seg:
                if start_res_id is None:
                    start_res_id = int(line[22:26])
                    start_res_coord[seq_index].append({})
                elif int(line[22:26]) != start_res_id:
                    if int(line[22:26]) != current_res_id:
                        segment_other_res_coord[seq_index].append({})
                        segment_other_res_lines[seq_index].append([])
                        current_res_id = int(line[22:26])
                    segment_other_res_coord[seq_index][-1][line[12:16].strip()] = (float(line[30:38]), float(line[38:46]), float(line[46:54]))
                    segment_other_res_lines[seq_index][-1].append(line)
                if int(line[22:26]) == start_res_id and seq_index == 0:
                    start_res_coord[seq_index][-1][line[12:16].strip()] = (float(line[30:38]), float(line[38:46]), float(line[46:54]))
            if seq_index != 0:
                segment_sugar_coord[seq_index] = segment_last_coord[seq_index-1]
                
            if seq_index == 0:
                segment_sugar_coord[seq_index] = get_sugar_cords(start_res_coord[seq_index][-1])
            segment_last_coord[seq_index] = get_sugar_cords(segment_other_res_coord[seq_index][-1])
            segment_other_res_coord_dict[seq_index] = segment_other_res_coord[seq_index]
            for i in range(len(segment_other_res_coord[seq_index])):
                segment_other_res_coord_list[seq_index].append(np.array(list(segment_other_res_coord[seq_index][i].values()), dtype=np.float32))
            seq_index += 1
        return segment_sugar_coord, segment_other_res_coord_list, segment_other_res_lines, segment_last_coord,segment_other_res_coord_dict
    
    def _copy_state_segments_variants(self, variant: segmented_module) -> None:
        self.segments = variant.segments
        self.spacer = variant.spacer
        self.segment_start_cord = variant.segment_start_cord
        self.segment_build_cords = variant.segment_build_cords
        self.segment_build_lines = variant.segment_build_lines
        self.segment_last_coord = variant.segment_last_coord
        self.segment_coord_dict = variant.segment_coord_dict
        self._copy_state(variant)
    

    def change_elements(self, seg_index: int) -> None:
        self.start_cord  = self.segment_start_cord[seg_index]
        self.build_cords = self.segment_build_cords[seg_index]
        self.build_lines = self.segment_build_lines[seg_index]
        self.last_coord  = self.segment_last_coord[seg_index]
        self.coord_dict  = self.segment_coord_dict[seg_index]
        self.sequence =  self.segments[seg_index]


    def reset_elements(self) -> None:
        self.start_cord  = self.full_start_cord 
        self.build_cords = self.full_build_cords
        self.build_lines = self.full_build_lines
        self.last_coord  = self.full_last_coord 
        self.coord_dict  = self.full_coord_dict 
        self.sequence = self.full_sequence
    
    def reset(self) -> None:
        self.reset_elements()


    def inverted(self) -> inv_segmented_module:
        mod = inv_segmented_module("i"+self.name,self.file,"i"+self.symbol,self.segments,self.spacer,self.priority,self.ligand)
        return mod
    

    
class inv_segmented_module(segmented_module):
    """Segmented module whose parsed structural segments are ordered in reverse."""

    def __init__(
        self,
        name: str,
        file: str | Path,
        symbol: str,
        sequence: list[str],
        spacer: list[str],
        priority: int = 0,
        ligand: str | None = None,
    ) -> None:
        super().__init__(name, file, symbol, sequence, spacer, priority, ligand)
        self.generate_segment_cords(True)
        self.segments = sequence[::-1]
        i=0
        try:
            for i in range(len(sequence)):
                assert len(self.segment_build_cords[i]) == len(self.segments[i])
        except AssertionError:
            print(self.name,f"segment = {i}",len(self.build_cords[i]),len(self.segments[i]))
            raise
