from other import db
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QInputDialog, QFormLayout, QGroupBox, QVBoxLayout, QComboBox, QLabel, QDialogButtonBox, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView

class UI_Database(QMainWindow):
    def setupUI(self, Database):
        Database.setObjectName("Database")
        self.PopulateTable = QtWidgets.QPushButton(Database)
        self.PopulateTable.setGeometry(QtCore.QRect(10, 10, 91, 23))
        self.PopulateTable.setObjectName("PopulateTable")
        self.CreateTable = QtWidgets.QPushButton(Database)
        self.CreateTable.setGeometry(QtCore.QRect(10, 40, 91, 23))
        self.CreateTable.setObjectName("CreateTable")
        self.DeleteTable = QtWidgets.QPushButton(Database)
        self.DeleteTable.setGeometry(QtCore.QRect(10, 70, 91, 23))
        self.DeleteTable.setObjectName("DeleteTable")
        self.AddEntry = QtWidgets.QPushButton(Database)
        self.AddEntry.setGeometry(QtCore.QRect(10, 100, 91, 23))
        self.AddEntry.setObjectName("AddEntry")
        self.EditEntry = QtWidgets.QPushButton(Database)
        self.EditEntry.setGeometry(QtCore.QRect(10, 130, 91, 23))
        self.EditEntry.setObjectName("EditEntry")
        self.DeleteEntry = QtWidgets.QPushButton(Database)
        self.DeleteEntry.setGeometry(QtCore.QRect(10, 160, 91, 23))
        self.DeleteEntry.setObjectName("DeleteEntry")
        self.SearchTable = QtWidgets.QPushButton(Database)
        self.SearchTable.setGeometry(QtCore.QRect(10, 190, 91, 23))
        self.SearchTable.setObjectName("SearchTable")
        self.OrderTable = QtWidgets.QPushButton(Database)
        self.OrderTable.setGeometry(QtCore.QRect(10, 220, 91, 23))
        self.OrderTable.setObjectName("OrderTable")
        self.ExportGeoJSON = QtWidgets.QPushButton(Database)
        self.ExportGeoJSON.setGeometry(QtCore.QRect(10, 250, 91, 23))
        self.ExportGeoJSON.setObjectName("ExportGeoJSON")

        self.retranslateUI(Database)
        QtCore.QMetaObject.connectSlotsByName(Database)

        self.ExportGeoJSON.clicked.connect(self.export_popup)
        self.OrderTable.clicked.connect(self.order_popup)
        self.SearchTable.clicked.connect(self.search_popup)
        self.DeleteEntry.clicked.connect(self.deleteEntry_popup)
        self.EditEntry.clicked.connect(self.editEntry_popup)
        self.AddEntry.clicked.connect(self.addEntry_popup)
        self.DeleteTable.clicked.connect(self.deleteTable_popup)
        self.CreateTable.clicked.connect(self.createTable_popup)
        self.PopulateTable.clicked.connect(self.populateTable_popup)

    def retranslateUI(self, Database):
        _translate = QtCore.QCoreApplication.translate
        Database.setWindowTitle(_translate("Database", "Database"))
        self.PopulateTable.setText(_translate("Database", "Populate Table"))
        self.CreateTable.setText(_translate("Database", "Create Table"))
        self.DeleteTable.setText(_translate("Database", "Delete Table"))
        self.AddEntry.setText(_translate("Database", "Add Entry"))
        self.EditEntry.setText(_translate("Database", "Edit Entry"))
        self.DeleteEntry.setText(_translate("Database", "Delete Entry"))
        self.SearchTable.setText(_translate("Database", "Search Table"))
        self.OrderTable.setText(_translate("Database", "Order Table"))
        self.ExportGeoJSON.setText(_translate("Database", "Export GeoJSON"))

    def export_popup(self):
        item, ok = QInputDialog.getText(self, "Select Table To Export", "Export Table:")
        if ok and item:
            db.exportTable(item)

    def order_popup(self):
        orderGroupBox = QGroupBox("Order Database Table By Feature")
        orderGroupBox.setWindowTitle("Sorted View")
        tablename = QLineEdit()
        feature = QComboBox()
        feature.addItems(['id', 'row', 'col', 
            'toplx', 'toply', 'toprx', 'topry', 
            'botlx', 'botly', 'botrx', 'botry', 
            'centroidx', 'centroidy'])
        order = QComboBox()
        order.addItems(['asc', 'desc'])
        layout = QFormLayout()
        layout.addRow(QLabel("Table"), tablename)
        layout.addRow(QLabel("Feature"), feature)
        layout.addRow(QLabel("Order"), order)
        orderGroupBox.setLayout(layout)
        orderButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        mainOrderLayout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(mainOrderLayout)
        mainOrderLayout.addWidget(orderGroupBox)
        mainOrderLayout.addWidget(orderButtonBox)
        self.setCentralWidget(central_widget)
        self.show()
        orderButtonBox.accepted.connect(lambda: self.displayTable(
            db.orderTable(
                tablename.text(), 
                feature.currentText(), 
                order.currentText())))
        orderButtonBox.rejected.connect(self.close)

    def search_popup(self):
        orderGroupBox = QGroupBox("View Range")
        orderGroupBox.setWindowTitle("Range View")
        tablename = QLineEdit()
        min_id = QLineEdit()
        max_id = QLineEdit()
        layout = QFormLayout()
        layout.addRow(QLabel("Table"), tablename)
        layout.addRow(QLabel("Min ID"), min_id)
        layout.addRow(QLabel("Max ID"), max_id)
        orderGroupBox.setLayout(layout)
        orderButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        mainOrderLayout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(mainOrderLayout)
        mainOrderLayout.addWidget(orderGroupBox)
        mainOrderLayout.addWidget(orderButtonBox)
        self.setCentralWidget(central_widget)
        self.show()
        orderButtonBox.accepted.connect(lambda: self.displayTable(
            db.searchTable(tablename.text(), min_id.text(), max_id.text())))
        orderButtonBox.rejected.connect(self.close)
        return 

    def displayTable(self, ordered_list):
        ordered_table = QTableWidget()
        ordered_table.setWindowTitle("Custom View")
        ordered_table.setRowCount(len(ordered_list))
        ordered_table.setColumnCount(13)
        ordered_table.setFixedWidth(ordered_table.columnWidth(0) * 13)
        count = 0
        for hid, row, col, toplx, toply, toprx, topry, botlx, botly, botrx, botry, centroidx, centroidy in ordered_list:
            print(hid, row, col, toplx, toply, toprx, topry, botlx, botly, botrx, botry, centroidx, centroidy)
            ordered_table.setItem(0 + count, 0, QTableWidgetItem(str(hid)))
            ordered_table.setItem(0 + count, 1, QTableWidgetItem(str(row)))
            ordered_table.setItem(0 + count, 2, QTableWidgetItem(str(col)))
            ordered_table.setItem(0 + count, 3, QTableWidgetItem(str(toplx)))
            ordered_table.setItem(0 + count, 4, QTableWidgetItem(str(toply)))
            ordered_table.setItem(0 + count, 5, QTableWidgetItem(str(toprx)))
            ordered_table.setItem(0 + count, 6, QTableWidgetItem(str(topry)))
            ordered_table.setItem(0 + count, 7, QTableWidgetItem(str(botlx)))
            ordered_table.setItem(0 + count, 8, QTableWidgetItem(str(botly)))
            ordered_table.setItem(0 + count, 9, QTableWidgetItem(str(botrx)))
            ordered_table.setItem(0 + count, 10, QTableWidgetItem(str(botry)))
            ordered_table.setItem(0 + count, 11, QTableWidgetItem(str(centroidx)))
            ordered_table.setItem(0 + count, 12 , QTableWidgetItem(str(centroidy)))
            count += 1
        features = ['id', 'row', 'col', 
            'toplx', 'toply', 'toprx', 'topry', 
            'botlx', 'botly', 'botrx', 'botry', 
            'centroidx', 'centroidy']
        ordered_table.setHorizontalHeaderLabels(features)
        ordered_table.horizontalHeader().setStretchLastSection(True)
        ordered_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        layout.addWidget(ordered_table)
        self.setCentralWidget(central_widget)
        self.show()
        return

    def deleteEntry_popup(self):
        orderGroupBox = QGroupBox("Headstone To Delete")
        orderGroupBox.setWindowTitle("Headstone To Delete")
        tablename = QLineEdit()
        hid = QLineEdit()
        layout = QFormLayout()
        layout.addRow(QLabel("Table"), tablename)
        layout.addRow(QLabel("ID"), hid)
        orderGroupBox.setLayout(layout)
        orderButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        mainOrderLayout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(mainOrderLayout)
        mainOrderLayout.addWidget(orderGroupBox)
        mainOrderLayout.addWidget(orderButtonBox)
        self.setCentralWidget(central_widget)
        self.show()
        orderButtonBox.accepted.connect(lambda: db.deleteEntry(tablename.text(), hid.text()))
        orderButtonBox.accepted.connect(self.close)
        orderButtonBox.rejected.connect(self.close)

    def editEntry_popup(self):
        orderGroupBox = QGroupBox("Edit An Entry")
        orderGroupBox.setWindowTitle("Edit An Entry")
        tablename = QLineEdit()
        hid = QLineEdit()
        row = QLineEdit()
        col = QLineEdit()
        toplx = QLineEdit()
        toply = QLineEdit()
        toprx = QLineEdit()
        topry = QLineEdit()
        botlx = QLineEdit()
        botly = QLineEdit()
        botrx = QLineEdit()
        botry = QLineEdit()
        centroidx = QLineEdit()
        centroidy = QLineEdit()
        layout = QFormLayout()
        layout.addRow(QLabel("Table"), tablename)
        layout.addRow(QLabel("ID"), hid)
        layout.addRow(QLabel("row"), row)
        layout.addRow(QLabel("col"), col)
        layout.addRow(QLabel("toplx"), toplx)
        layout.addRow(QLabel("toply"), toply)
        layout.addRow(QLabel("toprx"), toprx)
        layout.addRow(QLabel("topry"), topry)
        layout.addRow(QLabel("botlx"), botlx)
        layout.addRow(QLabel("botly"), botly)
        layout.addRow(QLabel("botrx"), botrx)
        layout.addRow(QLabel("botry"), botry)
        layout.addRow(QLabel("centroidx"), centroidx)
        layout.addRow(QLabel("centroidy"), centroidy)
        orderGroupBox.setLayout(layout)
        orderButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        mainOrderLayout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(mainOrderLayout)
        mainOrderLayout.addWidget(orderGroupBox)
        mainOrderLayout.addWidget(orderButtonBox)
        self.setCentralWidget(central_widget)
        self.show()
        orderButtonBox.accepted.connect(lambda: db.editEntry(
            tablename.text(), hid.text(), row.text(), col.text(), 
            toplx.text(), toply.text(), toprx.text(), topry.text(), 
            botlx.text(), botly.text(), botrx.text(), botry.text(), 
            centroidx.text(), centroidy.text()))
        orderButtonBox.accepted.connect(self.close)
        orderButtonBox.rejected.connect(self.close)

    def addEntry_popup(self):
        orderGroupBox = QGroupBox("Add An Entry")
        orderGroupBox.setWindowTitle("Add An Entry")
        tablename = QLineEdit()
        hid = QLineEdit()
        row = QLineEdit()
        col = QLineEdit()
        toplx = QLineEdit()
        toply = QLineEdit()
        toprx = QLineEdit()
        topry = QLineEdit()
        botlx = QLineEdit()
        botly = QLineEdit()
        botrx = QLineEdit()
        botry = QLineEdit()
        centroidx = QLineEdit()
        centroidy = QLineEdit()
        layout = QFormLayout()
        layout.addRow(QLabel("Table"), tablename)
        layout.addRow(QLabel("ID"), hid)
        layout.addRow(QLabel("row"), row)
        layout.addRow(QLabel("col"), col)
        layout.addRow(QLabel("toplx"), toplx)
        layout.addRow(QLabel("toply"), toply)
        layout.addRow(QLabel("toprx"), toprx)
        layout.addRow(QLabel("topry"), topry)
        layout.addRow(QLabel("botlx"), botlx)
        layout.addRow(QLabel("botly"), botly)
        layout.addRow(QLabel("botrx"), botrx)
        layout.addRow(QLabel("botry"), botry)
        layout.addRow(QLabel("centroidx"), centroidx)
        layout.addRow(QLabel("centroidy"), centroidy)
        orderGroupBox.setLayout(layout)
        orderButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        mainOrderLayout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(mainOrderLayout)
        mainOrderLayout.addWidget(orderGroupBox)
        mainOrderLayout.addWidget(orderButtonBox)
        self.setCentralWidget(central_widget)
        self.show()
        orderButtonBox.accepted.connect(lambda: db.addEntry(
            tablename.text(), hid.text(), row.text(), col.text(), 
            toplx.text(), toply.text(), toprx.text(), topry.text(), 
            botlx.text(), botly.text(), botrx.text(), botry.text(), 
            centroidx.text(), centroidy.text()))
        orderButtonBox.accepted.connect(self.close)
        orderButtonBox.rejected.connect(self.close)

    def deleteTable_popup(self):
        item, ok = QInputDialog.getText(self, "Enter Table To Delete", "Table To Delete:")
        if ok and item:
            db.deleteTable(item)

    def createTable_popup(self):
        item, ok = QInputDialog.getText(self, "Enter Table To Create", "Table To Create:")
        if ok and item:
            db.createTable(item)

    def populateTable_popup(self):
        item, ok = QInputDialog.getText(self, "Enter Table To Auto-Populate", "Table To Auto-Populate:")
        if ok and item:
            db.PopulateTable(item, _)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Database = QtWidgets.QWidget()
    ui = UI_Database()
    ui.setupUI(Database)
    Database.show()
    sys.exit(app.exec_())
