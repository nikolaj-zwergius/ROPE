if __name__ == "__main__":
    import sys
    import os
    from io import TextIOWrapper
    dir_path = os.path.dirname(os.path.realpath(__file__))  
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    wd = os.getcwd()
    
    function_help ={
        "fold":"functions as batch_revolvr from ROAD takes <file1> [<file2> ...] [runs_per_file] [max_workers],\n use the batch_revolvr.py or batch_revolvr.bat of ROPE for dircict call\n",
        "analysis":"functions as trace_analysis from ROAD takes [<file1> ...],\n use the trace_analysis.py or trace_analysis.bat of ROPE for dircict call\n",
        "build":"functions as RNAbuild from ROAD takes [<file1> ...],\n use the RNAbuild.py or RNAbuild.bat of ROPE for dircict call\n",
    }
    functions = function_help.keys()

    if len(sys.argv) == 1:
        print("\nNo function given is the allowed options\n")
        for i in function_help:
            print(f"{i}: {function_help[i]}")
        sys.exit()

    if sys.argv[1] not in functions:
        print("\nincorrect function called is the allowed options\n")
        for i in function_help:
            print(f"{i}: {function_help[i]}")
        sys.exit()