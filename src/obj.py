class Obj:
    
    _coords = None
    _graph = None
    
    def __init__(self, color, graph):
        self._color = color
        self._graph = graph
        
    def check_click(self, click_coords):
        x = self._coords[0]
        y = self._coords[1]
        if (x-25) <= click_coords[0] <= (x+25) and (y-15) <= click_coords[1] <= (y+15):
            return True
        else:
            return False

        
    def __del__(self):
        self.clear()
    
