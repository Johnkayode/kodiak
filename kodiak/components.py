import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *



class Label(QLabel):
    def __init__(self, name: str,  *args) -> None:
        super().__init__(name, *args)
        self.setStyleSheet('QLabel { text-align: right; }')


class FileFormatComboBox(QComboBox):
    """FileFormatComboBox displays the list of available file formats"""
    file_format_changed = pyqtSignal(str)

    def __init__(self, default_file_format: int, *args) -> None:
        super().__init__(*args)
        self.file_formats = ["Excel", "Csv"]
        self.addItems(self.file_formats)
        self.currentIndexChanged.connect(self.on_index_changed)
        self.setCurrentText(default_file_format)

    def on_index_changed(self, index: int):
        self.file_format_changed.emit(self.file_formats[index])


class FileDialog(QFileDialog):
    """FileDialog selects input file"""

    def __init__(self, file_filter: str, *args) -> None:
        super().__init__(*args)
        self.file_filter = file_filter

    def get_file(self):
        return self.getOpenFileName(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=self.file_filter,
        )

    def get_download_path(self):
        return self.getSaveFileName(
            parent=self, 
            caption='Select Download path',
            directory=os.getcwd(),
            filter=self.file_filter
        )
   

class JSONDisplayBox(QTextEdit):
    """JSONDisplayBox is a read-only textbox"""


    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.setReadOnly(True)
        self.setPlaceholderText("JSON")
        self.setStyleSheet(
            '''QTextEdit {
                padding-left: 5;
                padding-top: 5;
                padding-bottom: 5;
                padding-right: 5;
                color: #ffa500;
                background-color: #222222;
            }''' 
        )


class HeaderCheckBox(QCheckBox):
    """HeaderCheckBox is a checkbox to set header value"""
    header_btn_checked = pyqtSignal(bool)

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.setChecked(True)
        self.stateChanged.connect(self.on_btn_checked)
    
    def on_btn_checked(self, _):
        self.header_btn_checked.emit(self.isChecked())