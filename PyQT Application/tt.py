import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout


class InputWindow(QWidget):

    def __init__(self):
        super().__init__()

        # 创建输入框
        self.conf_thres_edit = QLineEdit()
        self.iou_thres_edit = QLineEdit()
        self.device_edit = QLineEdit()
        self.classes_edit = QLineEdit()
        self.agnostic_nms_edit = QLineEdit()
        self.augment_edit = QLineEdit()
        self.line_thickness_edit = QLineEdit()
        self.hide_labels_edit = QLineEdit()
        self.hide_conf_edit = QLineEdit()

        # 创建标签
        conf_thres_label = QLabel("conf_thres:")
        iou_thres_label = QLabel("iou_thres:")
        device_label = QLabel("device:")
        classes_label = QLabel("classes:")
        agnostic_nms_label = QLabel("agnostic_nms:")
        augment_label = QLabel("augment:")
        line_thickness_label = QLabel("line_thickness:")
        hide_labels_label = QLabel("hide_labels:")
        hide_conf_label = QLabel("hide_conf:")

        # 创建布局
        hbox1 = QHBoxLayout()
        hbox1.addWidget(conf_thres_label)
        hbox1.addWidget(self.conf_thres_edit)
        hbox1.addWidget(iou_thres_label)
        hbox1.addWidget(self.iou_thres_edit)
        hbox1.addWidget(device_label)
        hbox1.addWidget(self.device_edit)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(classes_label)
        hbox2.addWidget(self.classes_edit)
        hbox2.addWidget(agnostic_nms_label)
        hbox2.addWidget(self.agnostic_nms_edit)
        hbox2.addWidget(augment_label)
        hbox2.addWidget(self.augment_edit)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(line_thickness_label)
        hbox3.addWidget(self.line_thickness_edit)
        hbox3.addWidget(hide_labels_label)
        hbox3.addWidget(self.hide_labels_edit)
        hbox3.addWidget(hide_conf_label)
        hbox3.addWidget(self.hide_conf_edit)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        # 创建按钮
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.submit)

        vbox.addWidget(self.button)
        self.setLayout(vbox)

    def submit(self):
        # 处理用户提交的数据
        conf_thres = self.conf_thres_edit.text()
        iou_thres = self.iou_thres_edit.text()
        device = self.device_edit.text()
        classes = self.classes_edit.text()
        agnostic_nms = self.agnostic_nms_edit.text()
        augment = self.augment_edit.text()
        line_thickness = self.line_thickness_edit.text()
        hide_labels = self.hide_labels_edit.text()
        hide_conf = self.hide_conf_edit.text()

        # 打印提交的数据
        print("conf_thres:", conf_thres)
        print("iou_thres:", iou_thres)
        print("device:", device)
        print("classes:", classes)
        print("agnostic_nms:", agnostic_nms)
        print("augment:", augment)
        print("line_thickness:", line_thickness)
        print("hide_labels:", hide_labels)
        print("hide_conf:", hide_conf)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InputWindow()
    window.show()
    sys.exit(app.exec_())
