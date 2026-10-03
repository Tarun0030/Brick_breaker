# Python Brick Breaker

A simple **Brick Breaker game built with Python and Pygame**.

The game includes a paddle, bouncing balls, colored bricks, score
tracking, combo tracking, lives, random extra-ball powerups, and
win/game-over screens.

## Requirements

-   Python 3.x
-   Pygame

## Installation

Install Pygame before running the game:

``` bash
pip install pygame
```

> If you are using Pydroid 3 on Android, install `pygame` through the
> Pydroid Pip/package installer. Do **not** put `pip install pygame`
> inside the `.py` file.

## How to Run

Save the game as:

``` text
python_breaker.py
```

Then run:

``` bash
python python_breaker.py
```

The game creates an **800 × 600** window titled `Python Brick Breaker`.

## Controls

  Key            Action
  -------------- --------------------------------
  Left Arrow     Move paddle left
  Right Arrow    Move paddle right
  Space          Restart after Game Over or Win
  Close Window   Exit the game

## Gameplay

-   Use the paddle to bounce the ball.
-   Break all the bricks to win.
-   Each broken brick gives **100 points**.
-   The combo counter increases when the ball hits the paddle or a
    brick.
-   The player starts with **3 lives**.
-   When a ball falls below the screen, one life is lost.
-   If lives reach zero, the game ends.
-   Some bricks have a **10% chance** of spawning a powerup.
-   Catching the purple powerup adds an extra ball.
-   Breaking all bricks displays the **YOU WIN!** screen.

## Game Layout

-   **Screen:** 800 × 600
-   **Brick rows:** 5
-   **Bricks per row:** 8
-   **Total bricks:** 40
-   **Paddle speed:** 8 pixels per frame
-   **Game frame rate:** 60 FPS

## Main Components

### Ball

The `Ball` class manages:

-   Ball position
-   Ball radius
-   Horizontal and vertical movement
-   Ball collision rectangle
-   Ball drawing

### Paddle

The paddle is controlled using the left and right arrow keys and is
restricted to the screen boundaries.

### Bricks

Bricks are generated in a grid of 5 rows and 8 columns. Each row uses a
different color from the configured color list.

### Collision Detection

The game checks collisions between:

-   Ball and screen walls
-   Ball and paddle
-   Ball and bricks
-   Powerup and paddle

### Scoring

Every brick destroyed adds:

``` text
100 points
```

The game also maintains a combo counter.

### Lives

The player starts with:

``` text
3 lives
```

A life is lost whenever a ball falls below the bottom of the screen.

### Powerup

A destroyed brick can randomly create a purple powerup. If the paddle
catches it, an additional ball is added to the game.

## Restarting

After **Game Over** or **YOU WIN!**, press:

``` text
SPACE
```

The game resets:

-   Score
-   Combo
-   Lives
-   Bricks
-   Paddle position
-   Balls
-   Game state

## Project Structure

``` text
python-brick-breaker/
│
├── python_breaker.py
└── README.md
```

## Technology

-   **Python**
-   **Pygame**
-   `random` for random ball direction and powerup generation
-   `sys` for exiting the application

## Source

The game implementation in `python_breaker.py` initializes Pygame,
creates the game screen, builds the brick layout, handles collisions and
scoring, and runs the main 60 FPS game loop.
fileciteturn0file0L1-L16

The brick layout is configured as 5 rows × 8 columns, for a total of 40
bricks. fileciteturn0file0L91-L115

The game awards 100 points for each destroyed brick and can spawn a
random powerup. fileciteturn0file0L298-L323

## License

This project is provided for learning and personal use.
