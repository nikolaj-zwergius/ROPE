import numpy as np
import utils.rope_def as rd
import getopt,sys


flips =[((0),{"╰":"╭","╭":"╰","╯":"╮","╮":"╯","/":chr(92),chr(92):"/"},"Flipped file:"),
        ((1),{"╯":"╭","╮":"╰","╭":"╯","╰":"╮"},"Reversed file:"),
        ((0,1),{"╰":"╭","╭":"╰","╯":"╮","╮":"╯","/":chr(92),chr(92):"/"},"Reversed and Flipped file:")]

def flip_pattern(file):
     pattern = rd.generate_np_pattern(file)
     with open("flip.txt","w",encoding="utf-8") as f:
        f.write("Input file:")
        f.write("\n")
        for row in pattern:
            test = "".join(row)
            f.write(test)
            f.write("\n")
        f.write("\n")
        f.write("\n")

        for options in flips:
            f.write(options[2])
            f.write("\n")
            
            for row in np.flip(pattern,options[0]):
                flip_table=options[1]
                for i in range(len(row)):
                    if row[i] in flip_table.keys():
                        row[i] = flip_table[row[i]]
                test = "".join(row)
                f.write(test)
                f.write("\n")
            f.write("\n")
            f.write("\n")
        

flip_pattern("test.txt")

if __name__ == "__main__":
    try:
        opts = sys.argv

    except getopt.GetoptError:
            print("help_mes")
            sys.exit()
    try:
        flip_pattern(opts[1])
    except IndexError:
        print("no file given")


