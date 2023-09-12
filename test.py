from p5 import *

WIDTH_NODE = 60
HEIGHT_NODE = 60

# Documentation p5: https://p5.readthedocs.io/en/latest/tutorials
f = None
scale: int = 1
offset: Vector = None

mouse_is_pressed: bool = False
last_mouse_x_when_pressed: int = 0




class ActionParameter:
    id = 0

    def __init__(self, name: str, type: str):
        self.name: str = name
        self.type: str = type
        self.id: int = ActionParameter.id
        ActionParameter.id += 1



class Action:

    def __init__(self, name: str, parameters: list[ActionParameter]):
        self.name: str = name
        self.parameters: list[ActionParameter] = parameters



class Node:

    def __init__(self):
        self.action: Action = None
        self.parameters: list[ActionParameter] = []

        self.previouses: list[Node] = []
        self.nexts: list[Node] = []
        self.position: tuple[int, int] = (0, 0)
        self.current_width_node: int = WIDTH_NODE
        self.current_height_node: int = HEIGHT_NODE

    def draw(self):

        self.current_width_node = WIDTH_NODE * scale
        self.current_height_node = HEIGHT_NODE * scale

        rect(self.position, self.current_width_node, self.current_height_node)

        fill(0)
        text_font(f)
        text_size(int(8 * scale))
        text_align("CENTER")
        text(self.action.name, (self.position[0], self.position[1] - (self.current_height_node) / 4))

        # Draw all the parameters
        position_parameter = 0
        for parameter in self.action.parameters:
            text(f"{parameter.name}: {parameter.type}", (self.position[0], self.position[1] + position_parameter * self.current_height_node / 4))
            position_parameter += 1

        # Create all the edges to the next nodes
        for next_node in self.nexts:
            start_x = self.position[0] + self.current_width_node / 2
            start_y = self.position[1]
            end_x = next_node.position[0] - next_node.current_width_node / 2
            end_y = next_node.position[1] 
            line((start_x, start_y), (end_x, end_y))
            # Draw the arrow (size is 1/6 of the node)
            size_arrow = next_node.current_height_node / 6
            line((end_x - size_arrow, end_y - size_arrow), (end_x, end_y))
            line((end_x - size_arrow, end_y + size_arrow), (end_x, end_y))


        fill(255)




nodes = []

# Add an event listener of the wheel to zoom in and out
def mouse_wheel(event):
    global scale
    global offset

    s = 1 + event.scroll.y / 10
    scale *= s

    mouse = Vector(event.x, event.y)
    offset = (offset - mouse) * s + mouse


def mouse_dragged(event):
    global offset

    last_pos_x = event._raw.last_event.pos[0]
    last_pos_y = event._raw.last_event.pos[1]
    offset.x += (event.x - last_pos_x)
    offset.y += (event.y - last_pos_y)


def setup():
    global f
    global offset
    global last_mouse_x

    offset = Vector(0, 0)
    size(2000, 2000)
    rect_mode(CENTER)
    f = create_font("Arial.ttf", 16,) # Arial, 16 point, anti-aliasing on

    # Create a node test
    action = Action("Stack", [ActionParameter("X1", "block"), ActionParameter("X2", "block")])
    node1 = Node()
    node1.action = action
    node1.position = (100, 100)

    nodes.append(node1)


    action = Action("Put-down", [ActionParameter("X1", "block")])
    node2 = Node()
    node2.action = action
    node2.position = (300, 100)

    nodes.append(node2)


    node1.nexts.append(node2)
    node2.previouses.append(node1)



def draw():

    background(255)
    translate(offset.x, offset.y)

    for node in nodes:
        node.draw()
   


    


if __name__ == "__main__":
    run()