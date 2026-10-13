import os
import RNA
import random
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))


def make_kl_list(KL_MIN = -7.2,KL_OFF = -6.0,KL_MAX = -10.8):



    kls=[]

    with open(f"{parent_dir_path}/data/kl_list","r") as f:
             for line in f:
                 line_list = line.split(",")
                 line_list[0] = line_list[0]
                 line_list[2] = line_list[2].strip("\n")
                 if float(line_list[0]) >= KL_MAX and float(line_list[0]) <= KL_MIN:
                     kls.append(line_list)

    test = set()
    comp = set()
    for i in range(len(kls)):
        if kls[i][1] not in test and kls[i][1] not in comp:
            test.add(kls[i][1])
            comp.add(kls[i][2])

    single_kl = []

    for i in range(len(kls)):
        if kls[i][1] in test:
            single_kl.append(kls[i])

    return single_kl





def pairwise_valid(kl1, kl2, KL_OFF = -6.0):
    if kl1[1] == kl2[1] or kl1[2] == kl2[2]:
        return False
    engery1 = RNA.duplexfold(kl1[1], kl2[1]).energy
    engery2 = RNA.duplexfold(kl1[2], kl2[2]).energy
    energy3 = RNA.duplexfold(kl1[1], kl2[2]).energy
    energy4 = RNA.duplexfold(kl1[2], kl2[1]).energy
    if engery1 < KL_OFF or engery2 < KL_OFF or energy3 < KL_OFF or energy4 < KL_OFF:
        return False
    return True

def make_compatibility_file():
    KL_MIN = -7.2
    KL_OFF = -6.0
    KL_MAX = -10.8
    single_kl = make_kl_list(KL_MIN, KL_OFF, KL_MAX)
    compatibility = [0] * len(single_kl)
    for i, kl1 in enumerate(single_kl):
        for j in range(i + 1, len(single_kl)):
            kl2 = single_kl[j]
            
            if pairwise_valid(kl1, kl2, KL_OFF):
                compatibility[i] |= 1 << j
                compatibility[j] |= 1 << i

    with open(f"{parent_dir_path}/data/kl_compatibility", "w") as f:
        for i, kl in enumerate(single_kl):
            f.write(f"{kl},{compatibility[i]}\n")


def load_compatibility_file():
    KL_lookup = []
    with open(f"{parent_dir_path}/data/kl_compatibility", "r") as f:
        compatibility = [0] * 0

        for line in f:
            line_list = line.split(",")
            compatibility.append(int(line_list[3].strip("\n")))
            KL_lookup.append((line_list[1], line_list[2].strip("\n")))

    return compatibility, KL_lookup


def is_valid_sample(sample: list[int], compatibility: list[int]) -> bool:
    """Return True if every pair in sample is compatible."""
    for i, a in enumerate(sample):
        for b in sample[i + 1:]:
            if not compatibility[a] & (1 << b):
                return False

    return True


def generate_kl_sample(kl_number: int, compatibility: list[int]) -> list[int]:
    is_valid = False
    while not is_valid:
        sample = random.sample(list(range(len(compatibility))), k=kl_number)
        is_valid = is_valid_sample(sample, compatibility)
    return sample


if __name__ == "__main__":
    make_compatibility_file()