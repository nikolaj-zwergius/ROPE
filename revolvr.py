import os
import utils.rope_def as rd
import trace_pattern as tp
import utils.trace_utils as tu
import getopt,sys
import RNA
import random
from types import FunctionType

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))

#random.seed(85639)
#random.seed(9)
def compute_ED(seq:str) -> tuple[float,float,float]:
    # create fold_compound data structure (required for all subsequently applied  algorithms)
    fc = RNA.fold_compound(seq)

    # compute MFE and MFE structure
    (mfe_struct, mfe) = fc.mfe()

    # rescale Boltzmann factors for partition function computation
    fc.exp_params_rescale(mfe)

    # compute partition function
    (pp, pf) = fc.pf()

    # compute centroid structure
    (centroid_struct, dist) = fc.centroid()

    # compute free energy of centroid structure
    centroid_en = fc.eval_structure(centroid_struct)

    # compute MEA structure
    (MEA_struct, MEA) = fc.MEA()

    # compute free energy of MEA structure
    MEA_en = fc.eval_structure(MEA_struct)

    # #print everything like RNAfold -p --MEA
    return mfe, fc.pr_structure(mfe_struct), fc.mean_bp_distance()



def initlize_structure(file:str)->tuple[str,str,str,str]:
    with open(file, "r") as f:
        name = f.readline().rstrip().lstrip(">")
        pattern= tu.generate_np_pattern(file)
    init_seq,init_struc,_,_ = tp.trace_backbone(pattern)
    
    stack = []
    stack1 = []
    seq = ""
    for i in range(len(init_seq)):
        if init_struc[i] in ["("]:
            new_base=rd.mutate(rd.mutation_rate[init_seq[i]])
            seq += new_base
            if init_seq[i] == "K":
                stack.append(rd.k_table[new_base])
            else:
                stack.append(rd.base_pairs_table[new_base])
        elif init_struc[i] in [")"]:
            test_base = stack.pop(-1)
            if test_base in rd.one_letter_code[init_seq[i]]:
                seq += test_base
            else:
                new_base=rd.mutate(rd.mutation_rate[init_seq[i]])
                seq += new_base
        elif init_struc[i] in ["["]:
            new_base=rd.mutate(rd.mutation_rate[init_seq[i]])
            seq += new_base
            if init_seq[i] == "K":
                stack1.append(rd.k_table[new_base])
            else:
                stack1.append(rd.base_pairs_table[new_base])
        elif init_struc[i] in ["]"]:
            test_base = stack1.pop(-1)
            if test_base in rd.one_letter_code[init_seq[i]]:
                seq += test_base
            else:
                new_base=rd.mutate(rd.mutation_rate[init_seq[i]])
                seq += new_base
        elif init_struc[i] in ["{"]:
            if init_seq[i] == "N":
                new_base=rd.mutate((0,50,50,0))
            else:
                new_base=rd.mutate(rd.mutation_rate[init_seq[i]])
            seq += new_base
            if init_seq[i] == "K":
                stack1.append(rd.k_table[new_base])
            else:
                stack1.append(rd.base_pairs_table[new_base])
        elif init_struc[i] in ["}"]:
            test_base = stack1.pop(-1)
            if test_base in rd.one_letter_code[init_seq[i]]:
                seq += test_base
            else:
                new_base=rd.mutate(rd.mutation_rate[init_seq[i]])
                seq += new_base
        else:
            new_base=rd.mutate(rd.mutation_rate[init_seq[i]])
            seq += new_base
    clean_struc=init_struc.replace("[",".").replace("{",".").replace("}",".").replace("]",".")
    return name,init_seq,init_struc,seq,clean_struc

def mutator(clean_struc:str,struc:str,seq:str,init_seq:str,N:int,mutate_weitg:tuple[int,int,int,int],mask_gen:FunctionType ,rad_level:int=None) -> str:
    new_seq = [None]*len(clean_struc)
    predic_fold=struc
    mutate_mask = mask_gen(clean_struc,struc,seq,rad_level)
    di1 =  RNA.hamming_distance(clean_struc,predic_fold)
    for i in range(N):
        for i in range(len(mutate_mask)):
            if init_seq[i] in rd.VALID_BASES:
                new_seq[i] = init_seq[i]
                continue
            if mutate_mask[i] == "X" and i in bp_map.keys():
                if init_seq[i] == "N":
                    new_base=rd.mutate(mutate_weitg)
                    new_seq[i]=new_base
                else:
                    new_seq[i]=seq[i]
                if init_seq[i] == "K" or init_seq[bp_map[i]]=="K":
                    new_seq[bp_map[i]] = random.choice(rd.k_table[new_seq[i]])
                else:
                    new_seq[bp_map[i]] = random.choice(rd.base_pairs_table[new_seq[i]])
            elif mutate_mask[i] == "X" and clean_struc[i] == ".":
                new_base=rd.mutate(mutate_weitg)
                new_seq[i]=new_base
            else:
                new_seq[i]=seq[i]
        new_seq = "".join(new_seq)
        if new_seq in tested_seq.keys():
            predic_fold2 = tested_seq[new_seq]
        else:
            predic_fold2 =  RNA.fold(new_seq)[0]
            tested_seq[new_seq] =  predic_fold2
        di2 =  RNA.hamming_distance(clean_struc,predic_fold2)
        
        if di2 <= di1:
            if rad_level != None and di2 < di1:
                rad_level -= 1
            elif rad_level != None:
                rad_level += 1
            di1 = di2
            predic_fold = predic_fold2
            seq = new_seq
            mutate_mask = dir_mutate_mask_gen(clean_struc,predic_fold,seq)
           
        elif rad_level != None:
            rad_level += 1
        new_seq = [None]*len(clean_struc)
        stack = []
        if rad_level != None and rad_level<1:
            rad_level = 1
        elif rad_level != None and rad_level >20:
            rad_level = 20
        ##print("rad:",rad_level)
    if rad_level != None:
        return predic_fold,seq,rad_level
    return predic_fold,seq

def dir_mutate_mask_gen(clean_struc:str,struc:str,seq:str,rad_level:int = None) -> str:
    mutate_mask = []
    predic_fold = struc
    ##print(len(seq),len(clean_struc),len(RNA.fold(seq)[0]))
    for i in range(len(clean_struc)):
        if clean_struc[i] == predic_fold[i]:
            mutate_mask.append("-")
        else:
            mutate_mask.append("X")
    if rad_level == None:
        return "".join(mutate_mask)
    ids = []
    for i in range(len(mutate_mask)):
        if mutate_mask[i] == "X":
            ids.append(i)
    while len(ids) > rad_level:
        pick = random.choice(ids)
        mutate_mask[pick] = "-"
        ids.remove(pick)
    return "".join(mutate_mask)

def neu_mutate_mask_gen(clean_struc:str,struc:str,seq:str,rad_level:int) -> str:
    mutate_mask = []
    for i in range(len(clean_struc)-rad_level):
        mutate_mask.append("-")
    for i in range(rad_level):
        mutate_mask.append("X")
    random.shuffle(mutate_mask)
    return "".join(mutate_mask)

def base_pair_mapper(clean_struc:str) -> dict:
    stack1 = []
    base_pair_map ={}
    for i in range(len(clean_struc)):
        if clean_struc[i] == "(":
            stack1.append(i)
        if clean_struc[i] == ")":
            mate = stack1.pop(-1)
            base_pair_map[mate] = i
            base_pair_map[i] = mate
    return base_pair_map

def penalty_score(seq:str,struc:str) -> tuple[list,int]:
    
    new_seq,complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites = tu.count_repeats(seq,bpmap=bp_map)
    PS = complement_zones+duplicate_zones+pattern_repeats+poly_repeats+restriction_sites
    ##print(new_seq)
    return new_seq, PS

def gc_ratio_calculator(seq:str) -> int:
    GC = 0
    AU = 0
    GC_ration = 0
    for i in seq:
        if i in ["G","C"]:
            GC += 1
        else:
            AU += 1
    GC_ration = GC/(AU+GC)*100
    return GC_ration

def mutation_matix_ps(clean_struc:str,seq:str,rad_level:int,init_seq:str) -> tuple[list,int]:
    ps_matix, ps = penalty_score(seq,clean_struc)

    n_switch = False
    n_id = 0
    mutate_matix = ["-"]*len(seq)
    GC_ration = gc_ratio_calculator(seq)
    ##print(GC_ration)

    for i in range(len(seq)):
        if init_seq[i] in rd.VALID_BASES:
            continue
        if ps_matix[i] in ["S","W","X","D"]:
            mutate_matix[i] = rd.mutate(rd.mutation_rate[init_seq[i]])
            if i in bp_map:
                if init_seq[bp_map[i]] == "N":
                    pass
                elif init_seq[bp_map[i]] == "K" or init_seq[i] == "K":
                    pass
                elif mutate_matix[i] not in rd.base_pairs_table[init_seq[bp_map[i]]]:
                            mutate_matix[i] = "-"
        elif ps_matix[i] in ["G","U","C","A"]:
            match ps_matix[i]:
                case "G":
                    mutate_matix[i] = random.choice([rd.mutate(rd.change_base["G"]),"-"])
                case "U":
                    mutate_matix[i] = random.choice([rd.mutate(rd.change_base["U"]),"-"])
                case "C":
                    mutate_matix[i] = random.choice([rd.mutate(rd.change_base["C"]),"-"])
                case "A":
                    mutate_matix[i] = random.choice([rd.mutate(rd.change_base["A"]),"-"])
            try:
                #print(mutate_matix[i],rd.base_pairs_table[bp_map[i]])
                if mutate_matix[i] not in rd.base_pairs_table[bp_map[i]]:
                            mutate_matix[i] = "-"
            except:
                pass
        elif ps_matix[i] == "P":
            mutate_matix[i] = random.choices(["K","-"],(1,14),k=1)[0]
            if mutate_matix[i] == "-":
                mutate_matix[i] = random.choices(["M","-"],(1,4),k=1)[0]
            if mutate_matix[i] == "M":
                mutate_matix[i] = rd.mutate((25,25,25,25))
            if mutate_matix[i] == "K":
                if i in bp_map:
                    if init_seq[i] in rd.VALID_BASES or init_seq[bp_map[i]] in rd.VALID_BASES:
                        mutate_matix[i] = "-"
        if seq[i] in ["G","U"] and i in bp_map.keys() and mutate_matix[i] in "-":
            if i in bp_map:
                if init_seq[i] in rd.VALID_BASES or init_seq[bp_map[i]] in rd.VALID_BASES:
                    mutate_matix[i] = "-"
            elif seq[bp_map[i]] in ["G","U"]:
                mutate_matix[i] = random.choices(["K","A"],(9,1),k=1)[0]
                if mutate_matix[i] == "K":
                    mutate_matix[bp_map[i]] = "K"
                else:
                    mutate_matix[bp_map[i]] = "U"
            elif seq[bp_map[i]] == "A":
                mutate_matix[bp_map[i]] = random.choices(["-","B"],(99,1),k=1)[0]
            elif seq[bp_map[i]] == "C":
                mutate_matix[bp_map[i]] = random.choices(["-","D"],(99,1),k=1)[0]

        if GC_ration > 55 and seq[i] in ["G","C"] and mutate_matix[i] == "i":
            mutate_matix[i] = random.choices(["-","A","U"],(100-abs(GC_ration-55),abs(55-GC_ration)/2,abs(55-GC_ration)/2))[0]
        elif GC_ration < 55 and seq[i] in ["A","U"] and mutate_matix[i] == "i":
            mutate_matix[i] = random.choices(["-","G","C"],(100-abs(GC_ration-55),abs(55-GC_ration)/2,abs(55-GC_ration)/2))[0]
        ##print(GC_ration,"GC_HIGH",100-abs(GC_ration-55),abs(55-GC_ration)/2,abs(55-GC_ration)/2,"GC_LOW",100-(55-GC_ration),(55-GC_ration)//2,(55-GC_ration)//2)
    ids = []
    #print(mutate_matix)
    for i in range(len(seq)):
        if mutate_matix[i] == "-":
            continue
        if mutate_matix[i] == seq[i]:
            mutate_matix[i] = "-"


    for i in range(len(seq)):
        if mutate_matix[i] != "-":
            ids.append(i)
    while len(ids) > FAV_RAD_LEVEL:
        pick = random.choice(ids)
        ids.remove(pick)
        mutate_matix[pick] = "-"
    return mutate_matix,ps

def mutator2(clean_struc:str,struc:str,seq:str,init_seq:str,mask:list,ps:int) -> str:
    seq_list = list(seq)
    ps1 = ps
    predic_fold = struc
    di1 = RNA.hamming_distance(clean_struc,predic_fold)
    for i in range(len(mask)):
        if mask[i] == "K" and i in bp_map.keys():
            seq_list[i],seq_list[bp_map[i]] = seq_list[bp_map[i]],seq_list[i]
        elif mask[i] == "B":
            seq_list[i] = "G"
        elif mask[i] == "D":
            seq_list[i] = "U"
        elif mask[i] != "-":
            seq_list[i] = mask[i]
            if i in bp_map.keys():
                if rd.base_pairs_table[mask[i]] in rd.one_letter_code[init_seq[i]]:
                    seq_list[bp_map[i]] = rd.base_pairs_table[mask[i]]
    seq_string = "".join(seq_list)
    _,ps2 = penalty_score(seq_string,clean_struc)
    if seq_string in tested_seq.keys():
        new_struc = tested_seq[seq_string]
    else:
        new_struc = RNA.fold(seq_string)[0]
        tested_seq[seq_string] = new_struc
    di2 = RNA.hamming_distance(clean_struc,new_struc)
    ##print(seq_string, gc_ratio_calculator(seq_string), "".join(mask))
    new_GC = gc_ratio_calculator(seq_string)
    old_GC = gc_ratio_calculator(seq)
    if ps1==0 and ps2 == 0:
        if di2 == di1:
            if abs(55-new_GC) < abs(55-old_GC):
                return new_struc,seq_string
    elif ps2 <= ps1:
        if di2 == di1:
            #if abs(55-new_GC) < abs(55-old_GC):
            return new_struc,seq_string
    #print(seq)
    return struc,seq

def problem_in_loced(problem_mask:list,init_seq:str,control=True)->bool:
    locked_problem = False
    problems = 0
    locked_problems = 0
    for i in range(len(init_seq)):
        if problem_mask[i] != "-" and init_seq[i] != "N":
            locked_problems += 1
        if problem_mask[i] != "-":
            problems += 1
    #print(problem_mask)
    #print(init_seq)
    #print(locked_problems,problems)
    if problems == 0 and not control:
        return False
    if locked_problems == problems:
        locked_problem = True
    return locked_problem

def full_revolver(clean_struc:str,seq:str,init_seq:str,init_struc:str) -> tuple[str,str,float,float,float]:    
    rad_level = FAV_RAD_LEVEL
    struc = RNA.fold(seq)[0]
    #print("setup done")
    struc,seq = mutator(clean_struc,struc,seq,init_seq,5,(0,50,50,0),dir_mutate_mask_gen)
    
    
    #print("mutator 1 done") 

    num=0
    mask = dir_mutate_mask_gen(clean_struc,struc,seq)
    same = 0
    runs = 0
    locked_probelms = False
    while RNA.hamming_distance(clean_struc,struc) != 0 and not locked_probelms:
        off = 0
        for i in range(len(mask)):
            if init_seq[i] in ["C","A","U","G"] and mask[i] == "X":
                off += 1
        if off != mask.count("X"):
            struc,seq,rad_level=mutator(clean_struc,struc,seq,init_seq,2,(15,35,35,15),dir_mutate_mask_gen,rad_level)
        struc,seq,rad_level=mutator(clean_struc,struc,seq,init_seq,1,(15,35,35,15),neu_mutate_mask_gen,rad_level)
        mask = dir_mutate_mask_gen(clean_struc,struc,seq)
        runs+=1
        problem_in_loced(mask,init_seq)
        if problem_in_loced(mask,init_seq) and runs>=100:
            locked_probelms = True
        #print(seq)
        #print(init_seq)
        #print(mask)
        #print(RNA.hamming_distance(clean_struc,struc))
    


    #print("mutator 2 done")
    #print(seq)
    #print(init_seq)
    return mini_revolvr(clean_struc,seq,init_seq,init_struc,struc)


def mini_revolvr(clean_struc:str,seq:str,init_seq:str,init_struc:str,struc:str)->tuple[str,str,float,float,float]:
    rad_level = FAV_RAD_LEVEL
    mask = []
    runs = 0
    same = 0
    
    while set(mask) != {"-"}  or gc_ratio_calculator(seq)>55.1 or ps>0:
        
        mask,ps = mutation_matix_ps(clean_struc,seq,FAV_RAD_LEVEL,init_seq)
        #print(ps)
        pre_seq = seq
        struc,seq = mutator2(clean_struc,struc,seq,init_seq,mask,ps)
        test_mask,test_ps =penalty_score(seq,clean_struc)
        #print(test_mask)
        #print(gc_ratio_calculator(seq),set(mask),test_ps)
        runs += 1
        if pre_seq in tested_seq:
            same += 1
        if runs%100 == 0:
            #print("mutator2:\n")
            #print(runs,same,ps,gc_ratio_calculator(seq))
            #print(seq)
            #print(problem_in_loced(test_mask,init_seq))
            pass
        if runs == same and ps == 0 and set(mask) == {"-"} and runs > 5000 and problem_in_loced(test_mask,init_seq) :
            break
    stack = []
    kl_id = []
    kl_found = False
    kl_start = float("inf")
    for i in range(len(init_struc)):
        if init_struc[i] == "[" and kl_found == False:
            kl_start = i
            stack.append((i,i+6))
            kl_found = True
        elif i == kl_start+6:
            kl_found = False
        elif init_struc[i] == "]" and kl_found == False:
            kl_start = i
            kl_id.append((stack.pop(-1),(i,i+6)))
            kl_found = True
        elif i == kl_start+6:
            kl_found = False

    string_list = list(seq)
    ps = 1
    di = 1
    x = 0
    while ps > 0 and di > 0 and len(kl_id)>0:
        #print("starting KL round:",x)
        kl_rejected = True
        while kl_rejected:
            kl_rejected = False
            kl_used = []
            for i in kl_id:
                kl = random.choice(kls)

                string_list[i[0][0]:i[0][1]] = kl[1][1:-1]
                string_list[i[1][0]:i[1][1]] = kl[2][1:-1]
                kl_used.append(kl[1])
                kl_used.append(kl[2])
            if len(set(kl_used)) == len(kl_id):
                kl_rejected = True

            for i in range(len(kl_used)):
                for j in range(len(kl_used[i:])):
                    energy = RNA.duplexfold(kl_used[i],kl_used[j]).energy
                    if energy > KL_OFF and j == i+1:
                        kl_rejected = True
        seq = "".join(string_list)
        dump,ps = penalty_score(seq,clean_struc)
        if ps == 0:
            di = RNA.hamming_distance(clean_struc,RNA.fold(seq)[0])
            #print("di = ",di,"PS = ",0)
        else:
            #print("ps != 0",dump)
            pass
        x += 1
        if x > 4068:
            raise Exception
       #print("Done KL round:",x)
    mfe,feq,ed =compute_ED(seq)
    return seq,struc,mfe, feq, ed


def revolver(file:str):
    global bp_map
    global tested_seq
    global FAV_RAD_LEVEL
    global KL_OFF
    name,init_seq,init_struc,seq,clean_struc= initlize_structure(file)

    FAV_RAD_LEVEL = 15
    bp_map = base_pair_mapper(clean_struc) 
    KL_MIN = -7.2
    KL_MAX = -10.8
    KL_OFF = -6.0
    
    global tested_seq
    tested_seq = {}
    global kls
    kls = []
    if set(init_seq) == set(rd.VALID_BASES):
        mfe,feq,ed =compute_ED(seq)
        problem=dir_mutate_mask_gen(clean_struc,clean_struc,seq)
        return seq, clean_struc,mfe,feq,ed,problem,init_seq
    
    with open(f"{dir_path}/utils/kl_list","r") as f:
        for line in f:
            line_list = line.split(",")
            line_list[0] = float(line_list[0])
            line_list[2] = line_list[2].strip("\n")
            if line_list[0] >= KL_MAX and line_list[0] <= KL_MIN:
                kls.append(line_list)

    seq,struc,mfe,feq,min_ed = full_revolver(clean_struc,seq,init_seq,init_struc)
    #print("revolver done")
    problem=dir_mutate_mask_gen(clean_struc,struc,seq)

    return seq, struc,mfe,feq,min_ed,problem,init_seq


if __name__ == "__main__":
    try:
        opts = sys.argv

    except getopt.GetoptError:
            print("help_mes")
            sys.exit()
    try:
        revolver(opts[1])
    except IndexError:
        print("no file given")
    



    


