"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
import launchpad_py as launchpad
from core.engine import Minesweeper
from threading import Thread

class Colors:
    # Green
    DARK_GREEN = [0, 1]
    MID_GREEN = [0, 2]
    LIGHT_GREEN = [0, 3]

    # Lime
    DARK_LIME = [1, 1]
    MID_LIME = [1, 2]
    LIGHT_LIME = [1, 3]

    # Yellow
    DARK_YELLOW = [2, 1]
    MID_YELLOW = [2, 2]
    LIGHT_YELLOW = [2, 3]

    # Orange
    ORANGE = [3, 1]
    LIGHT_ORANGE = [3, 2]
    YELLOW = [3, 3]



class LaunchpadWrapper:
    def __init__(self):
        # Init Minesweeper
        self.minesweeper = Minesweeper(8,8)
        self.minesweeper.set_mines()
        self.minesweeper.set_values()
        self.last_values = []
        self.mines = []
        self.status = 0
        self.inBlinkLoop = False

        # Diff Setup
        self.curDiff = 0
        self.diffs = [4,6,8]

        # Open Launchpad Connection
        self.lp = launchpad.Launchpad()
        if self.lp.Open( 0 ):
            print("Opened launchpad.")
            self.isLp = True
        else:
            self.isLp = False  
    
    def resetGame(self):
        self.status = 0
        self.minesweeper = Minesweeper(self.diffs[self.curDiff],8)
        self.minesweeper.set_mines()
        self.minesweeper.set_values()
        self.last_values = []
        self.mines = []
        self.inBlinkLoop = False
    
    def blinkLoop(self, x):
        if not self.inBlinkLoop:
            self.inBlinkLoop = True
            y = {False: Colors.ORANGE, True: Colors.LIGHT_LIME}
            a,b = y[x]
            while self.status != 0:
                for i in range(8):
                    self.lp.LedCtrlXY(8, i+1, a, b)
                for item in self.mines:
                    self.lp.LedCtrlXY(item[0], item[1]+1, 3, 1)
                time.sleep(1)
                for i in range(8):
                    self.lp.LedCtrlXY(8, i+1, 0, 0)
                for item in self.mines:
                    self.lp.LedCtrlXY(item[0], item[1]+1, 0, 0)
                time.sleep(1)
    
    def setColors(self):
        colors = {
            "0": Colors.DARK_GREEN,
            "1": Colors.LIGHT_LIME,
            "2": Colors.LIGHT_YELLOW,
            "3": Colors.LIGHT_GREEN,
            "M": Colors.ORANGE
        }
        for r in range(self.minesweeper.n):
            for col in range(self.minesweeper.n):
                val = str(self.minesweeper.mine_values[r][col])
                if val in ["0", "1","2","3"]:
                    self.lp.LedCtrlXY(r, col+1, colors[val][0], colors[val][1])
                elif val == "M":
                    self.lp.LedCtrlXY(r, col+1, colors[val][0], colors[val][1])
                    self.mines.append([r,col])
    
    def changeDiff(self, increment):
        """
        Change diff by given increment
        Max: 2 (3)
        Min: 0 (1)
        """
        if self.curDiff + increment not in [-1, 3]:
            self.curDiff += increment
            print(f"Current difficulty set to {self.curDiff+1}")
            self.lp.Reset()
            self.resetGame()

    def run(self):
        lastBut = (-99,-99)
        self.lp.Reset()
        while True:
            buts = self.lp.ButtonStateXY()
            if buts != [] and buts != lastBut and buts[2] == True:
                del buts[2]
                if buts[0] != 8:
                    match buts:
                        case [0,0]:
                            lastBut = buts
                            self.lp.Reset()
                            self.resetGame()
                        case [2,0]:
                            self.changeDiff(-1)
                        case [3,0]:
                            self.changeDiff(1)  
                        case default:
                            if self.status == 0:
                                lastBut = buts
                                x = buts[0]+1
                                y = buts[1]
                                self.minesweeper.gameplay([x,y])
                                self.setColors()
                                if self.minesweeper.status in [True, False]:
                                    Thread(target=self.blinkLoop, args=(self.minesweeper.status,)).start()
                                    self.status = 1
                else:
                    ## Handle for all right buttons to also reset game
                    self.lp.Reset()
                    self.resetGame()

LaunchpadWrapper().run()
