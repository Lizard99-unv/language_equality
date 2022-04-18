import numpy as np

from src.obj import Obj

class Arrow(Obj):
    
    
    def __init__(self, graph, oval1, oval2, text):
        self._numbers = []
        self._x1 = oval1.get_all_info()[0][0]
        self._y1 = oval1.get_all_info()[0][1]
        self._numbers.append(oval1.get_all_info()[2])
        self._x2 = oval2.get_all_info()[0][0]
        self._y2 = oval2.get_all_info()[0][1]
        self._numbers.append(oval2.get_all_info()[2])
        self._graph = graph
        self._color = 'black'
        self._text = [text]
        if self._x1 == self._x2 and self._y1 == self._y2:
            self._own = True
            self._graph.draw_image(filename = './src/img/loop.png', location = (self._x1 - 56, self._y1 + 82))
        else:
            self._own = False
            self.draw_arrow('black')
            
    def add_text(self, text):
        self._text.append(text)
        
    def check_click(self, click_coords):
        if self._own:
            x = self._x1
            y = self._y1
            if x-56 <= click_coords[0] <= x+56 and y+82 >= click_coords[1] >= y+20:
                return True
            else:
                return False
        else:
            p1 = np.array([self._x1,self._y1])
            p2 = np.array([self._x2, self._y2])
            a = p2 - p1
            p2 = p2 - 25*a/np.linalg.norm(a)
            p1 = p1 + 25*a/np.linalg.norm(a)
            while np.linalg.norm(p1 - p2) > 1:
                if np.linalg.norm(p1 - click_coords) < 15:
                    return True
                p1 = p1 + a/np.linalg.norm(a)
            return False
        
    def draw_arrow(self,color):
        graph = self._graph
        self._color = color
        p1 = np.array([self._x1,self._y1])
        p2 = np.array([self._x2, self._y2])
        t1 = p1
        t2 = p2
        a = p2 - p1
        n = np.array([a[1],-a[0]])
        p2 = p2 - 25*a/np.linalg.norm(a)
        p1 = p1 + 25*a/np.linalg.norm(a)
        graph.draw_line(tuple(p1), tuple(p2), color = color, width = 1)
        o = p2 - 10*a/np.linalg.norm(a)
        o1 = o + 10*n/np.linalg.norm(o)
        o2 = o - 10*n/np.linalg.norm(o)
        graph.draw_line(tuple(p2), tuple(o1), color = color, width = 1)
        graph.draw_line(tuple(p2), tuple(o2), color = color, width = 1)
        if self._color == 'white':
            a = 0
            for text in self._text:
                a += 5
            graph.draw_rectangle(tuple((p1+p2)/2+15*n/np.linalg.norm(n)-a*np.array([20,20])), tuple((p1+p2)/2+15*n/np.linalg.norm(n)+a*np.array([20,20])), fill_color = self._color, line_color = self._color)
        else:
            a = 0
            for text in self._text:
                graph.draw_text(text, tuple((p1+p2)/2+(a+15)*n/np.linalg.norm(n)), color = self._color)
                a += 15
        
    def activate(self, mode):
        if self._own:
            if mode == 0:
                self._color = 'pink'
                self._graph.draw_image(filename = './src/img/loop_pink.png', location = (self._x1 - 56, self._y1 + 82))
                a = 0
                for text in self._text:
                    self._graph.draw_text(text, (self._x1, self._y1+42+a), color = self._color)
                    a += 15
            else:
                self.clear()
                self._color = 'black'
                self._graph.draw_image(filename = './src/img/loop.png', location = (self._x1 - 56, self._y1 + 82))
                a = 0
                for text in self._text:
                    self._graph.draw_text(text, (self._x1, self._y1+42+a), color = self._color)
                    a += 15
        else:
            if mode == 0:
                self.draw_arrow('pink')
            else:
                self.draw_arrow('black')
    
    def clear(self):
        if self._own:
            a = 0
            for text in self._text:
                a += 15
            self._graph.draw_rectangle((self._x1-56,self._y1+82+a), (self._x1+56, self._y1), fill_color = "white", line_color = 'white')
        else:
            self.draw_arrow('white')
        
    def update(self):
        if self._own:
            if self._color == 'black':
                self._graph.draw_image(filename = './src/img/loop.png', location = (self._x1 - 56, self._y1 + 82))
                a = 0
                for text in self._text:
                    self._graph.draw_text(text, (self._x1, self._y1+42+a), color = self._color)
                    a += 15
            else:
                self._graph.draw_image(filename = './src/img/loop_pink.png', location = (self._x1 - 56, self._y1 + 82))
                a = 0
                for text in self._text:
                    self._graph.draw_text(text, (self._x1, self._y1+42+a), color = self._color)
                    a += 15
        else:
            self.draw_arrow(self._color)
