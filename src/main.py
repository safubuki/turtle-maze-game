import turtle
from tkinter import Button, Label, Toplevel

from maze import Maze

# ウィンドウの設定
window = turtle.Screen()
window.title("Turtle Maze Game")
window.bgcolor("white")
window.setup(width=600, height=600)

# 迷路の生成と描画
maze = Maze()
maze.draw_maze()

# ゴール位置の計算（迷路の右下の通路セルをゴールとする）
goal_col = maze.cols - 2
goal_row = maze.rows - 2
goal_x = maze.origin_x + goal_col * maze.cell_size + maze.cell_size // 2
goal_y = maze.origin_y + goal_row * maze.cell_size + maze.cell_size // 2

# デバッグ用のプリント表示
print(f"Goal position: ({goal_x}, {goal_y})")

# ゴールマーカーの描画
goal_marker = turtle.Turtle()
goal_marker.hideturtle()
goal_marker.penup()
goal_marker.goto(goal_x, goal_y)
goal_marker.color("red")
goal_marker.write("G", align="center", font=("Arial", 16, "bold"))

# 亀（プレイヤー）の設定
player = turtle.Turtle()
player.shape("turtle")
player.color("green")
player.penup()
player.speed(0)
# 迷路の開始位置(通路セルであるmaze[1][1]に合わせる)
start_x = maze.origin_x + maze.cell_size + maze.cell_size // 2
start_y = maze.origin_y + maze.cell_size + maze.cell_size // 2
player.goto(start_x, start_y)


# ゴール判定とポップアップ表示
def check_goal():
    # プレイヤーの位置がゴールに近いか判定（誤差を考慮）
    if abs(player.xcor() - goal_x) < maze.cell_size / 2 and abs(player.ycor() -
                                                                goal_y) < maze.cell_size / 2:
        show_congratulations()


def finish_game():
    turtle.bye()


def show_congratulations():
    """
    ゴールに到着した際に表示するポップアップを生成します。
    ポップアップは画面中央に配置され、「Congratulations」と表示、
    Finishボタンでプログラムを終了できます。
    """
    # 既にポップアップが出ている場合は再度表示しない
    if hasattr(show_congratulations, "popup_shown") and show_congratulations.popup_shown:
        return
    show_congratulations.popup_shown = True

    # turtleウィンドウからTkのトップレベルウィンドウを取得
    canvas = turtle.getcanvas()
    root = canvas.winfo_toplevel()

    popup = Toplevel(root)
    popup.title("Congratulations")
    popup.geometry("250x100")
    popup.update_idletasks()  # サイズ情報を更新

    # ポップアップを画面中央に配置する計算
    w = popup.winfo_width()
    h = popup.winfo_height()
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width - w) // 2
    y = (screen_height - h) // 2

    popup.geometry(f"250x100+{x}+{y}")

    Label(popup, text="Congratulations!", font=("Arial", 14)).pack(pady=10)
    Button(popup, text="Finish", command=finish_game).pack(pady=5)


# 亀の移動関数：Maze.move_turtle()を活用して有効な移動か確認
def move_up():
    player.setheading(90)
    new_x, new_y = maze.move_turtle(player.xcor(), player.ycor(), "up")
    player.goto(new_x, new_y)
    check_goal()


def move_down():
    player.setheading(270)
    new_x, new_y = maze.move_turtle(player.xcor(), player.ycor(), "down")
    player.goto(new_x, new_y)
    check_goal()


def move_left():
    player.setheading(180)
    new_x, new_y = maze.move_turtle(player.xcor(), player.ycor(), "left")
    player.goto(new_x, new_y)
    check_goal()


def move_right():
    player.setheading(0)
    new_x, new_y = maze.move_turtle(player.xcor(), player.ycor(), "right")
    player.goto(new_x, new_y)
    check_goal()


# キーイベントの設定
window.listen()
window.onkey(move_up, "Up")
window.onkey(move_down, "Down")
window.onkey(move_left, "Left")
window.onkey(move_right, "Right")

# メインループ
turtle.mainloop()
