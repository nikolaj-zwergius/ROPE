class dirction():
    row = 0
    colum = 0
    move_list ={}
    def __int__(self,move_list):
        move_list = self.move_list
    def move(self,last_id):
        return (last_id[0]+self.row,last_id[1]+self.colum)
        
class dir_up(dirction):
    row = -1
    def __init__(self):
        super().__init__()
        self.move_list = {"╭":dir_rigth,
                    "╮":dir_left,
                    "/":dir_rigth,
                    chr(92):dir_left,}
        self.replace_list = {"/":"╭",chr(92):"╮","-":"─"}
        
    def __repr__(self):
        return "dir_up"
    
class dir_down(dirction):
    row = 1
    def __init__(self):
        super().__init__()
        self.move_list = {
                    "╯":dir_left,"╰":dir_rigth,
                    "/":dir_left,
                    chr(92):dir_rigth,}
        self.replace_list = {"/":"╯",chr(92):"╰","-":"─"}
    def __repr__(self):
        return "dir_down"
class dir_left(dirction):
    colum = -1
    def __init__(self):
        super().__init__()
        self.move_list = {"╭":dir_down,
                    "╰":dir_up,
                    "/":dir_down,
                    chr(92):dir_up,}
        self.replace_list = {"/":"╭",chr(92):"╰","-":"─"}
    def __repr__(self):
        return "dir_left"
class dir_rigth(dirction):
    colum = 1
    def __init__(self):
        super().__init__()
        self.move_list = {
                    "╮":dir_down,
                    "/":dir_up,
                    "╯":dir_up,
                    chr(92):dir_down,}
        self.replace_list = {"/":"╮",chr(92):"╯","-":"─"}
    def __repr__(self):
        return "dir_rigth"