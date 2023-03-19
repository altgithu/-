from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import(BLUR,SHARPEN)
from PyQt5.QtWidgets import (
    QApplication,QWidget,
    QFileDialog,
    QLabel,QPushButton,QListWidget,
    QHBoxLayout,QVBoxLayout
)
import os

app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')

btn_dir = QPushButton('Папка')
lw_files = QListWidget()

lb_image = QLabel('Картинка')

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')

main = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(lw_files)

col2.addWidget(lb_image, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

main.addLayout(col1, 20)
main.addLayout(col2, 80)
win.setLayout(main)
workdir = ' '

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filename = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for i in filename:
        lw_files.addItem(i)

from PyQt5.QtGui import QPixmap
class ImageProcessor():
    def __init__ (self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'
    def loading (self,filename):
        self.filename = filename
        fullname = os.path.join(workdir,filename)
        self.image = Image.open(fullname)
    def showIng(self,path):
        lb_image.hide()
        pixmap_img = QPixmap(path)
        w = lb_image.width()
        h = lb_image.height()
        pixmap_img = pixmap_img.scaled(w,h)
        lb_image.setPixmap(pixmap_img)
        lb_image.show()
    def saveImg(self):
        path = os.path.join(workdir,self.save_dir)
        if not (os.path.exists(path)) or os.path.isdir(path):
            os.mkdir(path)
        fullname = os.path.join(path,self.filename)
    def do_wb(self):
        self.image = self.image.convert('L')
        self.saveImg()
        img_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImg(img_path)



work_img = ImageProcessor()
def showChosenImg():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        work_img.loading(filename)
        work_img.showIng(os.path.join(workdir,filename))
lw_files.currentRowChanged.connect(showChosenImg)

btn_bw.clicked.connect(work_img.do_wb)

win.show()
btn_dir.clicked.connect(showFilenamesList)
app.exec()

