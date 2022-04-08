import tkinter as tk
import random

class CatGame:
    def __init__(self):
        self.root = tk.Tk()
        self.step = 0           # 流程
        self.timer = 0          # 時間
        self.score = 0          # 分數
        self.cat = 0            # 下一個貓咪變數
        self.cursor_x = 0       # 水平位置
        self.cursor_y = 0       # 垂直位置
        self.mouse_x = 0        # 滑鼠游標的 X 座標
        self.mouse_y = 0        # 滑鼠游標的 Y 座標
        self.mouse_click = 0    # 按鍵點擊狀態
        self.neko = []          # 貓咪矩陣
        self.check = []         # 確認矩陣
        for i in range(10):
            self.neko.append([0,0,0,0,0,0,0,0,0,0])
            self.check.append([0,0,0,0,0,0,0,0,0,0])

        self.canvas = tk.Canvas(self.root, width=912, height=768)
        self.canvas.pack()
        self.background = tk.PhotoImage(file="picture/neko_bg.png")
        self.cursor = tk.PhotoImage(file="picture/neko_cursor.png")
        self.img_neko = [None,
                        tk.PhotoImage(file="picture/neko1.png"),
                        tk.PhotoImage(file="picture/neko2.png"),
                        tk.PhotoImage(file="picture/neko3.png"),
                        tk.PhotoImage(file="picture/neko4.png"),
                        tk.PhotoImage(file="picture/neko5.png"),
                        tk.PhotoImage(file="picture/neko6.png"),
                        tk.PhotoImage(file="picture/neko_niku.png")]

    # 遊戲主程式
    def game_main(self):
        # step1 處理標題
        if self.step == 0:
            self.draw_txt("貓咪貓咪", 312, 240, 100, "violet", "TITLE")
            self.draw_txt("Click to start.", 312, 560, 50, "orange", "TITLE")
            for y in range(10):
                for x in range(10):
                    self.neko[y][x] = 0
            self.draw_neko()
            self.canvas.delete("CURSOR")
            self.score = 0
            self.step = 1
            self.mouse_click = 0
            
        # step2 處理按下滑鼠按鍵
        elif self.step == 1:
            if self.mouse_click ==1:
                for y in range(10):
                    for x in range(8):
                        self.neko[y][x] = 0
                self.mouse_click = 0
                self.score = 0
                self.cat = 0
                self.cursor_x = 0
                self.cursor_y = 0
                self.set_neko()
                self.draw_neko()
                self.canvas.delete("TITLE")      # 消除標題
                self.step = 2

        # step3 處理貓咪方塊落下
        elif self.step == 2:        
            if self.drop_neko() == True:
                self.step = 3
            self.draw_neko()
            
        # step4 處理是否連線
        elif self.step == 3:
            self.check_neko()
            self.draw_neko()
            self.step = 4

        # step5 消除連成一線的貓咪方塊
        elif self.step == 4:        
            sc = self.sweep_neko()
            self.score += sc*10
            if sc > 0:
                self.step = 2
            else:                    # 如果遊戲尚未結束, 隨機配置下一群落下的貓咪方塊
                if self.over_neko() == False:
                    self.cat = random.randint(1, 6)
                    self.step = 5
                else:
                    self.step = 6
                    self.timer = 0
            self.draw_neko()
        
        # step6 滑鼠點擊配置貓咪方塊
        elif self.step == 5:
            if 24 <= self.mouse_x and self.mouse_x < 24+72*8 and 24 <= self.mouse_y and self.mouse_y < 24+72*10:
                self.cursor_x = int((self.mouse_x-24)/72)
                self.cursor_y = int((self.mouse_y-24)/72)
                if self.mouse_click == 1:       # 當滑鼠被點擊時,顯示出1
                    self.mouse_click = 0
                    self.set_neko()
                    self.neko[self.cursor_y][self.cursor_x] = self.cat      # 在滑鼠的位置, 隨機產生一個貓咪方塊
                    self.cat = 0
                    self.step = 2
            self.canvas.delete("CURSOR")
            self.canvas.create_image(self.cursor_x*72+60, self.cursor_y*72+60, image=self.cursor, tag="CURSOR")
            self.draw_neko()

        # step7 遊戲結束
        elif self.step == 6:      
            self.timer += 1
            if self.timer == 1:
                self.draw_txt("GAME OVER", 312, 348, 68, "red", "OVER")      # GAME OVER
            if self.timer == 50:
                self.canvas.delete("OVER")
                self.step = 0
        self.canvas.delete("INFO")
        self.draw_txt("SCORE " + str(self.score), 160, 60, 32, "blue", "INFO")      # 分數顯示
        if self.cat > 0:      
            self.canvas.create_image(752, 128, image=self.img_neko[self.cat], tag="INFO")      # 跑出方塊
        self.root.after(100, self.game_main)

    # 開始遊戲
    def run(self):
        self.root.title("掉落物拼圖")
        self.root.resizable(False, False)
        self.root.bind("<Motion>", self.mouse_Move)
        self.root.bind("<ButtonPress>", self.mouse_Click)
        self.canvas.create_image(456, 384, image=self.background)
        self.game_main()
        self.root.mainloop()


    def mouse_Move(self, m):
        self.mouse_x = m.x      #滑鼠座標 X 座標
        self.mouse_y = m.y      #滑鼠座標Y 座標
    
   
    def mouse_Click(self, c):
        self.mouse_click = 1      # 點擊變成1 

    # 計算消除連線貓咪方塊數量
    def sweep_neko(self):
        num = 0
        for y in range(10):
            for x in range(8):
                if self.neko[y][x] == 7:
                    self.neko[y][x] = 0
                    num += 1
        return num

    # 最上層設定隨機落下貓咪方塊數量  
    def set_neko(self):
        for x in range(8):
            self.neko[0][x] = random.randint(0, 6)

  
    def draw_txt(self, txt, x, y, siz, col, tg):
        fnt = ("Times New Roman", siz, "bold")
        self.canvas.create_text(x+2, y+2, text=txt, fill="black", font=fnt, tag=tg)
        self.canvas.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)

    # 貓咪方塊圖片   
    def draw_neko(self):
        self.canvas.delete("NEKO")
        for y in range(10): 
            for x in range(8):
                if self.neko[y][x] > 0:       # 如果neko陣列中大於 0, 顯示對應的貓咪圖片
                    self.canvas.create_image(x*72+60, y*72+60, image=self.img_neko[self.neko[y][x]], tag="NEKO")      # (x*72+60, y*72+60) 代表指定了格子中心點的座標 !




#========================================================= Question 1 =========================================================
    # 題目說明：
    # 判斷同色貓咪方塊是否至少有3塊連成一線(上下/左右/斜角)，不需回傳值(return)，只需要把符合條件的 self.neko 內的內容修改掉即可
    def check_neko(self):
        for y in range(10):
            for x in range(8):
                self.check[y][x] = self.neko[y][x]

      
        for y in range(1, 9): 
            for x in range(8):
                if self.check[y][x] > 0:
                    if self.check[y-1][x] == self.check[y][x] and self.check[y+1][x] == self.check[y][x]:
                        self.neko[y-1][x] = 7
                        self.neko[y][x] = 7
                        self.neko[y+1][x] = 7 # 該位置換成肉球圖片顯示，代表相連後被消去


        
   

        # 判斷左右是否連線
        # <<<將你的程式寫在這邊>>>
        for x in range(1,7): 
            for y in range(10):
                if self.check[y][x] > 0:#假如不是空的凱使跑回圈
                    if self.check[y][x-1] == self.check[y][x] and self.check[y][x+1] == self.check[y][x]: #檢查是否左右相同
                        self.neko[y][x-1] = 7
                        self.neko[y][x] = 7
                        self.neko[y][x+1] = 7 # 此處 7 的意思是把此位置換成肉球圖片顯示，代表相連後被消去

        # 3.判斷斜角是否連線
        # <<<將你的程式寫在這邊>>>
        for y in range(1,9): 
            for x in range(1,7):
                if self.check[y][x] > 0:
                    if self.check[y-1][x-1] == self.check[y][x] and self.check[y+1][x+1] == self.check[y][x]:#檢查是否右下到左上相同
                        self.neko[y-1][x-1] = 7
                        self.neko[y][x] = 7
                        self.neko[y+1][x+1] = 7 # 此處 7 的意思是把此位置換成肉球圖片顯示，代表相連後被消去

                    elif self.check[y-1][x+1] == self.check[y][x] and self.check[y+1][x-1] == self.check[y][x]:#檢查是否左下到右上相同
                        self.neko[y-1][x+1] = 7
                        self.neko[y][x] = 7
                        self.neko[y+1][x-1] = 7 # 此處 7 的意思是把此位置換成肉球圖片顯示，代表相連後被消去

#========================================================= Question 2 =========================================================
    # 題目說明(此題有兩項要求)：
    # 讓貓咪方塊下落，需要判斷落下的貓咪方塊下方是否有已存在的貓咪方塊，若有則停止落下，若無則繼續往下一格落下。
    # 方塊必須一格一格落下，全部方塊落下完畢後，要回傳(return) True，告知 game_main() 要往下個step前進了。
    # 最理想的情況是能讓程式一格一格顯示下落的方塊，並讓方塊正確下落堆疊。
    def drop_neko(self):
        # hint : 此方法需要回傳值(return)，型態為布林值(bool : True, False)
        # <<<將你的程式寫在這邊>>>
        dropch=True #先假設回傳是true
        for y in range(9):
            for x in range(8):
                if self.neko[y][x]>0 and self.neko[y+1][x]==0:#假如要往下掉有東西，且下一個是空的
                    self.neko[y+1][x]=self.neko[y][x]#往下掉
                    self.neko[y][x]=0#原本的清空
                    dropch=False #還沒跑完所以是false
        


        return dropch #跑完了return True

#========================================================= Question 3 =========================================================
    # 題目說明：
    # 1.判斷貓咪方塊是否碰到到最上層，是則回傳 True，否則回傳 False。
    def over_neko(self):
        y=0
        check=False #假設一開始是false
        for x in range(8):
            if self.neko[y][x] > 0:
                check=True
                break  #245-248開始偵測偵測到碰到最上面 check變成True，且停止迴圈

        return check
        # hint : 此方法需要回傳值(return)，型態為布林值(bool : True, False)
        # <<<將你的程式寫在這邊>>>

#==============================================================================================================================
newgame = CatGame()
newgame.run()