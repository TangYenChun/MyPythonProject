"""
File: babygraphics.py
Name: Bella
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    graph_width = width - GRAPH_MARGIN_SIZE*2
    if year_index == 0:
        return GRAPH_MARGIN_SIZE
    return GRAPH_MARGIN_SIZE+int(graph_width * (year_index / len(YEARS)))


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Draw horizontal lines.
    x1 = GRAPH_MARGIN_SIZE
    x2 = CANVAS_WIDTH - GRAPH_MARGIN_SIZE
    y = GRAPH_MARGIN_SIZE
    canvas.create_line(x1, y, x2, y)

    y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
    canvas.create_line(x1, y, x2, y)

    # Draw vertical line
    for index, year in enumerate(YEARS):
        x = get_x_coordinate(CANVAS_WIDTH, index)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT)
        canvas.create_text(x+TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=year, anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid
    # A list of coordinate and text(name and rank) for drawing.
    draw_list = []
    line_height = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE * 2

    # Compose list data for drawing.
    for name in lookup_names:
        if name not in name_data:
            continue

        # Dictionary, key-> vertex, value -> text
        vertex_text_dict = {}
        # Dictionary, key -> year(str), value -> rank(str)
        year_rank_dict = name_data[name]
        for index, year in enumerate(YEARS):
            x = get_x_coordinate(CANVAS_WIDTH, index)
            # If year is not in year_rank_dict, then draw the text on the bottom of the canvas.
            if str(year) not in year_rank_dict:
                vertex_text_dict[(x, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)] = f'{name} *'
                continue
            rank = int(year_rank_dict[str(year)])
            # Get the height of the rank.
            y = int(line_height * (rank/MAX_RANK)) + GRAPH_MARGIN_SIZE
            vertex_text_dict[(x, y)] = f'{name} {rank}'
        draw_list.append(vertex_text_dict)

    # Draw lines
    for index, data in enumerate(draw_list):
        # Let the color be used in a loop.
        idx = index % len(COLORS)
        last_vertex = None
        for vertex, text in data.items():
            canvas.create_text(vertex[0] + TEXT_DX, vertex[1], text=text, anchor=tkinter.SW, fill=COLORS[idx])
            # If current vertex is not the first, then create a line.
            if last_vertex is not None:
                canvas.create_line(last_vertex[0], last_vertex[1], vertex[0], vertex[1], width=LINE_WIDTH, fill=COLORS[idx])
            last_vertex = vertex


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
