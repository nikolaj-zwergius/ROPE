import numpy as np

FOLDER = "RNA_lib/modules/"
NT_FOLDER = "RNA_lib/nucleotides/"
SUGAR_ATOMS = ['C3\'', 'C4\'', 'C5\'', 'O4\'',"P"]


class Module():
    def __init__(self,name = 'Module', file = 'Module.pdb', symbol = 'M',sequence:str = None,priority=0,len = None):
        self.name = name
        self.file = file
        self.start_cord = None
        self.build_cords = None
        self.build_lines = None
        self.last_coord = None
        self.coord_dic = None
        self.symbol = symbol
        self.sequence = sequence
        self.have_seq = False
        self.generate_cords()
        if len is None:
            self.set_len()
        else:
            self.len = len
        self.priority = priority
        
    def set_len(self):
        if self.sequence is not None:
            self.have_seq = True
            self.len = len(self.sequence)
        elif self.build_cords is not None:
            self.len = len(self.build_cords)
        else:
            self.len = 1
    
    def generate_cords(self):
        self.start_cord,self.build_cords,self.build_lines,self.last_coord,self.coord_dict = self._generate_cords()

    def _generate_cords(self):
        start_res_id = None
        start_res_coord = {}
        other_res_coord = []
        other_res_lines = []
        current_res_id = None
        try:
            with open(FOLDER + self.file, 'r') as f:
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
            print(f"File {self.file} not found. Please check the file path.")
            return None, None, None, None,None
        return sugar_coord, other_res_coord, other_res_lines, last_coord,other_res_coord_dict
    
    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        elif self.priority == other.priority:
            return self.len < other.len
        else:
            return False
    def __gt__(self, other):
        if self.priority > other.priority:
            return True
        elif self.priority == other.priority:
            return self.len > other.len
        else:
            return False
    def __eq__(self, other):
        return self.priority == other.priority and self.len == other.len
    def __str__(self):
        return f"Module: {self.name}"
    def __repr__(self): 
        return f"Module: {self.name}"
class nucleotide(Module):
    def __init__(self,name = 'Nucleotide', file = 'Nucleotide.pdb', symbol = 'N'):
        super().__init__(name, file, symbol)

    def _generate_cords(self):
        start_res_id = None
        start_res_coord = {}
        other_res_coord = []
        other_res_lines = []
        current_res_id = None
        try:
            with open(NT_FOLDER + self.file, 'r') as f:
                for line in f:
                    if line.startswith('ATOM'):
                        if start_res_id is None:
                            start_res_id = int(line[22:26])
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
            other_res_coord_dict = other_res_coord
            for i in range(len(other_res_coord)):
                other_res_coord[i] = np.array(list(other_res_coord[i].values()), dtype=np.float32)
            
        except FileNotFoundError:
            print(f"File {self.file} not found. Please check the file path.")
            return None, None, None,None,None
        return sugar_coord, other_res_coord, other_res_lines, last_coord,other_res_coord_dict
class segmented_module(Module):
    def __init__(self, name='Module', file='Module.pdb', symbol='M', sequence = None,spacer = [""],priority=0):
        try:
            assert type(sequence) == list
            assert type(spacer) == list
            assert len(spacer) == len(sequence)-1
        except:
            print(type(sequence),type(spacer),len(spacer),len(sequence)-1)
            raise AssertionError
        spaced_sequnces = []
        self.segments = sequence
        self.segments_len = len(sequence)
        for i in range(len(sequence)):
            spaced_sequnces.append(sequence[i])
            if i != len(sequence)-1:
                spaced_sequnces.append(spacer[i])
        spaced_sequnces = "".join(spaced_sequnces)
        super().__init__(name, file, symbol, spaced_sequnces,priority=priority)
        self.spacer = spacer
        

def get_sugar_cords(coords):
    sugar_coord = {}
    sugar_corrd_list=[]
    for atom in coords.keys():
        if atom in SUGAR_ATOMS:
            sugar_coord[atom] = coords[atom]
    sc_sorted = sorted(sugar_coord.keys())
    for i in range(len(sc_sorted)):
        sugar_corrd_list.append(sugar_coord[sc_sorted[i]])
    sugar_coord = np.array(sugar_corrd_list, dtype=np.float32)
    return sugar_coord


class RangeDict(dict):

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"Key {key} overlaps with existing key(s) in RangeDict.")
        if not isinstance(key, range):
            super().__setitem__(range(key,key+1), value)
        else:
            super().__setitem__(key, value)

    def __contains__(self, item):
        if not isinstance(item, range): # or xrange in Python 2
            for key in self:
                if item in key:
                    return True
            return False
        else:
            return super().__contains__(item)

    def __getitem__(self, item):
        if not isinstance(item, range): # or xrange in Python 2
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)
    def override(self, key, value):
        if key not in self:
            self.__setitem__(key, value)
        if not isinstance(key, range):
            super().__setitem__(range(key,key+1), value)
        else:
            super().__setitem__(key, value)