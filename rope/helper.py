from rope.tools.analysis import analysis_parser
from rope.tools.batch_revolvr import batch_parser
from rope.tools.build import build_parser
from rope.tools.continuous_revolvr import continuous_parser
from rope.tools.flip_trace import flip_parser
from rope.tools.trace import trace_parser
import shutil
from rope.version import get_version
parsers = [batch_parser,continuous_parser,build_parser,flip_parser,analysis_parser, trace_parser]


sep_len = (shutil.get_terminal_size().columns)//10*8

def main():

    print(f"""ROPE {get_version()}
=========================
ROPE Available Tools
=========================
""")
    print("-" * sep_len)
    for parser_func in parsers:
        
        parser = parser_func()
        print(parser.prog,"      ",parser.description)
        parser.print_usage()
        
        print("-" * sep_len)

    print("Run <tool> --help for detailed information.")

if __name__ == "__main__":
    main()