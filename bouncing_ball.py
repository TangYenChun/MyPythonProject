"""
File: bouncing_ball.py
Name: Bella
-------------------------
"""

from campy.graphics.gobjects import GOval
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked

VX = 3
DELAY = 10
GRAVITY = 1
SIZE = 20
REDUCE = 0.9
START_X = 30
START_Y = 40
# The number of times the ball leaves the rightmost side of the window,
# the game cannot be started again if this number is exceeded.
ROUND = 3

# Global variable
window = GWindow(800, 500, title='bouncing_ball.py')
ball = GOval(SIZE, SIZE, x=START_X, y=START_Y)
can_start = True  # To determine if the current mouse click is valid.
count = 0  # Calculate the number of times the ball leaves the window.


def main():
    """
    This program simulates a bouncing ball at (START_X, START_Y)
    that has VX as x velocity and 0 as y velocity. Each bounce reduces
    y velocity to REDUCE of itself.
    """
    ball.filled = True
    window.add(ball)

    onmouseclicked(move)


def back_to_start():
    """
    Set the position of the ball to the starting position
    """
    ball.x = START_X
    ball.y = START_Y


def move(event):
    """
    This function simulates a bouncing ball.
    """
    global can_start, count
    # Determine if the current mouse click is valid.
    # Mouse clicks are only effective when the ball is stationary.
    if can_start:
        can_start = False  # When the ball starts to move, change the status to false.
        vy = 0  # The initial value of y velocity is 0.

        # The while loop will continue until the ball leaves the rightmost side of the window.
        while True:
            vy += GRAVITY  # The y velocity add gravity in every round.
            # Check the ball is moving upwards or downwards.
            is_up = True if vy < 0 else False
            ball.move(VX, vy)

            # Check if the ball has leave the rightmost side of the window.
            if ball.x + SIZE >= window.width:
                count += 1
                # Check if the current count is greater than the maximum count;
                # if so, the game cannot be started again.
                can_start = True if count < ROUND else False
                back_to_start()  # Set the ball back to the start point.
                break

            # Check if the ball has touched the bottom.
            if ball.y + SIZE >= window.height and not is_up:
                vy = int(vy * REDUCE)  # The y velocity of upwards is 90% of its speed before the bounce.
                vy = -vy  # Change direction.

            pause(DELAY)
    

if __name__ == "__main__":
    main()
