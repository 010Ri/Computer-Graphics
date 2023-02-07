# THIS IS THE PROGRAM FOR COMPUTER GRAPHICS.
# AUTHOR : YAMANAKA

import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, image_names, ttk, messagebox
import os

# === Computer Graphics Class ===============================================================
class ComputerGraphics():
        # グレースケール画像に変換する関数
        def Gray(self, img, name):
                fname = 'gray_' + name
                gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                return fname, gray_img

        # グレースケール画像を二値化する関数
        def Bin(self, gray_img, name, thresh, max, mode):
                fname = 'bin_' + name
                if mode == 0:
                        ret, bin_img = cv2.threshold(gray_img, thresh, max, cv2.THRESH_OTSU)
                elif mode == 1:
                        ret, bin_img = cv2.threshold(gray_img, thresh, max, cv2.THRESH_BINARY)
                elif mode == 2:
                        ret, bin_img = cv2.threshold(gray_img, thresh, max, cv2.THRESH_BINARY_INV)
                else:
                        print('please select mode')
                return fname, bin_img
        
        # 画像の輪郭抽出を行う関数
        def Edge(self, got_img, bin_img, name):
                fname = 'edge_' + name
                contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                edge_img = cv2.drawContours(got_img, contours, -1, (0, 255, 0), 5, 8)
                return fname, edge_img
        
        # filter2Dのカーネルによる画像の平滑化
        def Kernel_Smoothing(self, got_img, name, m):
                fname = 'ksmooth_' + name
                kernel = np.ones((m, m), np.float32) / (m * m)
                ksmooth_img = cv2.filter2D(got_img, -1, kernel)
                return fname, ksmooth_img

        # filter2Dのカーネルによる画像の鮮鋭化
        def Kernel_Sharpening(self, got_img, name, r, c):
                fname = 'ksharp_' + name
                kernel = np.array([[r, r, r], [r, c, r], [r, r, r]], np.float32)
                ksharp_img = cv2.filter2D(got_img, -1, kernel)
                return fname, ksharp_img

        # GaussianBlur関数による画像の平滑化
        def Gau(self, got_img, name, m):
                fname = 'Gaussian_' + name
                gau_img = cv2.GaussianBlur(got_img, (m, m), 0)
                return fname, gau_img

        # bilateralFilter関数による画像のエッジが劣化しない平滑化
        def bil(self, got_img, name, d, s):
                fname = 'bilateral_' + name
                bil_img = cv2.bilateralFilter(got_img, d, s, 20)
                return fname, bil_img

        # Canny関数によるエッジの検出
        def Can(self, got_img, name, t1, t2):
                fname = 'Canny_' + name
                can_img = cv2.Canny(got_img, t1, t2)
                return fname, can_img

        # Laplacian関数による輪郭検出
        def Lap(self, got_img, name, k):
                fname = 'Laplacian_' + name
                lap_img = cv2.Laplacian(got_img, cv2.CV_32F, k)
                return fname, lap_img

        # マスキングをする関数
        def mask(self, got_img, bin_img, name):
                fname = 'masked_' + name
                mask_img = cv2.bitwise_not(bin_img)
                mask_rgb = cv2.cvtColor(mask_img, cv2.COLOR_GRAY2RGB)
                masked_img = cv2.bitwise_and(got_img, mask_rgb)
                return fname, masked_img

# ============================================================================================

# === Functions for GUI action =============================================================
# ファイル参照ボタンを押したときに実行する関数
def file_select():
        dir = '/path/to/your/directory'  # 初期参照フォルダ
        extension = [("すべて", "*"), ("PNG","*.png")]  # select file extension
        file_path = tk.filedialog.askopenfilename(filetypes= extension, initialdir= dir)  # get file path
        file_name = os.path.basename(file_path)  # get file name
        ref_box.delete(0, tk.END)  # 入力ボックスの初期化（空白にする）
        ref_box.insert(tk.END, file_name)  # show file name（入力ボックスにファイル名を入力）
        preview(file_name)

# プレビュー画像をキャンバスに表示する関数
def preview(img_path):
        global preview_img
        preview_img = tk.PhotoImage(file= img_path)
        canvas.create_image(200, 150, image= preview_img)

# 注意書きを表示する関数
def rad_clicked():
        t = var.get()
        if t == 0:  # グレースケール
                caution_label = tk.Label(text= "※ 詳細設定なし　　　　　　　　　　　　　　　　　　")
                caution_label.grid(row= 0, column= 2, sticky= 'w', padx= 80, pady= 5)  
        elif t == 1:  # 二値化
                caution_label = tk.Label(text= "※ しきい値を設定　　　　　　　　　　　　　　　　　")
                caution_label.grid(row= 0, column= 2, sticky= 'w', padx= 80, pady= 5)  
        elif t == 2:  # 輪郭抽出
                caution_label = tk.Label(text= "※ しきい値＆モードを設定　　　　　　　　　　　　　")
                caution_label.grid(row= 0, column= 2, sticky= 'w', padx= 80, pady= 5)  
        elif t == 3:  # カーネルによる平滑化
                caution_label = tk.Label(text= "※ 引数1=カーネルの縦＆横幅　　　　　　　　　　　　")
                caution_label.grid(row= 0, column= 2, sticky= 'w', padx= 80, pady= 5)  
        elif t == 4:  # カーネルによる鮮鋭化
                caution_label = tk.Label(text= "※ 引数1=まわり, 引数2=中心　　　　　　　　　　　　")
                caution_label.grid(row= 0, column= 2, sticky= 'w', padx= 80, pady= 5)  
        elif t == 5:  # GaussianBlur
                caution_label = tk.Label(text= "※ 引数1=カーネルの縦＆横幅, 引数2=標準偏差σ　　　")
                caution_label.grid(row= 0, column= 2, sticky= 'w', padx= 80, pady= 5)  
        elif t == 6:  # bilateralFilter
                caution_label = tk.Label(text= "※ 引数1=ぼかす領域, 引数2=色についての標準偏差σ　")
                caution_label.grid(row= 0, column= 2, sticky= 'w', padx= 80, pady= 5)  
        elif t == 7:  # Canny
                caution_label = tk.Label(text= "※ 引数1=しきい値1, 引数2=しきい値2　　　　　　　")
                caution_label.grid(row= 0, column= 2, sticky= 'w', padx= 80, pady= 5)  
        elif t == 8:  # Laplacian
                caution_label = tk.Label(text= "※ 引数1=カーネルサイズ　　　　　　　　　　　　　")
                caution_label.grid(row= 0, column= 2, sticky= 'w', padx= 80, pady= 5)  
        elif t == 9:  # マスキング
                caution_label = tk.Label(text= "　　　　　　　　　　　　　　　　　　　　　　　　　")
                caution_label.grid(row= 0, column= 2, sticky= 'w', padx= 80, pady= 5)  
        else:
                print('　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　')

# 出力ボタンが押されたときに画像を表示するための関数
def draw():
        img_path = ref_box.get()  # get image file path
        got_img = cv2.imread(img_path)
        # チェックされているラジオボタン番号を取得
        num = var.get()
        if num == 0:  # グレースケール
                fname, gray_img = cgs.Gray(got_img, img_path)
                cv2.imwrite(fname, gray_img)
                preview(fname)

        elif num == 1:  # 二値化
                thresh = thresh_scale.get()
                mode = var2.get()
                fname, gray_img = cgs.Gray(got_img, img_path)
                fname, bin_img = cgs.Bin(gray_img, img_path, thresh, 255, mode)
                cv2.imwrite(fname, bin_img)
                preview(fname)

        elif num == 2:  # 輪郭抽出
                thresh = thresh_scale.get()
                mode = var2.get()
                fname, gray_img = cgs.Gray(got_img, img_path)
                fname, bin_img = cgs.Bin(gray_img, img_path, thresh, 255, mode)
                fname, edge_img = cgs.Edge(got_img, bin_img, img_path)
                cv2.imwrite(fname, edge_img)
                preview(fname)

        elif num == 3:  # カーネルによる平滑化
                arg1 = filter_scale_1.get()
                fname, ksmooth_img = cgs.Kernel_Smoothing(got_img, img_path, arg1)
                cv2.imwrite(fname, ksmooth_img)
                preview(fname)

        elif num == 4:  # カーネルによる鮮鋭化
                arg1 = filter_scale_1.get()
                arg2 = filter_scale_2.get()
                fname, ksharp_img = cgs.Kernel_Sharpening(got_img, img_path, arg1, arg2)
                cv2.imwrite(fname, ksharp_img)
                preview(fname)

        elif num == 5:  # GaussianBlur
                arg1 = filter_scale_1.get()
                fname, gau_img = cgs.Gau(got_img, img_path, arg1)
                cv2.imwrite(fname, gau_img)
                preview(fname)

        elif num == 6:  # bilateral
                arg1 = filter_scale_1.get()
                arg2 = filter_scale_2.get()
                fname, bil_img = cgs.bil(got_img, img_path, arg1, arg2)
                cv2.imwrite(fname, bil_img)
                preview(fname)

        elif num == 7:  # Canny
                arg1 = filter_scale_1.get()
                arg2 = filter_scale_2.get()
                fname, can_img = cgs.Can(got_img, img_path, arg1, arg2)
                cv2.imwrite(fname, can_img)
                preview(fname)

        elif num == 8:  # Laplacian
                arg1 = filter_scale_1.get()
                fname, lap_img = cgs.Lap(got_img, img_path, arg1)
                cv2.imwrite(fname, lap_img)
                preview(fname)

        elif num == 9:  # マスキング
                thresh = thresh_scale.get()
                mode = var2.get()
                fname, gray_img = cgs.Gray(got_img, img_path)
                fname, bin_img = cgs.Bin(gray_img, img_path, thresh, 255, mode)
                fname, masked_img = cgs.mask(got_img, bin_img, img_path)
                cv2.imwrite(fname, masked_img)
                preview(fname)

        else:
                print('please select radiobutton')
# ==============================================================================================

# create instance of ComputerGraphics
cgs = ComputerGraphics()

# === GUI setting ===========================================================================
gui = tk.Tk()  # create instance (create main window)
gui.geometry('950x430')  # set window size
gui.title('コンピュータグラフィックス')  # set title

# ラジオボタンのチェックの有無を確認する変数
var = tk.IntVar()
var.set(0)  # 初期状態のチェック番号
var2 = tk.IntVar()
var2.set(0)

# infoラベルの作成
info_label_1 = tk.Label(text= "1. ファイル選択")
info_label_1.grid(row= 0, column= 0, columnspan= 2 , sticky= 'w', padx= 5, pady= 5)
info_label_2 = tk.Label(text= "2. 処理モード選択")
info_label_2.grid(row= 3, column= 0, sticky= 'w', padx= 5, pady= 5)
info_label_3 = tk.Label(text= "3. 詳細設定")
info_label_3.grid(row= 3, column= 1, sticky= 'w', padx= 5, pady= 5)
info_label_4 = tk.Label(text= "4. 画像プレビュー")
info_label_4.grid(row= 3, column= 2, sticky= 'w', padx= 80, pady= 5)

# 参照先のファイル名の入力欄の作成
ref_box = tk.Entry(width= 50)
ref_box.grid(row= 1, column= 0, sticky= 'w', padx= 5, pady= 5)

# 参照ボタンの作成
ref_button = tk.Button(text= "参照", command= file_select)
ref_button.grid(row= 1, column= 1, sticky= 'w', padx= 5, pady= 5)

# ラジオボタン作成
rad1 = tk.Radiobutton(gui, value= 0, variable= var, text= 'グレースケール', command= rad_clicked)
rad1.grid(row= 4, column= 0, sticky= 'w', padx= 5)
rad2 = tk.Radiobutton(gui, value= 1, variable= var, text= '二値化', command= rad_clicked)
rad2.grid(row= 5, column= 0, sticky= 'w', padx= 5)
rad3 = tk.Radiobutton(gui, value= 2, variable= var, text= '輪郭検出', command= rad_clicked)
rad3.grid(row= 6, column= 0, sticky= 'w', padx= 5)
rad4 = tk.Radiobutton(gui, value= 3, variable= var, text= 'カーネル（平滑化）', command= rad_clicked)
rad4.grid(row= 7, column= 0, sticky= 'w', padx= 5)
rad5 = tk.Radiobutton(gui, value= 4, variable= var, text= 'カーネル（鮮鋭化）', command= rad_clicked)
rad5.grid(row= 8, column= 0, sticky= 'w', padx= 5)
rad6 = tk.Radiobutton(gui, value= 5, variable= var, text= 'GaussianBlur', command= rad_clicked)
rad6.grid(row= 9, column= 0, sticky= 'w', padx= 5)
rad7 = tk.Radiobutton(gui, value= 6, variable= var, text= 'bilateralFilter', command= rad_clicked)
rad7.grid(row= 10, column= 0, sticky= 'w', padx= 5)
rad8 = tk.Radiobutton(gui, value= 7, variable= var, text= 'Canny', command= rad_clicked)
rad8.grid(row= 11, column= 0, sticky= 'w', padx= 5)
rad9 = tk.Radiobutton(gui, value= 8, variable= var, text= 'Laplacian', command= rad_clicked)
rad9.grid(row= 12, column= 0, sticky= 'w', padx= 5)
rad10 = tk.Radiobutton(gui, value= 9, variable= var, text= 'マスク', command= rad_clicked)
rad10.grid(row= 13, column= 0, sticky= 'w', padx= 5)

# 二値化のモード選択用ラジオボタンの作成
bin_label = tk.Label(text= "▷ モード選択")
bin_label.grid(row= 4, column= 1, sticky= 'w')
bin_rad1 = tk.Radiobutton(gui, value= 0, variable= var2, text= '大津')
bin_rad1.grid(row= 5, column= 1, sticky= 'w', padx= 5)
bin_rad2 = tk.Radiobutton(gui, value= 1, variable= var2, text= 'BINARY')
bin_rad2.grid(row= 6, column= 1, sticky= 'w', padx= 5)
bin_rad3 = tk.Radiobutton(gui, value= 2, variable= var2, text= 'BINARY_INV')
bin_rad3.grid(row= 7, column= 1, sticky= 'w', padx= 5)

# scaleの作成
scale_label_thresh = tk.Label(text= "▷ しきい値")
scale_label_thresh.grid(row= 8, column= 1, sticky= 'w')
thresh_scale = tk.Scale(orient= tk.HORIZONTAL, from_= 0, to= 255)
thresh_scale.grid(row= 9, column= 1, sticky= 'w')
scale_label_filter_1 = tk.Label(text= "▷ フィルター引数1")
scale_label_filter_1.grid(row= 10, column= 1, sticky= 'w')
filter_scale_1 = tk.Scale(orient= tk.HORIZONTAL, from_= -255, to= 255)
filter_scale_1.grid(row= 11, column= 1, sticky= 'w')
scale_label_filter_2 = tk.Label(text= "▷ フィルター引数2")
scale_label_filter_2.grid(row= 12, column= 1, sticky= 'w')
filter_scale_2 = tk.Scale(orient= tk.HORIZONTAL, from_= -255, to= 255)
filter_scale_2.grid(row= 13, column= 1, sticky= 'w')

# canvasの作成
canvas = tk.Canvas(width= 400, height= 300)
canvas.grid(row= 4, column= 2, rowspan= 10, padx= 80, pady= 5)

# 出力ボタン
output_button = tk.Button(text= "画像出力", command= draw)
output_button.grid(row= 1, column= 2, sticky= 'w', padx= 80, pady= 5)

# even if this program is finished, the window never disappears
gui.mainloop()
# ========================================================================================
