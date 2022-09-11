from operator import truediv
import sys
from tkinter import Button, Label
import random
from typing import Counter
import settings
import ctypes

class Cell:
    all=[]
    cell_count=settings.cell_count
    cell_count_label_object=None
    def __init__(self, x,y,is_mine=False):
        self.is_mine=is_mine
        self.is_open=False
        self.is_mine_cand=False
        self.cell_btn_object= None
        self.X=x
        self.Y=y

        #to append
        Cell.all.append(self)

    def create_btn_object(self,location):
        btn=Button(
            location,
            width=12,
            height=4,
        )

        btn.bind('<Button-1>',self.left_click_action)
        btn.bind('<Button-3>',self.right_click_action)
        self.cell_btn_object=btn

    @staticmethod
    def create_cell_count_label(location):
        lbl=Label(
            location,
            text=f"cells left :{Cell.cell_count}",
            width=12,
            height=4,
            bg="black",
            fg="white",
            font=("",30)
        )
        Cell.cell_count_label_object=lbl

    def left_click_action(self,event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length==0:
                for cell_obj in self.surrounded_cell:
                    cell_obj.show_cell()
            self.show_cell()
            #if mines count= cell count player won
            if Cell.cell_count==settings.mines_count:
                ctypes.windll.user32.MessageBoxW(0, "congrats you won",0)

        #to cancel clicking ehen we've already clicked
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-1>')


    def get_cell_by_axis(self,x,y):
        for cell in Cell.all:
            if cell.X==x and cell.Y==y:
                return cell


    @property
    def surrounded_cell(self):
        cells=[
            self.get_cell_by_axis(self.X-1,self.Y-1),
            self.get_cell_by_axis(self.X-1,self.Y),
            self.get_cell_by_axis(self.X-1,self.Y+1),
            self.get_cell_by_axis(self.X,self.Y-1),
            self.get_cell_by_axis(self.X+1,self.Y-1),
            self.get_cell_by_axis(self.X+1,self.Y),
            self.get_cell_by_axis(self.X+1,self.Y+1),
            self.get_cell_by_axis(self.X,self.Y+1)
        ]
        cells=[cell for cell in cells if cell is not None]
        return cells


    @property
    def surrounded_cells_mines_length(self):
        Counter=0
        for cell in self.surrounded_cell:
            if cell.is_mine:
                Counter+=1
        return Counter

    def show_cell(self):
        if not self.is_open:
            Cell.cell_count-=1
            self.cell_btn_object.config(text=self.surrounded_cells_mines_length)
            
            #to replace the cell count everytime

            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.config(
                    text=f"cells left :{Cell.cell_count}"
                )
            # when clicked on a mine candidate but it is a normal when don't have to right click again
            
            self.cell_btn_object.config(
                bg="SystemButtonFace"
            ) 
        self.is_open=True

    #tod show all mines
    def show_mine(self):
        self.cell_btn_object.config(bg="red")
        ctypes.windll.user32.MessageBoxW(0, "ypu clickeed a mine",0)
        sys.exit()

        


    def right_click_action(self,event):
        if not self.is_mine_cand:
            self.cell_btn_object.config(
                bg="orange"
            )
            self.is_mine_cand=True
        else:
            self.cell_btn_object.config(
                bg="SystemButtonFace"
            )
            self.is_mine_cand=False

    @staticmethod
    def randomize_mines():
        picked_cells=random.sample(
            Cell.all,settings.mines_count
        )
        for picked_cells in picked_cells:
            picked_cells.is_mine=True


    def __repr__(self):
        return f"cell({self.X},{self.Y})"
