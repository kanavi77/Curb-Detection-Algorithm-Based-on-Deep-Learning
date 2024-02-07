
import cv2

from multiprocessing import freeze_support


from PyQt5 import uic, QtGui, QtCore

from PyQt5.QtMultimedia import *


from qt_material import apply_stylesheet, QtStyleTools, density


from GUI.label_combox import DefaultLabelComboBox

from GUI.canvas import canvas
from GUI.zoomWidget import ZoomWidget
from GUI.utils import *
from GUI.ustr import ustr
from GUI.load_worker import loadWorker
from GUI.model_dialog import ModelDialog
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


if hasattr(Qt, 'AA_ShareOpenGLContexts'):
    try:
        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    except:
        QCoreApplication.set_attribute(Qt.AA_ShareOpenGLContexts)
else:
    print("'Qt' object has no attribute 'AA_ShareOpenGLContexts'")

freeze_support()



class MyWindow(QMainWindow, QtStyleTools):
    
    def __init__(self):
        super().__init__()

        self = uic.loadUi('./GUI/ui_window.ui', self)
        self.setWindowTitle('路缘石视频检测平台')
         
         
         
        self.canvas = canvas(parent=self)

        
        self.player = QMediaPlayer() 
        self.videoFileUrl = ""
        self.filePath = ""
        self.labelPath = ""
        self.canvas.fileWorker.finished.connect(self.open_file_finish)
        self.loadWorker = loadWorker(self.canvas)
        self.loadWorker.sinOut.connect(self.update_load_status)

        
        self.statusBar = self.statusBar() 
         
        self.label_coordinates = QLabel('Hello')
        self.statusBar.addPermanentWidget(self.label_coordinates)

        
        self.zoom_widget = ZoomWidget()
        self.scroll_area = self.scroll
        self.scroll.setWidget(self.canvas)
        self.scroll.setWidgetResizable(True)
        self.scroll_bars = {
            Qt.Vertical: self.scroll.verticalScrollBar(),
            Qt.Horizontal: self.scroll.horizontalScrollBar()
        }

        
        self.pushButtonPlay.pressed.connect(self.video_play)  
        self.playTimer = QTimer(self)
        self.playTimer.timeout.connect(self.play_frame)
        self.isPlaying = False
        self.buttonBackward.pressed.connect(lambda: self.jump_frame(dpos = -5))
        self.buttonPre.pressed.connect(lambda: self.jump_frame(dpos = -1))
        self.buttonNext.pressed.connect(lambda: self.jump_frame(dpos = 1))
        self.buttonForward.pressed.connect(lambda: self.jump_frame(dpos = 5))

         
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolBarVertical.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.actionFile.triggered.connect(self.open_file)   
        self.actionGt.triggered.connect(self.load_file)
        self.actionGt.setVisible(False)
        self.actionSave.triggered.connect(self.save_file)
        self.actionDict.triggered.connect(self.open_dict)
        self.toolBarVertical.addAction(self.actionZoomIn)
        self.actionZoomIn.triggered.connect(lambda: self.add_zoom(increment = 10))
        self.toolBarVertical.addAction(self.actionZoomOut)
        self.actionZoomOut.triggered.connect(lambda: self.add_zoom(increment = -10))

        self.toolBarVertical.addWidget(self.zoom_widget)
        self.zoom_widget.setValue(100)
        self.zoom_widget.valueChanged.connect(self.paint_canvas)
        self.toolBarVertical.addAction(self.actionFit)
        self.toolBarVertical.addSeparator()

        self.actionFit.triggered.connect(self.adjust_scale)
        
        
        self.labelHint = ['Cub','Fence','Wall','Barrier','Guard_Rail','Curb Cut']
        self.defaultLabel = self.labelHint[0]
        self.labelCombobox = DefaultLabelComboBox(self, items = self.labelHint)
        self.labelCombobox.setVisible(False)
        self.toolBarVertical.addWidget(self.labelCombobox)

        self.toolBarVertical.addAction(self.actionModel)
        self.toolBarVertical.addAction(self.actionTrack)

         

        self.toolBarVertical.addAction(self.actionAnnot)
        self.toolBarVertical.addAction(self.actionDelete)
        self.actionAnnot.setVisible(False)
        self.actionDelete.setVisible(False)
        self.actionDelete.triggered.connect(self.canvas.delete_shape)
        self.actionModel.triggered.connect(self.modelSelect)
        self.actionAnnot.triggered.connect(self.set_create_mode)
        self.actionTrack.triggered.connect(self.canvas.track_frame)   

        
        self.lineCurFrame.returnPressed.connect(self.jump_frame)
         
        
        
        self.vedioSlider.setMinimum(1)
        self.vedioSlider.sliderMoved.connect(self.move_slider) 
        self.vedioSlider.valueChanged.connect(self.move_slider)

        
        self.model = ["tiny_visdrone", "mid_visdrone", "large_visdrone","tiny_mot", "mid_mot", "large_mot"]
        self.modelDialog = ModelDialog(parent=self, model=self.model)
        self.currentModel = self.modelDialog.currentModel

        
        self.canvas.newShape.connect(self.new_shape)
        self.canvas.scrollRequest.connect(self.scroll_request)
        self.canvas.zoomRequest.connect(self.zoom_request)
        self.prev_label_text = ''

    def setupUi(self, MainWindow):
        MainWindow.setWindowIcon(QIcon("图标.ico"))
    
    def open_file(self):
        self.filePath, _ = QFileDialog.getOpenFileName(self, "Open file", "", "mp4 Video (*.mp4)")
        if self.filePath.endswith('.mp4'):
            self.videoFileUrl = QUrl.fromLocalFile(self.filePath)
            
            self.canvas.init_frame(self.filePath)

    def open_file_finish(self):
        self.adjust_scale()
        self.lineCurFrame.setText("1")
        self.labelTotalFrame.setText(str(self.canvas.numFrames))
        self.vedioSlider.setMaximum(self.canvas.numFrames)
    def open_dict_t(self):
        target_dir_path = ustr(QFileDialog.getExistingDirectory(self, 'Open Directory', '.',
                                                                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks))
        self.canvas.init_frame(target_dir_path)
    def open_dict(self):
        target_dir_path = ustr(QFileDialog.getExistingDirectory(self, 'Open Directory', '.', QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks))
        target_dir_path+=r'/result.mp4'

        a1=self.canvas.imgFrames
        a2=self.canvas.returnframes()
        cap = cv2.VideoCapture(self.filePath)
        ret, frame = cap.read()
        fw, fh = int(cap.get(3)), int(cap.get(4))

        out_mp4 = cv2.VideoWriter(target_dir_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (fw, fh))

        for frame in self.canvas.imgFrames:
            out_mp4.write(frame)

        cap.release()
        out_mp4.release()

         
         
         
         
         

    def play_frame(self):
         
        self.canvas.curFramesId += 1
        self.lineCurFrame.setText(str(self.canvas.curFramesId))
        self.vedioSlider.setValue(self.canvas.curFramesId)
        self.canvas.change_frame(self.canvas.curFramesId)
        if self.canvas.curFramesId > self.canvas.numFrames - 1:
            self.playTimer.stop()
            self.pushButtonPlay.setIcon(QIcon("./GUI/resources/svg/play.svg"))
            self.pushButtonPlay.setText("PLAY")

    
    def load_file(self):
        self.statusBar.showMessage("正在加载标注文件，请稍后")
        self.labelPath, _ = QFileDialog.getOpenFileName(self, "Choose annotation file", "", "txt(*.txt)")  
        self.loadWorker.load_path(self.labelPath)
        self.loadWorker.start()

    def update_load_status(self, message):
        self.statusBar.showMessage(message)

   
    def move_slider(self, position):
        self.lineCurFrame.setText(str(position))
        self.jump_frame()

    
    def jump_frame(self, dpos = 0):
        num = int(self.lineCurFrame.text())
         
        dpos = int(dpos)
        if dpos == 0:
            self.canvas.curFramesId = num
            self.vedioSlider.setValue(num)
            self.canvas.change_frame(num)
            self.adjust_scale()
            return
        elif dpos > 0:
            pos = num + dpos if num + dpos <= self.canvas.numFrames else self.canvas.numFrames
            self.lineCurFrame.setText(str(pos))
        elif dpos < 0:
            pos = num + dpos if num + dpos >= 1 else 1
            self.lineCurFrame.setText(str(pos))

        self.canvas.curFramesId = pos
        self.vedioSlider.setValue(pos)
        self.canvas.change_frame(pos)
        self.adjust_scale()

    
    def video_play(self):
        if self.isPlaying is False:
            self.isPlaying = True
            self.pushButtonPlay.setIcon(QIcon("./GUI/resources/svg/stop.svg"))
            self.pushButtonPlay.setText("STOP")
            self.playTimer.start(50)
        else:
            self.isPlaying = False
            self.pushButtonPlay.setIcon(QIcon("./GUI/resources/svg/play.svg"))
            self.pushButtonPlay.setText("PLAY")
            self.playTimer.stop()

    def paint_canvas(self):
         
        self.canvas.scale = 0.01 * self.zoom_widget.value()
         
        self.canvas.adjustSize()
        self.canvas.update()

    
    def adjust_scale(self, initial=False):
         
        self.canvas.pointPos = QPointF(0, 0)
        self.canvas.deltaPos = QPointF(0, 0)
        value = self.scale_fit_window()
        self.zoom_widget.setValue(int(100 * value))
        self.canvas.repaint()

     
    def scale_fit_window(self):
        """Figure out the size of the pixmap in order to fit the main widget."""
        e = 20.0   
        w1 = self.centralWidget().width() - e
        h1 = self.centralWidget().height() - 4 * e
        a1 = w1 / h1
         
        w2 = self.canvas.pixmap.width() - 0.0
        h2 = self.canvas.pixmap.height() - 0.0
        a2 = w2 / h2
        return w1 / w2 if a2 >= a1 else h1 / h2

    def scroll_request(self, delta, orientation):
        units = - delta / (6 * 13)
        bar = self.scroll_bars[orientation]
        bar.setValue(int(bar.value() + bar.singleStep() * units))

    def set_zoom(self, value):
         
         
         
         
         
        self.zoom_widget.setValue(int(value))

    def add_zoom(self, increment=10):
        self.set_zoom(self.zoom_widget.value() + increment)

    def zoom_request(self, delta):
         
         
        h_bar = self.scroll_bars[Qt.Horizontal]
        v_bar = self.scroll_bars[Qt.Vertical]

         
        h_bar_max = h_bar.maximum()
        v_bar_max = v_bar.maximum()

         
         
         
         
         
        cursor = QCursor()
        pos = cursor.pos()
        relative_pos = QWidget.mapFromGlobal(self, pos)

        cursor_x = relative_pos.x()
        cursor_y = relative_pos.y()

        w = self.scroll_area.width()
        h = self.scroll_area.height()

         
         
        margin = 0.1
        move_x = (cursor_x - margin * w) / (w - 2 * margin * w)
        move_y = (cursor_y - margin * h) / (h - 2 * margin * h)

         
        move_x = min(max(move_x, 0), 1)
        move_y = min(max(move_y, 0), 1)

         
        units = delta // (8 * 15)
        scale = 10
        self.add_zoom(scale * units)

         
         
        d_h_bar_max = h_bar.maximum() - h_bar_max
        d_v_bar_max = v_bar.maximum() - v_bar_max

         
        new_h_bar_value = int(h_bar.value() + move_x * d_h_bar_max)
        new_v_bar_value = int(v_bar.value() + move_y * d_v_bar_max)

        h_bar.setValue(new_h_bar_value)
        v_bar.setValue(new_v_bar_value)

    def modelSelect(self):
         
         
        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "选取对应模型",
                                                            os.getcwd(),
                                                            "Pth File (*.pt)")
        self.currentModel=get_filename_path
    def toggle_draw_mode(self, edit=True):
        self.canvas.set_editing(edit)
        self.actionAnnot.setEnabled(edit)

    def set_create_mode(self):
         
        self.toggle_draw_mode(False)

    def default_label_combo_selection_changed(self, index):
        self.defaultLabel = self.labelHint[index]

     
    def new_shape(self):
        """Pop-up and give focus to the label editor.

        position MUST be in global coordinates.
        """
         
        text = self.defaultLabel
        self.prev_label_text = text
        generate_line_color, generate_fill_color = generate_color_by_text(text)
        shape = self.canvas.set_last_label(text, generate_line_color, generate_fill_color)
         
        self.canvas.set_editing(True)  
        self.actionAnnot.setEnabled(True)
         

    def current_path(self):
        return os.path.dirname(self.filePath) if self.filePath else '.'

    def save_file(self):
         
         
         
        savedPath = self.save_file_dialog(remove_ext=False)
        self.save_labels(savedPath)
    
    def save_file_dialog(self, remove_ext=True):
        caption = 'Choose Path to save annotation'
        filters = 'Files Directory(*.*)'
         
        open_dialog_path = self.current_path()
        dlg = QFileDialog(self, caption, open_dialog_path, filters)
         
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        filename = os.path.splitext(self.filePath)[0] + '.txt'
        dlg.selectFile(filename)
        dlg.setOption(QFileDialog.DontUseNativeDialog, False)
        if dlg.exec_():
            full_file_path = ustr(dlg.selectedFiles()[0])
            if remove_ext:
                return os.path.splitext(full_file_path)[0]   
            else:
                return full_file_path
        return ''
        
    def save_labels(self, savedPath):
        with open(f'{savedPath}', 'a') as f:
                for line in self.canvas.result:
                    f.write(('%g ' * len(line)).rstrip() % line + '\n')

     
    def delete_selected_shape(self):
        self.canvas.delete_selected()

    def keyPressEvent(self, ev):
        key = ev.key()
        if key == Qt.Key_Delete or key == Qt.Key_S:
            self.delete_selected_shape()

    def closeEvent(self, event):
        sys.exit(0)


if __name__ == "__main__":
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MyWindow = MyWindow()
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    MyWindow.setWindowIcon(QIcon("图标.ico"))
    MyWindow.showMaximized()
    sys.exit(app.exec_())

