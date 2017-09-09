# Bad Eye Tracking Games

Hello and welcome to mine (Misha Ivkov), Cuebeom Choi, and Woody Ye's 
project for hackCMU 2017! For this hackathon we decided to 
create a web browser based game which used the webcam to capture eye 
movement instead of using a mouse. The game we chose to hack for this
was [Brick Breaker](https://en.wikipedia.org/wiki/Brick_Breaker), an 
ageless classic. The only caveat is that not only is the game eye 
controlled, but the paddle will move in the opposite direction of where
you move your eyes and/or face. We hope you enjoy!
## Setup
The requirements for running the main script are having `npm`, `node`, `python3`, `opencv2`, and `pip3`.
To set up your environment inside this folder and run:
```bash
$ npm install express http python-shell body-parser path
$ pip3 install opencv-python pynput threading
$ node index.js
```
This will start the server at `localhost:8000`, and `8000` is required to be
open for the program to run. 

## Gameplay
1. When the game is opened at its default path, the first screen
will contain calibration instructions for the eye tracker. This is mostly
so the program can calculate position accurately. 
2. You will be asked to click on each of the three circles and stare at it immediately after clicking.
A good rule of thumb is to wait until your webcam turns off to look away and 
proceed. 
3. After doing all three circles, scroll down slightly in the window
to access the "submit" button, which will bring you to the actual game.
There you will play classic Brick Breaker. 
4. Notice that even after winning or losing, you will be able to move your paddle around. This is for you to practice your skills :).