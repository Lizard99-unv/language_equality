import logging

from src.window import Window, CLOSED

def main():

    logging.basicConfig(filename="event.log", level=logging.INFO, filemode="w")

    window = Window()

    try:
        while True:                             # The Event Loop
            event, values = window.get_click()
            if event == 'graph':
                window.screen_click(values['graph'])
            if event == "Add Node":
                window.add_node(0)
            else:
                window.add_node(1)
                
            if event == "Add Edge":
                window.add_edge(0)
            else:
                window.add_edge(1)
                
            if event == 'Delete':
                window.delete()
            
            if event == CLOSED or event == 'Exit':
                break      
                
            if event == 'Next':
                window.next_()
                
            if event == 'Result':
                window.result()
            
            logging.info(event)
            logging.info(values)
            window.draw()

        window.close()
    except Exception as exc:
        window.close()
        logging.error("Error occured! ", exc)

if __name__=="__main__":
    main()
