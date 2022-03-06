# Importing packages
import random

class GameStatus:
    GAME_COMPLETED = True
    GAME_LOST = False
    GAME_INPROGRESS = None
 
class Minesweeper:
    def __init__(self, mines_no, n):
        self.mines_no = mines_no
        self.n = n
        self.vis = []
        self.flags = []
        self.numbers = [[0 for y in range(n)] for x in range(n)] 
        self.mine_values = [[' ' for y in range(n)] for x in range(n)]
        self.status = GameStatus.GAME_INPROGRESS
    
    # Function for setting up Mines
    def set_mines(self):
        # Track of number of mines already set up
        count = 0
        while count < self.mines_no:
            # Random number from all possible grid positions 
            val = random.randint(0, self.n*self.n-1)
            # Generating row and column from the number
            r = val // self.n
            col = val % self.n
            # Place the mine, if it doesn't already have one
            if self.numbers[r][col] != -1:
                count = count + 1
                self.numbers[r][col] = -1
    
    def set_values(self):
        """
        Set values given mine locations
        """
        for r in range(self.n):
            for col in range(self.n):
                if self.numbers[r][col] == -1:
                    continue
                if r > 0 and self.numbers[r-1][col] == -1:
                    self.numbers[r][col] = self.numbers[r][col] + 1
                # Check down    
                if r < self.n-1  and self.numbers[r+1][col] == -1:
                    self.numbers[r][col] = self.numbers[r][col] + 1
                # Check left
                if col > 0 and self.numbers[r][col-1] == -1:
                    self.numbers[r][col] = self.numbers[r][col] + 1
                # Check right
                if col < self.n-1 and self.numbers[r][col+1] == -1:
                    self.numbers[r][col] = self.numbers[r][col] + 1
                # Check top-left    
                if r > 0 and col > 0 and self.numbers[r-1][col-1] == -1:
                    self.numbers[r][col] = self.numbers[r][col] + 1
                # Check top-right
                if r > 0 and col < self.n-1 and self.numbers[r-1][col+1] == -1:
                    self.numbers[r][col] = self.numbers[r][col] + 1
                # Check below-left  
                if r < self.n-1 and col > 0 and self.numbers[r+1][col-1] == -1:
                    self.numbers[r][col] = self.numbers[r][col] + 1
                # Check below-right
                if r < self.n-1 and col < self.n-1 and self.numbers[r+1][col+1] == -1:
                    self.numbers[r][col] = self.numbers[r][col] + 1

    def neighbours(self, r, col):
        """
        Recursive 0 search
        """
        if [r,col] not in self.vis:
            self.vis.append([r,col])
            if self.numbers[r][col] == 0:
                self.mine_values[r][col] = self.numbers[r][col]
                if r > 0:
                    self.neighbours(r-1, col)
                if r < self.n-1:
                    self.neighbours(r+1, col)
                if col > 0:
                    self.neighbours(r, col-1)
                if col < self.n-1:
                    self.neighbours(r, col+1)    
                if r > 0 and col > 0:
                    self.neighbours(r-1, col-1)
                if r > 0 and col < self.n-1:
                    self.neighbours(r-1, col+1)
                if r < self.n-1 and col > 0:
                    self.neighbours(r+1, col-1)
                if r < self.n-1 and col < self.n-1:
                    self.neighbours(r+1, col+1)           
            if self.numbers[r][col] != 0:
                self.mine_values[r][col] = self.numbers[r][col]   

    def check_over(self):
        """
        Check completion of Minesweeper game
        """
        count = 0
        for r in range(self.n):
            for col in range(self.n):
                if self.mine_values[r][col] != ' ' and self.mine_values[r][col] != 'F':
                    count = count + 1         
        if count == self.n * self.n - self.mines_no:
            return True
        else:
            return False
                     
    def show_mines(self):
        """
        Supposedly shows all mines, but it doesn't work for some reason.
        """
        for r in range(self.n):
            for col in range(self.n):
                if self.numbers[r][col] == -1:
                    self.mine_values[r][col] = 'M'
    
    def gameplay(self, val):        
        r = val[0]-1
        c = val[1]-1
        match self.numbers[r][c]:
            case -1:
                # Landed On Mine; Game Over
                self.status = GameStatus.GAME_LOST
                self.mine_values[r][c] = 'M'
                self.show_mines()
            case 0:
                # 0 Cell Recursives
                self.vis = []
                self.mine_values[r][c] = '0'
                self.neighbours(r, c)
            case default:
                # Default case
                self.mine_values[r][c] = self.numbers[r][c]
        # Check for game completion	
        if(self.check_over()):
            self.status = GameStatus.GAME_COMPLETED
            self.show_mines()