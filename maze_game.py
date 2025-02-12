import os
import random
import time
from datetime import datetime
from collections import deque
import subprocess
import sys


def set_difficulty():
    """難易度を設定し、迷路のサイズと制限時間を設定"""
    global TIME_LIMIT

    print("難易度を設定するわね")    
        
    while True:
        try:
            difficulty = int(input("1:[かんたん] , 2:[ふつ～] , 3:[むずかし～]、この中から数字で選択して"))
            if difficulty == 1:
                return 11, 11, 30
            elif difficulty == 2:
                return 21, 21, 90
            elif difficulty == 3:
                return 29, 29, 120
            else:
                print("1～3の間で選ばないといけないんだからね！")
        except ValueError:
            print("数字を入力してほしいのだけど・・・。")

def display_maze(maze, playerX, playerY):    
    
    rows = len(maze)#行数
    cols = len(maze[0])#列数

    for y in range(rows):
        row_string = ""  # ✅ 各行ごとにリセットする
        for x in range(cols):
            if y == playerY and x == playerX:
                row_string += "〇"
            elif maze[y][x] == 1:
                row_string += "■"
            elif maze[y][x] == 0:
                row_string += "　"
            elif maze[y][x] == 2:
                row_string += "ほ"
            elif maze[y][x] == 3:
                row_string += "☆"
        print(row_string)  # 行ごとにprint()することでズレを防ぐ

def generate_maze(maze, y, x, rows, cols):
    directions = [(0, -2),(0, 2), (-2, 0), (2, 0)]
    random.shuffle(directions)

    for dy, dx in directions:
        ny, nx = y + dy, x + dx

        #範囲内かつ、2マス先が壁なら掘る
        if 1 <= ny < rows - 1 and 1<= nx < cols - 1 and maze[ny][nx] == 1:
            maze[ny][nx] = 0  #2マス先を通路にする
            maze[y + dy//2][x + dx//2] = 0  #間の壁も壊す
            generate_maze(maze, ny, nx, rows, cols) #再帰的に迷路を掘る

def create_maze(rows, cols):
    maze = [[1] * cols for _ in range(rows)]
    maze[1][1] = 0  #スタート地点

    #迷路生成
    generate_maze(maze, 1 ,1, rows, cols)
    return maze

def generate_goal_point(maze, rows, cols):
    while(1):
        goalY = random.randrange(1, rows - 1, 2)
        goalX = random.randrange(1, cols - 1, 2)

        if maze[goalY][goalX] == 0:
            maze[goalY][goalX] = 2
            return goalY, goalX

def move_player(maze, move, playerX, playerY):
    if move == "w" and maze[playerY - 1][playerX] != 1:
        playerY -= 1
    elif move == "a" and maze[playerY][playerX - 1] != 1:
        playerX -= 1
    elif move == "d" and maze[playerY][playerX + 1] != 1:
        playerX += 1
    elif move == "s" and maze[playerY + 1][playerX] != 1:
        playerY += 1            
    return playerY, playerX

def find_path_bfs(maze, playerY, playerX, goalY, goalX):
    """BFSでスタートからゴールへの最短経路を探索し、経路をヒント（☆）で表示する"""
    startY, startX = playerY, playerX
    rows, cols = len(maze), len(maze[0])
    queue = deque([(goalY, goalX)]) #探索リスト
    prev = {}  #何処から来たかを記録

    #4方向(上、下、左、右)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    #訪問済みの座標を記録
    visited = set()
    visited.add((goalY, goalX))

    while queue:
        y, x = queue.popleft()#キューの先頭を取得

        if(y, x) == (startY, startX): # 🔹 ゴールに到達したら探索終了
            break

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            
            if 0 <= ny < rows and 0 <= nx < cols and (ny, nx) not in visited and maze[ny][nx] != 1:
                queue.append((ny, nx))#次の探索候補に追加
                visited.add((ny, nx))
                prev[(ny, nx)] = (y, x)#何処から来たか記憶

    #  経路復元（ゴールからスタートまで逆順にたどる）
    path = []
    current = (startY, startX)

    while current in prev:
        path.append(current)
        current = prev[current]

    path = path[::-1]  # ゴール → プレイヤー の順番を逆転しておく

    #経路をヒントとして☆に変える
    for y, x in path[:-1]:
        maze[y][x] = 3
        
    display_maze(maze, playerX, playerY)  # ヒントを含めた迷路を表示
    time.sleep(5)  # 5秒待つ
    # ヒントを消して迷路を再描画
    for y, x in path[:-1]:
        maze[y][x] = 0
    clear_screen()  # 画面をクリア
    display_maze(maze, playerX, playerY)  # 通常の迷路を再表示

    maze[goalY][goalX] = 2
def clear_screen():
    print("\n" * 50)

playerY, playerX = 1,1
rows, cols ,TIME_LIMIT = set_difficulty()
maze = create_maze(rows, cols)
goalY, goalX = generate_goal_point(maze, rows, cols)
start_time = time.time() #現在の日時の取得

while True:
    elapsed_time = time.time() - start_time   # float - float なのでOK  # 経過時間を取得
    
    clear_screen()  
    print(f"経過時間: {elapsed_time:.1f}秒")
    display_maze(maze, playerX, playerY)
    move = input("Move(WASDH):").lower()
    if move in ["w", "a", "s", "d"]:
        playerY, playerX = move_player(maze, move,playerX, playerY)
    elif move == "h":
        find_path_bfs(maze, playerY, playerX, goalY, goalX)

    if elapsed_time >= TIME_LIMIT:
        print("時間切れよ・・・また挑戦してね")
        break
    
    
    if maze[playerY][playerX] == 2:
        print("ゲームクリア！おめでとう！")
        break

