from __future__ import annotations
import numpy as np
import os
from pathlib import Path
from rope.model.StructuralElement import StructuralElement
from rope.definitions.rope_def import FOLDER,SUGAR_ATOMS
from rope.utils.get_sugar import get_sugar_cords
from rope.utils.range_dict import RangeDict


class Module(StructuralElement):
    def __init__(self, name:str, file:str|Path, symbol:str, sequence:str|None = None, priority:int = 0, len:int|None=None, ligand:str|None = None,test:bool =False,ligand_variants_files:dict[str,str]|None = None,main=True):
        super().__init__(name, file, symbol)
        self.name = name
        self.file = file
        self.symbol = symbol
        self.sequence = sequence
        self.have_seq = False
        self.generate_cords()
        self.ligand = ligand
        self.ligand_variants = ligand_variants_files
        self.variants = {}
        self.default_varian= None
        if main:
            self.default_variant = Module(name, file, symbol, sequence, priority, len, ligand,test=test,main=False)
        if ligand_variants_files is not None and main:
            for i in ligand_variants_files.keys():
                self.variants[i] = Module(name, ligand_variants_files[i], symbol, sequence, priority, len, ligand=i,test=test,main=False)
        if ligand is not None:
            self.ligand_coords,self.ligand_lines = self.get_ligand_coords()
        if len is None:
            self.set_len()
        else:
            self.len = len
        self.priority = priority

        self.segments = NotImplemented
    def inverted(self):
        raise NotImplementedError

    def set_len(self):
        if self.sequence is not None:
            self.have_seq = True
            self.len = len(self.sequence)
        elif self.build_cords is not None:
            self.len = len(self.build_cords)
        else:
            self.len = 1
        if not self.flie_found:
            self.len = 0
            return
        if len(self.build_cords) != self.len:
            raise Exception(f"{self.name}: Length of pdb {len(self.build_cords)} is not the same as Length of Module elements {self.len}")
        

    def _generate_cords(self):
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


    def get_ligand_coords(self):
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
    def __lt__(self, other:Module) -> bool:
        if self.priority < other.priority:
            return True
        elif self.priority == other.priority:
            return self.len < other.len
        else:
            return False
    def __gt__(self, other:Module) -> bool:
        if self.priority > other.priority:
            return True
        elif self.priority == other.priority:
            return self.len > other.len
        else:
            return False
        
    def _copy_state(self,variant:Module):
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

    def set_variant(self, variant_str: str):
        variant = self.variants[variant_str]
        self._copy_state(variant)

    def reset_variant(self):
        self._copy_state(self.default_variant)

    def reset(self):
        self.reset_variant()

    def __eq__(self, other) -> bool:
        if type(other) != Module:
            raise TypeError
        return self.priority == other.priority and self.len == other.len
    def __str__(self):
        return f"Module: {self.name}"
    def __repr__(self): 
        return f"Module: {self.name}"


class segmented_module(Module):
    def __init__(self, name, file:str|Path, symbol:str, sequence:list[str] ,spacer:list[str],priority:int,ligand:str|None=None,main=True,ligand_variants_files:dict[str,str]|None = None,test:bool=False):
        try:
            assert type(sequence) == list
            assert type(spacer) == list
            assert len(spacer) == len(sequence)-1
        except:
            print(type(sequence),type(spacer),len(spacer),len(sequence)-1)
            raise AssertionError
        spaced_sequnces = []
        
        for i in range(len(sequence)):
            spaced_sequnces.append(sequence[i])
            if i != len(sequence)-1:
                spaced_sequnces.append(spacer[i])
        spaced_sequnces = "".join(spaced_sequnces)
        super().__init__(name, file, symbol, spaced_sequnces,priority=priority,ligand=ligand)
        self.segments = sequence
        self.segments_len = len(sequence)
        self.spacer = spacer
        self.generate_segment_cords()
        assert len(self.build_cords) == len(self.sequence)
        for i in range(len(self.segment_build_cords)):
            try:
                assert len(self.segment_build_cords[i])==len(self.segments[i])
            except AssertionError:
                print(f"Length of segment seqcencs {i} of module {self.name} is  {len(self.segments[i])}, but only {len(self.segment_build_cords[i])} residues were found")
                raise

        self.full_start_cord = self.start_cord
        self.full_build_cords = self.build_cords
        self.full_build_lines = self.build_lines
        self.full_last_coord = self.last_coord
        self.full_coord_dict =  self.coord_dict
        self.full_sequence = self.sequence

        if main:
            self.default_variant = segmented_module(name,file,symbol,sequence,spacer,priority,ligand,main=False)
        if ligand_variants_files is not None and main:
            for i in ligand_variants_files.keys():
                self.variants[i] = segmented_module(name, ligand_variants_files[i], symbol, sequence, spacer, priority, ligand=i,main=False)

    def generate_segment_cords(self,invsers = False) -> None:
        self.segment_start_cord,self.segment_build_cords,self.segment_build_lines,self.segment_last_coord,self.segment_coord_dict = self._generate_segment_cords(invsers)
        return
    def _generate_segment_cords(self,invsers:bool)-> tuple[list[np.ndarray],list[list],list[list],list[dict],list[dict]]: 
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
        
        if invsers:
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
        if invsers:
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
    
    def _copy_state_segments_variants(self,variant:segmented_module):
        self.segments = variant.segments
        self.spacer = variant.spacer
        self.segment_start_cord = variant.segment_start_cord
        self.segment_build_cords = variant.segment_build_cords
        self.segment_build_lines = variant.segment_build_lines
        self.segment_last_coord = variant.segment_last_coord
        self.segment_coord_dict = variant.segment_coord_dict
        self._copy_state(variant)
    
    def set_variant(self, variant_str: str):
        variant = self.variants[variant_str]
        if type(variant) is segmented_module:
            self._copy_state_segments_variants(variant)
        return super().set_variant(variant_str)

    def reset_variant(self):
        self._copy_state_segments_variants(self.default_variant)
        super().reset_variant()

    def change_elements(self,seg_index:int):
        """
        Changes which elemets that the segmented module shows, from the full to a segment

        Warning: This function should always be followed by the use of the reset_elements funtion of segmented_module,
        when processsing of the current segment is done to ensure that the module can still use the full length in between.
        
        There is no check or enforcment of this
        """
        self.start_cord  = self.segment_start_cord[seg_index]
        self.build_cords = self.segment_build_cords[seg_index]
        self.build_lines = self.segment_build_lines[seg_index]
        self.last_coord  = self.segment_last_coord[seg_index]
        self.coord_dict  = self.segment_coord_dict[seg_index]
        self.sequence =  self.segments[seg_index]


    def reset_elements(self):
        self.start_cord  = self.full_start_cord 
        self.build_cords = self.full_build_cords
        self.build_lines = self.full_build_lines
        self.last_coord  = self.full_last_coord 
        self.coord_dict  = self.full_coord_dict 
        self.sequence = self.full_sequence
    
    def reset(self):
        self.reset_elements()
        self.reset_variant()
        super().reset()


    def inverted(self) -> inv_segmented_module:
        mod = inv_segmented_module("i"+self.name,self.file,"i"+self.symbol,self.segments,self.spacer,self.priority,self.ligand)
        return mod
    

    
class inv_segmented_module(segmented_module):
    def __init__(self, name, file, symbol, sequence, spacer, priority=0, ligand = None):
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
