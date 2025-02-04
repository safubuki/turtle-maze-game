import random
import turtle

CELL_SIZE = 20


def generate_maze(width, height):
    """
    指定された通路セルの数(width, height)に基づいて迷路を生成する。
    迷路は深さ優先探索を用いて生成され、1が壁、0が通路を表す。
    なお、内部的な全体セル数はそれぞれ2 * セル数 + 1となる。

    引数:
        width (int): 通路セルの数（横方向）
        height (int): 通路セルの数（縦方向）

    戻り値:
        list: 2次元リスト形式の迷路データ
    """
    maze_rows = 2 * height + 1  # 迷路の全体の行数（壁と通路含む）
    maze_cols = 2 * width + 1  # 迷路の全体の列数（壁と通路含む）
    # すべてのセルを初期状態で壁(1)に設定
    maze = [[1 for _ in range(maze_cols)] for _ in range(maze_rows)]

    def carve(x, y):
        """
        深さ優先探索を用いて迷路内の通路を生成する再帰処理。
        
        引数:
            x (int): 現在のセルのx座標（列、通路セル位置）
            y (int): 現在のセルのy座標（行、通路セル位置）
        """
        maze[y][x] = 0  # 現在のセルを通路(0)に設定
        # 壁を飛ばして上下左右の2セル先へ移動するための方向リスト
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # 新たに訪問するセルが範囲内でまだ壁の場合
            if 0 < nx < maze_cols and 0 < ny < maze_rows and maze[ny][nx] == 1:
                # 現在のセルと新セルの中間の壁を通路に変更
                maze[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)

    carve(1, 1)
    return maze


class Maze:
    """
    迷路クラス。
    ユーザーが直感的な全体セル数を指定できるように改善しており、
    内部ではこれを通路セル数に変換して迷路を生成、描画および移動判定を行う。
    """

    def __init__(self, grid_width=21, grid_height=21):
        """
        Mazeクラスのコンストラクタ。
        
        引数:
            grid_width (int): 迷路の全体の列数（壁と通路を含む、奇数推奨、デフォルト21）
            grid_height (int): 迷路の全体の行数（壁と通路を含む、奇数推奨、デフォルト21）
        """
        # 外周は必ず壁とするため、実際の通路セル数は (全体セル数 - 1) // 2 となる
        width = (grid_width - 1) // 2
        height = (grid_height - 1) // 2

        self.width = width  # 通路セルの数（横方向）
        self.height = height  # 通路セルの数（縦方向）
        self.maze = generate_maze(width, height)
        self.cell_size = CELL_SIZE
        self.rows = len(self.maze)  # 全体行数（壁と通路含む）
        self.cols = len(self.maze[0])  # 全体列数（壁と通路含む）
        # 迷路全体を画面中央に描画するための原点計算
        self.origin_x = -(self.cols * self.cell_size) / 2
        self.origin_y = -(self.rows * self.cell_size) / 2

        # デバッグ用に各プロパティを表示
        print(f"Grid Width (全体セル): {grid_width}")
        print(f"Grid Height (全体セル): {grid_height}")
        print(f"Path Width (通路セル): {self.width}")
        print(f"Path Height (通路セル): {self.height}")
        print(f"Cell Size: {self.cell_size}")
        print(f"Rows (全体行数): {self.rows}")
        print(f"Cols (全体列数): {self.cols}")
        print(f"Origin X: {self.origin_x}")
        print(f"Origin Y: {self.origin_y}")
        print("Maze:")
        for row in self.maze:
            print(row)

    def draw_maze(self):
        """
        タートルを使用して迷路の壁を描画する。
        高速描画のためにトレーサーの更新を一時停止し、一括で画面を更新する。
        """
        turtle.tracer(0, 0)
        drawer = turtle.Turtle()
        drawer.hideturtle()
        drawer.speed(0)
        drawer.penup()

        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == 1:
                    x = self.origin_x + col * self.cell_size
                    y = self.origin_y + row * self.cell_size
                    drawer.goto(x, y)
                    drawer.pendown()
                    for _ in range(4):
                        drawer.forward(self.cell_size)
                        drawer.left(90)
                    drawer.penup()

        turtle.update()
        turtle.tracer(1, 10)

    def is_move_valid(self, x, y):
        """
        指定された座標(x, y)が迷路内の通路かどうかを判定する。

        引数:
            x (float): タートルのx座標
            y (float): タートルのy座標
        
        戻り値:
            bool: 有効な通路であればTrue、そうでなければFalse
        """
        col = int((x - self.origin_x) / self.cell_size)
        row = int((y - self.origin_y) / self.cell_size)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.maze[row][col] == 0
        return False

    def move_turtle(self, current_x, current_y, direction):
        """
        タートルの移動処理。指定された方向への移動先が通路であれば新しい座標を返す。
        移動が無効な場合は元の座標を返す。

        引数:
            current_x (float): 現在のx座標
            current_y (float): 現在のy座標
            direction (str): 移動方向 ("up", "down", "left", "right")
        
        戻り値:
            tuple: (新しいx座標, 新しいy座標)
        """
        new_x, new_y = current_x, current_y
        if direction == "up":
            new_y += self.cell_size
        elif direction == "down":
            new_y -= self.cell_size
        elif direction == "left":
            new_x -= self.cell_size
        elif direction == "right":
            new_x += self.cell_size

        print(f"Current position: ({current_x}, {current_y}), New position: ({new_x}, {new_y})")
        if self.is_move_valid(new_x, new_y):
            return new_x, new_y
        return current_x, current_y
