import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QUndoStack, QMessageBox, QLabel

from someFunc.lexical.Automata import Lex_analyzer
from someFunc.parser_re.Statement import Match_program_stmt
from ui import Ui_MainWindow
from subui import Ui_rndm


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.windowTitle = "廖语言编译器威力加强无敌版V99.9（国产正版）"
        self.openedFileName = ''
        self.anlsInfo = ''
        self.token_list = None

        self.statusBar.showMessage("就绪")
        self.setWindowTitle(self.windowTitle)

        # TODO
        self.undoStack = QUndoStack()  # 存放命令的栈

        # Other
        self.textEditMain.textChanged.connect(self.change_tips)

        # File
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSaveAs.triggered.connect(self.save_as_file)
        self.actionOpenRecent.setDisabled(True)
        self.actionExit.triggered.connect(self.close)

        # Edit
        self.actionCut.triggered.connect(self.cut_text)
        self.actionCopy.triggered.connect(self.copy_text)
        self.actionPaste.triggered.connect(self.paste_text)

        # LexAnls
        self.actionLexicalAnalyzer.triggered.connect(self.LexAnls)
        self.actionNFA_DFA_MFA.triggered.connect(self.rndm)

        # Parsing
        self.actionParser.triggered.connect(self.parser)

        # Symbol
        self.actionSymbol.triggered.connect(self.update_symbol_sta)

        # Help
        self.actionHelp.triggered.connect(self.open_help)
        self.actionAbout.triggered.connect(self.about_dialog)

    # Other
    def change_tips(self):
        self.setWindowTitle(self.windowTitle + '*')
        self.anlsInfo = "not now"

    # File
    def new_file(self):
        self.textEditMain.clear()
        self.openedFileName = ''
        self.lineEditPath.setText('')

    def open_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "打开文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        self.openedFileName = fileName
        self.lineEditPath.setText(fileName)

        fileContent = open(fileName, 'r').read()
        self.textEditMain.setText(fileContent)
        self.setWindowTitle(self.windowTitle)

    def save_file(self):
        fileName = self.openedFileName
        paths = []
        for item in os.listdir('.'):
            path = (os.getcwd() + '\\' + item).replace('\\', '/')
            paths.append(path)
        if fileName not in paths:
            fileName, filetype = QtWidgets.QFileDialog.getSaveFileName(self, "保存文件", os.getcwd(),
                                                                       "All Files (*);;Text Files (*.txt)")
            if self.openedFileName == '':
                self.lineEditPath.setText(fileName)
        fileContent = self.textEditMain.toPlainText()
        open(fileName, 'w').write(fileContent)
        self.setWindowTitle(self.windowTitle)

    def save_as_file(self):
        fileName, filetype = QtWidgets.QFileDialog.getSaveFileName(self, "保存文件", os.getcwd(),
                                                                   "All Files (*);;Text Files (*.txt)")
        fileContent = self.textEditMain.toPlainText()
        open(fileName, 'w').write(fileContent)

    # Edit
    def cut_text(self):
        self.textEditMain.cut()

    def copy_text(self):
        self.textEditMain.copy()

    def paste_text(self):
        self.textEditMain.paste()

    # LexAnls
    def LexAnls(self):
        content = self.textEditMain.toPlainText()
        # TODO
        lex_anal = Lex_analyzer()
        lex_anal.set_text(content)
        token_list, info_list = lex_anal.get_token_info()
        self.token_list = token_list

        res = ''
        for item in token_list:
            token_str = '{}\t{}\t{}\t{}\t{}'.format(token_list.index(item), item.data, item.type, item.row, item.col)
            res += '{}\n'.format(token_str)
        self.anlsInfo = ''
        for item in info_list:
            self.anlsInfo += '{}\n'.format(item)

        self.textEditRes.clear()
        self.textEditRes.setText(res)
        self.update_symbol_sta()

    def rndm(self):
        my_subWin.show()

    # Parsing
    def parser(self):
        content = self.textEditMain.toPlainText()
        # TODO
        parser_anal = Match_program_stmt()
        parser_anal.set_tokenList(self.token_list)
        res, idx, tree, error_list = parser_anal.run(True)
        res_info = parser_anal.tree.show(stdout=False)

        self.anlsInfo = '{}\n{}'.format(res, error_list)

        self.textEditRes.clear()
        self.textEditRes.setText(res_info)
        self.update_symbol_sta()

    # Symbol
    def update_symbol_sta(self):
        if not self.actionSymbol.isChecked():
            self.textEditInfo.clear()
        else:
            self.textEditInfo.setText(self.anlsInfo)

    # Help
    def open_help(self):
        os.startfile('"help.docx"')

    def about_dialog(self):
        QMessageBox.about(self, "国产正版", "廖语言编译器威力加强无敌版V99.9")


class MySubForm(QMainWindow, Ui_rndm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.view = QGraphicsView(self)
        # self.view.setGeometry(0, 0, 710, 650)
        self.actionStart.clicked.connect(self.start)
        pix = QPixmap('someFunc/re2mdfa/out/nfa.png')
        lb1 = QLabel(self)
        lb1.setGeometry(0, 0, 300, 200)
        lb1.setStyleSheet("border: 2px solid red")
        lb1.setPixmap(pix)

    def start(self):
        content = self.lineEditRe.text()
        # anls(content)
        self.graphicsView_nfa.show('./someFunc/out/nfa.png')
        print('ok')
        # image_path = './someFunc/out/nfa.png'
        # print(image_path)
        # img = cv2.imread(image_path)  # 读取图像
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
        # x = img.shape[1]  # 获取图像大小
        # y = img.shape[0]
        # self.zoomscale = 1  # 图片放缩尺度
        # frame = QImage(img, x, y, QImage.Format_RGB888)
        # pix = QPixmap.fromImage(frame)
        # self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        # self.scene = QGraphicsScene()  # 创建场景
        # self.scene.addItem(self.item)
        # self.view.setScene(self.scene)
        # self.view.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_win = MyMainForm()
    my_subWin = MySubForm()
    my_win.show()
    sys.exit(app.exec_())
