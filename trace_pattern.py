import numpy as np
import rope_def as rd
import getopt,sys


def base_pair_id(pattern,tup):
    up,down,left,rigth = rd.check_round(pattern,tup)
    if up in ["┊","!","*"]:
        return (tup[0]-2,tup[1]),up
    if down in ["┊","!","*"]:
        return (tup[0]+2,tup[1]),down
    if pattern[tup[0]][tup[1]] in rd.one_letter_code.keys():
        return None,"."
    return None,None

def trace_backbone(pattern):
    p5 = rd.find_5_prime(pattern)
    up,down,left,rigth = rd.check_round(pattern,p5)
    next = rd.dirction
    #print(p5,up,down,left,rigth)
    if up.isalpha():
        first = (p5[0]-1,p5[1])
        dir = rd.dir_up()
    elif down.isalpha():
        first = (p5[0]+1,p5[1])
        dir = rd.dir_down()
    elif left.isalpha():
        first = (p5[0],p5[1]-1)
        dir=rd.dir_left()
    elif rigth.isalpha():
        first = (p5[0],p5[1]+1)
        dir=rd.dir_rigth()
    else:
        raise Exception("No vaild frist base")

    seq = ""
    base_pair =""
    next_base = first
    bracket0 =[]
    bracket1 =[]
    bracket2 =[]

    while pattern[next_base[0]][next_base[1]] != "3":
        next_base_name = pattern[next_base[0]][next_base[1]]
        #print(next_base_name)
        if next_base_name.isalpha() and next_base_name not in rd.one_letter_code.keys():
            if next_base_name == "T":
                next_base_name = "U"
            else:
                next_base_name ="N"
        #print(next_base_name)
        match_id,match_type = base_pair_id(pattern,next_base)
        match match_type:
            case "*":
                if match_id not in bracket0 and next_base not in bracket0:
                    bracket0.append(match_id)
                    base_pair+="["
                if next_base in bracket0:
                    bracket0.pop()
                    base_pair+="]"
            case "!":
                if match_id not in bracket1 and next_base not in bracket1:
                    bracket1.append(match_id)
                    base_pair+="{"
                if next_base in bracket1:
                    bracket1.pop()
                    base_pair+="}"
            case "┊":
                if match_id not in bracket2 and next_base not in bracket2:
                    bracket2.append(match_id)
                    base_pair+="("
                if next_base in bracket2:
                    bracket2.pop()
                    base_pair+=")"
            case ".":
                base_pair+="."
            case _:
                pass

        if next_base_name in rd.one_letter_code.keys():
            seq+=next_base_name
        if next_base_name in dir.move_list.keys():
            dir=dir.move_list[next_base_name]()
        next_base = dir.move(next_base)
    return seq,base_pair


def trace_pattern_out(file):
    pattern = rd.generate_np_pattern(file)
    seq,base_pair= trace_backbone(pattern)
    with open(file, "r") as f:
        name = f.readline().rstrip().lstrip(">")

    with open("target.txt","w") as output:
       output.write(name)
       output.write("\n")
       output.write(base_pair)
       output.write("\n")
       output.write(seq)


if __name__ == "__main__":
    try:
        opts = sys.argv

    except getopt.GetoptError:
            print("help_mes")
            sys.exit()
    try:
        trace_pattern_out(opts[1])
    except IndexError:
        print("no file given")
    


