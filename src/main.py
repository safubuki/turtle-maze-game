import turtle

from maze import Maze

# ウィンドウの設定
window = turtle.Screen()
window.title("Turtle Maze Game")
window.bgcolor("white")
window.setup(width=600, height=600)

# 迷路の生成と描画
maze = Maze()
maze.draw_maze()

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


# 亀の移動関数：Maze.move_turtle()を活用して有効な移動か確認
def move_up():
    player.setheading(90)
    new_x, new_y = maze.move_turtle(player.xcor(), player.ycor(), "up")
    player.goto(new_x, new_y)


def move_down():
    player.setheading(270)
    new_x, new_y = maze.move_turtle(player.xcor(), player.ycor(), "down")
    player.goto(new_x, new_y)


def move_left():
    player.setheading(180)
    new_x, new_y = maze.move_turtle(player.xcor(), player.ycor(), "left")
    player.goto(new_x, new_y)


def move_right():
    player.setheading(0)
    new_x, new_y = maze.move_turtle(player.xcor(), player.ycor(), "right")
    player.goto(new_x, new_y)


# キーイベントの設定
window.listen()
window.onkey(move_up, "Up")
window.onkey(move_down, "Down")
window.onkey(move_left, "Left")
window.onkey(move_right, "Right")

# メインループ
turtle.mainloop()
