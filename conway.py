import numpy as np
import time


class Conway:
    def __init__(self):
        self.actualHeightSize = int(200)
        self.actualWidthSize = int(200)
        self.visibleHeightSize = int(16)
        self.visibleWidthSize = int(16)
        # Basically, we want the center of the actual grid and the visible grid to co incide
        # So, the first left coordinate would be at actual center - the half of visible grid length
        self.visibleLeftCoordinate = int(
            (self.actualWidthSize / 2) - (self.visibleWidthSize / 2))
        self.visibleTopCoordinate = int(
            (self.actualHeightSize / 2) - (self.visibleHeightSize / 2))

        self.lastUpdated = time.time()

        initialVisibleGrid = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])

        self.actualGrid = np.pad(initialVisibleGrid, ((self.visibleLeftCoordinate, self.visibleLeftCoordinate),
                                                      (self.visibleTopCoordinate, self.visibleTopCoordinate)), 'constant')
        self.actualGrid.astype(int)
        self.is_refreshed = False
        self.currentColumn = 0
        # print(self.actualGrid[242:258, 242:258])

    def get_cell_neighbour_life(self, i, j):
        neighbour_alives = 0

        width_wise = [i-1, i, i+1]
        height_wise = [j-1, j, j+1]

        for ii in width_wise:
            for jj in height_wise:
                ii_pos = width_wise.index(ii)
                jj_pos = height_wise.index(jj)
                # do not consider itself
                if (ii == i and jj == j):
                    continue

                # if they are left or right of the actual grid, it is by default dead
                if (ii < 0 or ii >= self.actualWidthSize):
                    continue
                #  if they are above or below the actual grid, dead
                if (jj < 0 or jj >= self.actualHeightSize):
                    continue
                neighbour_alives = neighbour_alives + self.actualGrid[ii, jj]

        return neighbour_alives

    def get_cell_next_life_alive(self, i, j):
        neighbour_alive_count = self.get_cell_neighbour_life(i, j)
        if (neighbour_alive_count < 2):
            return 0
        if (neighbour_alive_count > 3):
            return 0

        return 1

    def get_cell_next_life_dead(self, i, j):
        neighbour_alive_count = self.get_cell_neighbour_life(i, j)

        if (neighbour_alive_count == 3):
            return 1
        return 0

    def getNewFrame(self):
        new_frame = np.zeros((self.actualHeightSize, self.actualWidthSize))
        for i in range(self.actualHeightSize):
            for j in range(self.actualWidthSize):

                cell = self.actualGrid[i, j]

                if (cell):
                    new_frame[i][j] = int(self.get_cell_next_life_alive(i, j))
                else:
                    # dead
                    new_frame[i][j] = int(self.get_cell_next_life_dead(i, j))

        self.actualGrid = np.array(new_frame)
        self.actualGrid.astype(int)

    def getVisibleFrame(self):
        change = False
        if (time.time() - self.lastUpdated > 0.05):
            change = True
            if self.currentColumn >= self.visibleWidthSize - 1:
                print('called after', time.time()-self.lastUpdated)
                before = time.time()
                self.getNewFrame()
                print(time.time() - before, 'time for recalc')
                self.currentColumn = 0
            else:
                self.currentColumn = self.currentColumn + 1
            self.lastUpdated = time.time()

        return self.actualGrid[self.visibleTopCoordinate: (self.visibleTopCoordinate+self.visibleHeightSize), self.visibleLeftCoordinate: (self.visibleLeftCoordinate+self.visibleWidthSize)], self.currentColumn, change
