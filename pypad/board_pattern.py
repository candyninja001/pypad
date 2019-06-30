from .common import binary_to_list

class BoardPattern:
    def __init__(self, rows):
        self._rows = []
        for r in range(5):
            self._rows.append([])
            for c in range(6):
                self._rows[r].append(False)

        if len(rows) == 5:
            for r in range(5):
                for c in binary_to_list(rows[r]):
                    self._rows[r][c] = True
    
    # x - 0 at left
    # y - 0 at top
    def contains(self, x, y) -> bool:
        return self._rows[y][x]

    # x - 0 at left
    # y - 0 at top
    
    # x 0,1,2,3 -> 0,1,2,3
    # x 4,5,6 ->  3,4,5
    # x -1,-2,-3 -> -1,-2,-3
    # x -4,-5,-6,-7 ->  -3,-4,-5,-6
    
    # y 0,1,2 -> 0,1,2
    # y 3,4,5 -> 2,3,4
    # y -1,-2,-3 -> -1,-2,-3
    # y -4,-5,-6 ->  -3,-4,-5
    def contains_7x6(self, x, y) -> bool:
        if x > 3:
            x -= 1
        if x < -3:
            x += 1
        if y > 2:
            y -= 1
        if y < -3:
            y += 1
        return self._rows[y][x]

    def to_json(self):
        return [[x for x in row] for row in self._rows]