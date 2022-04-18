import PySimpleGUI as sg
import sys
from functools import reduce
import pickle
import math
import copy

from src.oval import Oval
from src.arrow import Arrow
import src.analysis as lgraph


CLOSED = sg.WIN_CLOSED

class Window:
    
    
    def __init__(self):

        sg.theme('Dark') 

        layout1 = [           
                      [sg.Button('Add Node'), sg.Button('Add Edge'), sg.Button('Delete'),
                       sg.Graph(
                            canvas_size=(650, 0),
                            graph_bottom_left=(0, 0),
                            graph_top_right=(650, 0)
                        ),
                       sg.Col([[sg.Button('Next')]], pad = (0, 0)),
                       sg.Col([[sg.Button('Result')]], pad = (0, 0)),
                       sg.Button('Exit')],
                      [
                          sg.Graph(
                            canvas_size=(1200, 800),
                            graph_bottom_left=(0, 0),
                            graph_top_right=(1200, 800),
                            change_submits=True,
                            key="graph"
                        )
                      ]
        ]      




        layout = [[sg.Column(layout1, key='-COL1-', element_justification="center",vertical_alignment="right")]]

        self._window = sg.Window('L-Graphs', layout,element_padding=(10,10))
        self._window.Finalize()


        self._graph = self._window.Element("graph")
        self._window['Result'].update(visible = False)
        self._graph.DrawRectangle((1200, 800), (0, 0), line_color="white", fill_color = 'white')
        self._res = []
        self._figures = []
        self._matr = []
        self._number = 1
        self._active = None
        self._group_index = None
        self._new_tile = False
        self._to_group = False
        self._figures.append(Oval((125,385), 0, self._graph, 'Start'))
        self._figures.append(Oval((925,385), 0, self._graph, 'Finish'))
        self._type_ = 'Normal'

    
    def screen_click(self, coords):
        self._active = None
        for index, figure in enumerate(self._figures):
            figure.activate(1)
            if figure.check_click(coords):
                self._active = index
        if self._active is not None:
            self._figures[self._active].activate(0)
        if self._to_group and self._active is not None and self._active != 0 and self._group_index != 1:
            if self._group_index == 0 or self._active == 1:
                self._figures.append(Arrow(self._graph, self._figures[self._group_index], self._figures[self._active], ""))
                self._matr.append([getattr(self._figures[self._group_index], 'text', ""), getattr(self._figures[self._active], 'text', ""), ""])
            elif str(type(self._figures[self._active])) != "<class 'src.arrow.Arrow'>":
                text = sg.popup_get_text('Enter label and bracket')
                if text is not None:
                    t1 = getattr(self._figures[self._group_index], '_text', "")
                    t2 = getattr(self._figures[self._active], '_text', "")
                    fig = None
                    add = False
                    for figure in self._figures:
                        if str(type(figure)) == "<class 'src.arrow.Arrow'>":
                            indecies = getattr(figure, '_numbers', [])
                            if indecies[0] == t1 and indecies[1] == t2:
                                fig = figure
                                add = True
                    if add:
                        fig.add_text(text)
                        self._matr.append([t1, t2, text])
                        fig = None
                        add = False
                    else:
                        self._figures.append(Arrow(self._graph, self._figures[self._group_index], self._figures[self._active], text))
                        self._matr.append([getattr(self._figures[self._group_index], '_text', ""), getattr(self._figures[self._active], '_text', ""), text])
        if self._new_tile:
            self._figures.append(Oval(coords, self._number, self._graph, self._type_))
            self._number += 1
            
    def get_click(self):   # узнать место клика
        return self._window.read()
        
            
    def add_node(self, mode):
        if mode == 0:
            self._new_tile = True
        else:
            self._new_tile = False
            
    def add_edge(self, mode):
        if mode == 0 and self._active is not None:
            self._figures[self._active].activate(1)
            self._group_index = self._active
            self._to_group = True
        else:
            self._to_group = False
            
    def delete(self):
        if self._active is not None and self._active > 1:
            del self._figures[self._active]
            self._active = None
            
    def next_(self):
        self._window['Next'].update(visible = False)
        self._window['Result'].update(visible = True)
        self._res.append(self._matr)
        self._figures = self._figures[:2]
        self._matr = []
        self._active = None
        self._group_index = None
        self._new_tile = False
        self._to_group = False
        
    def result(self):
        self._res.append(self._matr)
        sg.popup_ok(str(lgraph.check_eq(self._res[0], self._res[1])))
        self._window['Next'].update(visible = True)
        self._window['Result'].update(visible = False)
        self._res = []
        self._number = 1
        self._figures = self._figures[:2]
        self._matr = []
        self._active = None
        self._group_index = None
        self._new_tile = False
        self._to_group = False
        
    def draw(self):
        for figure in self._figures:
            figure.update()
        
    def close(self):  # закрыь окно
        for figure in self._figures:
            del figure
        self._window.close()

