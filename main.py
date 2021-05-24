import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QUndoStack, QMessageBox, QLabel

from someFunc.lexical.Automata import Lex_analyzer
from someFunc.parser.forecastTable.Grammar import Parser_analyzer
from someFunc.parser.recursiveDescent.Statement import Match_program_stmt
from someFunc.semanticAndMidCode.GrammaticalGuidance import SMC_analyzer
from ui import Ui_MainWindow
from subui import Ui_rndm


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # base info init
        self.windowTitle = "11823020232"
        self.openedFileName = ''
        self.anlsRes = ''
        self.anlsLog = ''
        self.token_list = None

        self.statusBar.showMessage("就绪")
        self.setWindowTitle(self.windowTitle)

        # TODO
        self.undoStack = QUndoStack()  # 存放命令的栈

        # init Other
        self.textEditMain.textChanged.connect(self.change_tips)

        # init menu
        self.init_menu_File()
        self.init_menu_Edit()
        self.init_menu_Lexical()
        self.init_menu_Parsing()
        self.init_menu_MidCode()
        self.init_menu_View()
        self.init_menu_Help()

        # init Interpreter
        self.actionInterpreter_3.triggered.connect(self.Interpreter)

    def init_menu_File(self):
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSaveAs.triggered.connect(self.save_as_file)
        self.actionOpenRecent.setDisabled(True)
        self.actionExit.triggered.connect(self.close)

    def init_menu_Edit(self):
        self.actionCut.triggered.connect(self.cut_text)
        self.actionCopy.triggered.connect(self.copy_text)
        self.actionPaste.triggered.connect(self.paste_text)

    def init_menu_Lexical(self):
        self.actionLexical.triggered.connect(self.LexAnls)
        self.actionNFA_DFA_MFA.triggered.connect(self.rndm)

    def init_menu_Parsing(self):
        self.actionRecuDescent.triggered.connect(self.RecuDescent)
        self.actionForecastTable.triggered.connect(self.ForecastTable)
        self.actionOptrPreced.triggered.connect(self.OptrPreced)

    def init_menu_MidCode(self):
        self.actionGramGuide.triggered.connect(self.GramGuide)

    def init_menu_View(self):
        pass

    def init_menu_Help(self):
        self.actionHelp.triggered.connect(self.open_help)
        self.actionAbout.triggered.connect(self.about_dialog)

    # Other
    def change_tips(self):
        self.setWindowTitle(self.windowTitle + '*')
        self.anlsLog = "not now"

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

        self.anlsRes = ''
        for item in info_list:
            self.anlsRes += '{}\n'.format(item)

        self.anlsLog = ''
        for item in token_list:
            token_str = '{}\t{}\t{}\t{}\t{}'.format(token_list.index(item), item.tag, item.type, item.row, item.col)
            self.anlsLog += '{}\n'.format(token_str)

        self.textEditRes.clear()
        self.textEditRes.setText(self.anlsRes)
        self.textEditLog.setText(self.anlsLog)

    def rndm(self):
        pass
        # my_subWin.show()

    # Parsing
    def RecuDescent(self):
        self.LexAnls()
        self.anlsRes = ''
        self.anlsLog = ''

        parser_anal = Match_program_stmt()
        parser_anal.set_tokenList(self.token_list)
        res, idx, tree, error_list = parser_anal.run(True)
        self.anlsRes = '{}\n{}'.format(res, error_list)
        self.anlsLog = parser_anal.tree.show(stdout=False)

        self.textEditRes.clear()
        self.textEditRes.setText(self.anlsRes)
        self.textEditLog.setText(self.anlsLog)

    def ForecastTable(self):
        self.LexAnls()
        self.anlsRes = ''
        self.anlsLog = ''

        path1 = 'someFunc/parser/forecastTable/grammer_LL(1).txt'
        path2 = 'someFunc/parser/forecastTable/ff_set.txt'
        parser_anal = Parser_analyzer()
        parser_anal.load_analyzer(path1, path2)
        parser_anal.load_stack(self.token_list, 'program')
        self.anlsLog += parser_anal.table_show()
        self.anlsRes, log = parser_anal.run(log=True)
        self.anlsLog += log
        self.anlsLog += parser_anal.AST_Tree.show(stdout=False)
        # parser_anal.create_dotPic('./treePic')

        self.textEditRes.clear()
        self.textEditRes.setText(self.anlsRes)
        self.textEditLog.setText(self.anlsLog)

    def OptrPreced(self):
        self.LexAnls()
        self.anlsRes = ''
        self.anlsLog = ''
        # TODO

        self.textEditRes.clear()
        self.textEditRes.setText(self.anlsRes)
        self.textEditLog.setText(self.anlsLog)

    # MidCode
    def GramGuide(self):
        self.LexAnls()
        self.anlsRes = ''
        self.anlsLog = ''
        # TODO
        path1 = 'someFunc/parser/forecastTable/grammer_LL(1).txt'
        path2 = 'someFunc/parser/forecastTable/ff_set.txt'
        SMC_anal = SMC_analyzer()
        SMC_anal.load_analyzer(path1, path2)
        SMC_anal.load_stack(self.token_list, 'program')
        SMC_anal.run(log=False)

        symbol_table, op_stack, flag = SMC_anal.dfs_detect()  # 返回符号表及四元式组
        if flag:
            symbol_table_new = []
            op_stack_new = []
            # print('符号表')
            for item in symbol_table.items():
                temp = item
                symbol_table_new.append(temp[0])
                # print(temp)
                self.anlsRes += "{}\n".format(temp)
            # print('中间代码')
            for item in op_stack:
                temp = [item.op, item.a1, item.a2, item.res]
                op_stack_new.append(temp)
                # print(op_stack.index(item), temp)
                self.anlsLog += "{}\t{}\n".format(op_stack.index(item), temp)
        else:
            self.anlsRes = symbol_table
            self.anlsLog = op_stack

        self.textEditRes.clear()
        self.textEditRes.setText(self.anlsRes)
        self.textEditLog.setText(self.anlsLog)

    def Interpreter(self):
        print('test')

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
