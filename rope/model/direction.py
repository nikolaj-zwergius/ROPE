from __future__ import annotations


class direction():
    """Grid step plus transition maps used to trace structural diagrams.

    Concrete directions define ``row``/``column`` offsets, ``move_list`` maps
    corner or slash glyphs to the next direction class, and ``replace_list``
    maps input glyphs to normalized drawing symbols.
    """

    row = 0
    column = 0
    move_list: dict[str, type[direction]] = {}
    replace_list: dict[str, str] = {}

    def __int__(self, move_list: dict[str, type[direction]]) -> None:
        move_list = self.move_list

    def move(self, last_id: tuple[int, int]) -> tuple[int, int]:
        return (last_id[0]+self.row,last_id[1]+self.column)
        
class dir_up(direction):
    row = -1

    def __init__(self) -> None:
        super().__init__()
        self.move_list = {"╭":dir_right,
                    "╮":dir_left,
                    "/":dir_right,
                    chr(92):dir_left,}
        self.replace_list = {"/":"╭",chr(92):"╮","-":"─"}
        
    def __repr__(self) -> str:
        return "dir_up"
    
class dir_down(direction):
    row = 1

    def __init__(self) -> None:
        super().__init__()
        self.move_list = {
                    "╯":dir_left,"╰":dir_right,
                    "/":dir_left,
                    chr(92):dir_right,}
        self.replace_list = {"/":"╯",chr(92):"╰","-":"─"}
    def __repr__(self) -> str:
        return "dir_down"

class dir_left(direction):
    column = -1

    def __init__(self) -> None:
        super().__init__()
        self.move_list = {"╭":dir_down,
                    "╰":dir_up,
                    "/":dir_down,
                    chr(92):dir_up,}
        self.replace_list = {"/":"╭",chr(92):"╰","-":"─"}
    def __repr__(self) -> str:
        return "dir_left"

class dir_right(direction):
    column = 1

    def __init__(self) -> None:
        super().__init__()
        self.move_list = {
                    "╮":dir_down,
                    "/":dir_up,
                    "╯":dir_up,
                    chr(92):dir_down,}
        self.replace_list = {"/":"╯",chr(92):"╮","-":"─"}
    def __repr__(self) -> str:
        return "dir_right"