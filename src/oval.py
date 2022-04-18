from src.obj import Obj

class Oval(Obj):
    
    
    def __init__(self, coords, number, graph, type_ = 'Normal'):
        self._coords = coords
        self._graph = graph
        self._text = str(number)
        self._type = type_
        x = coords[0]
        y = coords[1]
        if type_=='Normal':
            self._color = 'black'
            graph.draw_text(self._text, (x,y), color = "black")
            graph.draw_oval((x - 25, y + 15), (x + 25, y - 15), fill_color = None, line_color = 'black', line_width = 1)
        elif type_=='Start':
            self._color = 'green'
            self._text = 'start'
            graph.draw_text('start', (x,y), color = "green")
            graph.draw_oval((x - 25, y + 15), (x + 25, y - 15), fill_color = None, line_color = 'green', line_width = 1)
        else:
            self._text = 'finish'
            self._color = 'red'
            graph.draw_text('finish', (x,y), color = "red")
            graph.draw_oval((x - 25, y + 15), (x + 25, y - 15), fill_color = None, line_color = 'red', line_width = 1)
        
        
    
    def activate(self, mode):
        x = self._coords[0]
        y = self._coords[1]
        if mode == 0:
            self._color = 'pink'
            self._graph.draw_text(self._text, (x,y), color = self._color)
            self._graph.draw_oval((x - 25, y + 15), (x + 25, y - 15), fill_color = None, line_color = self._color, line_width = 1)
        else:
            if self._text == 'start':
                self._color = 'green'
            elif self._text == 'finish':
                self._color = 'red'
            else:
                self._color = 'black'
            self._graph.draw_text(self._text, (x,y), color = self._color)
            self._graph.draw_oval((x - 25, y + 15), (x + 25, y - 15), fill_color = None, line_color = self._color, line_width = 1)
    
    def clear(self):
        x = self._coords[0]
        y = self._coords[1]
        self._graph.draw_rectangle((x-5,y+5), (x+5, y-5), fill_color = "white", line_color = 'white')
        self._graph.draw_oval((x - 25, y + 15), (x + 25, y - 15), fill_color = None, line_color = 'white', line_width = 1)
        
    def get_all_info(self):
        return (self._coords, self._color, self._text)
        
    def update(self):
        x = self._coords[0]
        y = self._coords[1]
        self._graph.draw_text(self._text, (x,y), color = self._color)
        self._graph.draw_oval((x - 25, y + 15), (x + 25, y - 15), fill_color = None, line_color = self._color, line_width = 1)
        
