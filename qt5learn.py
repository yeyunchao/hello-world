import sys
import time
import os
from report import report

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import re

from myfirst_ui import Ui_MainWindow
from wave import instrument
import serial.tools.list_ports

class Layoutwave(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.itemdata=[]
        self.uartset=[]
        super(Layoutwave,self).__init__()
        self.setupUi(self)
        #self.label_17.setScaledContents(True)

        self.setupbutton.clicked.connect(self.setupprocess)
        self.selectbutton.clicked.connect(self.readfile)
        self.selectedbutton.clicked.connect(self.transtotable)
        self.configurebutton.clicked.connect(self.transtotable)
        self.allselectbtn.clicked.connect(self.allselect)
        self.notallselectbtn.clicked.connect(self.notallselect)
        self.runbutton.clicked.connect(self.begintest)

        self.finduartport()
        self.lineEdit_19.setText('19200')
        self.lineEdit.setText('7F 08 99 A2 B3 C4 02 FF 01 00 CF')   #turn on
        self.lineEdit_2.setText('7F 08 99 A2 B3 C4 02 FF 01 01 CF')  #turn off
        self.lineEdit_3.setText('7F 08 99 A2 B3 C4 02 FF 05 88 CF')  #vol
        self.lineEdit_4.setText('7F 08 99 A2 B3 C4 02 FF 09 88 CF')  #bl
        self.lineEdit_5.setText('7F 08 99 A2 B3 C4 02 FF 01 0d CF')   #vga
        self.lineEdit_18.setText('7F 08 99 A2 B3 C4 02 FF 01 53 CF')  #hdmi
        self.turnonbtn.clicked.connect(self.testturnon)
        self.turnoffbtn.clicked.connect(self.testturnoff)
        self.volumesetbtn.clicked.connect(self.testvolset)
        self.blsetbtn.clicked.connect(self.blset)
        self.hdmibtn.clicked.connect(self.gohdmi)
        self.vgabtn.clicked.connect(self.govga)

        print('load html')
        url=os.getcwd().replace('\\','/') + r'/webfirst.html'
        #url = r'D:/PycharmProjects/untitled/webfirst.html'
        self.browser = QWebEngineView()
        self.browser.load(QUrl(url))
        self.verticalLayout_3.addWidget(self.browser)



#################uart test######################
    def testturnon(self):
        a=self.lineEdit.text()
        b=a.split(' ')
        c=[]
        for i in b:
            c.append(int(i,16))
        print(self.combobox.currentText())
        print(self.lineEdit_19.text())
        self.porttest(self.combobox.currentText(),int(self.lineEdit_19.text()),c)    #com,  baudrate, cmd
    def testturnoff(self):
        a = self.lineEdit_2.text()
        b = a.split(' ')
        c = []
        for i in b:
            c.append(int(i, 16))
        print(self.combobox.currentText())
        print(self.lineEdit_19.text())
        self.porttest(self.combobox.currentText(), int(self.lineEdit_19.text()), c)  # com,  baudrate, cmd
    def testvolset(self):
        a=self.lineEdit_3.text()
        b = a.split(' ')
        c = []
        for i in b:
            c.append(int(i, 16))
        print(self.combobox.currentText())
        print(self.lineEdit_19.text())
        self.porttest(self.combobox.currentText(), int(self.lineEdit_19.text()), c)  # com,  baudrate, cmd
    def blset(self):
        a=self.lineEdit_4.text()
        b = a.split(' ')
        c = []
        for i in b:
            c.append(int(i, 16))
        print(self.combobox.currentText())
        print(self.lineEdit_19.text())
        self.porttest(self.combobox.currentText(), int(self.lineEdit_19.text()), c)  # com,  baudrate, cmd
    def govga(self):
        a=self.lineEdit_5.text()
        b = a.split(' ')
        c = []
        for i in b:
            c.append(int(i, 16))
        print(self.combobox.currentText())
        print(self.lineEdit_19.text())
        self.porttest(self.combobox.currentText(), int(self.lineEdit_19.text()), c)  # com,  baudrate, cmd
    def gohdmi(self):
        a=self.lineEdit_18.text()
        b = a.split(' ')
        c = []
        for i in b:
            c.append(int(i, 16))
        print(self.combobox.currentText())
        print(self.lineEdit_19.text())
        self.porttest(self.combobox.currentText(), int(self.lineEdit_19.text()), c)  # com,  baudrate, cmd

#################set up####################
    def setupprocess(self):
        self.tabWidget.setCurrentIndex(0)
#################tree to table###############
    def transtotable(self):
        self.tabWidget.setCurrentIndex(2)
        self.myinst = instrument()
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(200)
        self.tableWidget.setHorizontalHeaderLabels(['Test item','Signal','Cat','Inst','Chal','Vert(V)','Hori(s)','Trig S','Trig L(V)'])
        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget.setColumnWidth(1, 90)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 60)
        self.tableWidget.setColumnWidth(4, 40)
        self.tableWidget.setColumnWidth(5, 50)
        self.tableWidget.setColumnWidth(6, 80)
        self.tableWidget.setColumnWidth(7, 50)
        self.tableWidget.setColumnWidth(8, 60)
        for i in range(200):
            newitem=QTableWidgetItem(' ')
            for j in [0,1,2,5,6,7,8]:
                self.tableWidget.setItem(i,j,newitem)
        rowsetdata =[]
        selectedtestitem=[]
        n=0
        for i in self.itemdata:
            for j in i:
                try:
                    a = self.treeWidget.findItems(j, Qt.MatchRegExp | Qt.MatchRecursive, 0)
                except:
                    QMessageBox.warning(self, '警告', '没有加载到测试项目，先点击Select Tests。', QMessageBox.Yes, QMessageBox.Yes)
                    return

                b=a[0].checkState(0)
                if b==2:
                    #print('被选中了b==2')
                    selectedtestitem.append(j)
                    if 'DC_TEST' in self.catitem[self.itemdata.index(i)]:
                        c = j[0:(j.index('V'))]
                        #print(float(c)/3)

                        rowsetdata=[n,'DC_TEST',j,'VOLT',str('%.2f'%(int(c)/3)),'0.05','POS','1']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                        rowsetdata=[n,'DC_TEST',j,'RIPP','0.05','0.05','POS','1']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                        rowsetdata=[n,'DC_TEST',j,'CURR_INRU','2','0.005','POS','1']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                        rowsetdata = [n, 'DC_TEST', j, 'CURR_NOM',  '0.5', '0.05', 'POS', '1']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                        if 'SB' in j:
                            rowsetdata = [n, 'DC_TEST', j, 'CURR_STB', '0.05', '0.05', 'POS','1' ]
                            #print(n)
                            self.rowset(rowsetdata)
                            n = n + 1
                    elif 'SEQUENCE_TEST' in self.catitem[self.itemdata.index(i)]:
                        rowsetdata = [n, 'SEQ_TEST', j, (j.split(','))[0], '2' ,  '0.5', 'POS', '1']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n+1
                        for k in (j.split(','))[1:]:
                            if 'V' in k:
                                if k.index('V')!=0:
                                    c = k[0:(k.index('V'))]
                                    ver = str('%.2f'%(int(c)/3))
                                else:
                                    ver ='2'
                            else:
                                ver = '2'
                            rowsetdata = [n, 'SEQ_TEST', j, k,  ver]
                            #print(n)
                            self.rowset(rowsetdata)
                            n = n+1
                    elif 'AC_TEST' in self.catitem[self.itemdata.index(i)]:
                        rowsetdata = [n, 'AC_TEST', j, ' ', ]
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                    elif 'GPIO_TEST' in self.catitem[self.itemdata.index(i)]:
                        rowsetdata = [n, 'GPIO_TEST', j, 'VOLT',  '2',  '0.5', 'POS', '1']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                    elif 'UART_TEST' in self.catitem[self.itemdata.index(i)]:
                        rowsetdata = [n, 'UART_TEST', j, 'VOLT',  '2',  '0.00005', 'POS','1' ]
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                        rowsetdata = [n, 'UART_TEST', j, 'RISE TIME',  '2', '0.00005', 'POS', '1']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                        rowsetdata = [n, 'UART_TEST', j, 'FALL TIME',  '2',  '0.00005', 'NEG', '1']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                    elif 'AUDIO_TEST' in self.catitem[self.itemdata.index(i)]:
                        rowsetdata = [n, 'AUDIO_TEST', j, 'CH+', '5']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                        rowsetdata = [n, 'AUDIO_TEST', j, 'CH-', '5']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                    elif 'BL_TEST' in self.catitem[self.itemdata.index(i)]:
                        rowsetdata = [n, 'BL_TEST', j, 'ADJ', '2']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                        rowsetdata = [n, 'BL_TEST', j, 'CURR', '0.1']
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                        rowsetdata = [n, 'BL_TEST', j, 'VOLT', '50']
                        # print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
                #####其它自定义情况################
                    else:
                        rowsetdata = [n,self.catitem[self.itemdata.index(i)], j, '', ]
                        #print(n)
                        self.rowset(rowsetdata)
                        n = n + 1
        print('测试项目总数:   '+str(n))

    def rowset(self,rowsetdata):
        newitem=QTableWidgetItem(rowsetdata[1])           #总项目名
        self.tableWidget.setItem(rowsetdata[0],0,newitem)
        newitem=QTableWidgetItem(rowsetdata[2])           #信号
        self.tableWidget.setItem(rowsetdata[0],1,newitem)
        newitem = QTableWidgetItem(rowsetdata[3])         #项目子类名
        self.tableWidget.setItem(rowsetdata[0], 2, newitem)
        if 1:#rowsetdata[1] != 'AC_TEST':
            combox = QComboBox()                                             #instrument
            print(self.myinst.instlist)
            if len(self.myinst.instlist )== 0:
                combox.addItem('无')
                self.tableWidget.setCellWidget(rowsetdata[0], 3, combox)
            else:
                combox.addItem('------')
                for i in self.myinst.instlist:
                    combox.addItem((i.split('::'))[-2][0:4])
                self.tableWidget.setCellWidget(rowsetdata[0], 3, combox)
            combox = QComboBox()                                             #channel
            if len(self.myinst.instlist )== 0:
                combox.addItem('无')
                self.tableWidget.setCellWidget(rowsetdata[0], 4, combox)
            else:
                combox.addItem('1')
                combox.addItem('2')
                combox.addItem('3')
                combox.addItem('4')
                self.tableWidget.setCellWidget(rowsetdata[0], 4, combox)
        if rowsetdata[1] != 'AC_TEST':
            if len(rowsetdata) >5:
                newitem = QTableWidgetItem(rowsetdata[4])  # vertical
                self.tableWidget.setItem(rowsetdata[0], 5, newitem)
                newitem = QTableWidgetItem(rowsetdata[5])  # hor
                self.tableWidget.setItem(rowsetdata[0], 6, newitem)
                newitem = QTableWidgetItem(rowsetdata[6])  # trig slope
                self.tableWidget.setItem(rowsetdata[0], 7, newitem)
                newitem = QTableWidgetItem(rowsetdata[7])  # trig level
                self.tableWidget.setItem(rowsetdata[0], 8, newitem)
            elif len(rowsetdata)==5:
                newitem = QTableWidgetItem(rowsetdata[4])  # vertical
                self.tableWidget.setItem(rowsetdata[0], 5, newitem)


    #################tree init#########################
    def readfile(self):
        self.tabWidget.setCurrentIndex(1)
        pattern = re.compile(r'[^=].+[^=]')
        try :
            f = open('setup.txt','r')
        except:
            QMessageBox.warning(self,'警告','没有Setup.txt文件! 请先生成一个。',QMessageBox.Yes,QMessageBox.Yes)
            return
        a = f.readlines()
        catitemindex =[]
        self.catitem =[]
        for i in a:
            if '=' in i:
                catitemindex.append(a.index(i))
                c = pattern.findall(i[:-1])
                self.catitem.append(c[0])
        print('this is catitem')
        print(self.catitem)
        #print(catitemindex)
        self.itemdata = ['']*len(catitemindex)

        for i in range(0,len(catitemindex)):
            self.itemdata[i]=[]
            if i==len(catitemindex)-1:
                n =len(a)
            else:
                n =catitemindex[i+1]
            for j in range(catitemindex[i]+1,n):
                if a[j][:-1]!='':
                    self.itemdata[i].append(a[j][:-1])
        print('this is itemdata :')
        print(self.itemdata)
        f.close()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['Item', 'Status'])
        root = QTreeWidgetItem(self.treeWidget)
        if self.treeWidget.findItems('海外大屏电性能测试', Qt.MatchRegExp | Qt.MatchRecursive, 0)==[]:
            root.setText(0,'海外大屏电性能测试')
        self.treeWidget.setColumnWidth(0,260)
        self.treeWidget.addTopLevelItem(root)

        for i in range(0,len(self.catitem)):
            child=QTreeWidgetItem()
            child.setText(0,self.catitem[i])
            child.setText(1,'')
            if self.treeWidget.findItems(self.catitem[i], Qt.MatchRegExp | Qt.MatchRecursive, 0) == []:
                root.addChild(child)
            for j in range(0,len(self.itemdata[i])):
                b = self.treeWidget.findItems(self.catitem[i], Qt.MatchRegExp | Qt.MatchRecursive, 0)
                child1 = QTreeWidgetItem()
                child1.setText(0,self.itemdata[i][j])
                child1.setText(1,'NO')
                child1.setCheckState(0,Qt.Checked)
                if self.treeWidget.findItems(self.itemdata[i][j], Qt.MatchRegExp | Qt.MatchRecursive, 0) ==[]:
                    b[0].addChild(child1)
        self.treeWidget.expandAll()
        #print('current:'+self.treeWidget.currentItem())

    def allselect(self):
        for i in self.itemdata:
            for j in i:
                a=self.treeWidget.findItems(j, Qt.MatchRegExp | Qt.MatchRecursive, 0)
                a[0].setCheckState(0,Qt.Checked)
    def notallselect(self):
        for i in self.itemdata:
            for j in i:
                a=self.treeWidget.findItems(j, Qt.MatchRegExp | Qt.MatchRecursive, 0)
                a[0].setCheckState(0,Qt.Unchecked)
################串口寻找##################
    def finduartport(self):
        plist = list(serial.tools.list_ports.comports())
        self.plist_0=[]
        if len(plist)<=0:
            print('no ports')
            self.combobox.addItem('无')
        else:
            for p in plist:
                self.plist_0.append(list(p)[0])
                for uartport in self.plist_0:
                    self.combobox.addItem(uartport)
                    self.combobox.setCurrentText(uartport)

    ################串口发命令测试##################
    def porttest(self,uartport,baudratein,cmdin):
        print('test uart')

        p = serial.Serial(port=uartport, baudrate=baudratein)  # ,bytesize=8,parity='PARITY_NONE',stopbits=1,timeout=60
        cmd=cmdin
        print(uartport)
        print(baudratein)
        print(cmdin)
        p.write(cmd)
        p.close()
        print('uart test is over')

    def gpiotestset(self):
        instnum = '0'
        channel = '2'
        vertical = '1'   #垂直档位
        unit = 'VOLT'  #垂直单位
        probe = '10'
        couple = 'DC'
        tbscale= '0.000002'         #水平档位
        triggerslope = 'NEG'  #边沿触发类型 NEG  RFAL
        triggerlevel = '1'          # 触发电平
        triggersource = channel
        testitem = 'uart_tx_rise_time'
        setdata=[instnum,channel,vertical,unit,probe,tbscale,couple,triggerlevel,triggerslope,triggersource]
        testdemo =[testitem,setdata]
        testdemo1 = testdemo[:]
        testdemo1[0] = 'uart_rx_rise_time'
        testdemo1[1][1]='1'
        test = [testdemo,testdemo1]
        print(test[0][0]+test[1][0])
        path = 'D:\\PycharmProjects\\untitled\\file\\'

        for testexample in test[0:-1]:

            #print('已经连接的设备总数是 '+str(len(self.myinst.instlist)))
            self.myinst.instfind()
            while (len(self.myinst.instlist))==0:
                message = QMessageBox.information(self,'连接VISA设备','没有找到设备，请连好线，还有检查下驱动是否安装好！ ',QMessageBox.Yes)
                self.myinst.instfind()
            self.myinst.gpioinstset()


    def begintest(self):
        self.tabWidget.setCurrentIndex(4)
        self.myinst = instrument()
        rowsnumtotal =0
        column0=[]
        column0num=[]
        column0index = []
        for i in range(200):
            try:
                a = self.tableWidget.item(i, 0).text()
            except:
                QMessageBox.warning(self, '警告', '没有加载到测试项目，先点击Select Tests。', QMessageBox.Yes, QMessageBox.Yes)
                return
            if a !=' ':
                rowsnumtotal =rowsnumtotal+1                       #得到总行数
                column0.append(a)
        print(str(rowsnumtotal))
        column0norep=sorted(set(column0),key=column0.index)    #总项目名
        for i in column0:
            column0num.append(column0.count(i))
        for i in column0norep:
            column0index.append(column0.index(i))
        print(column0num)                                                             #每个主项目数量
        print(column0norep)                                                             #每个主项目名
        print(column0index)                                                             #每个主项目开始位置

        column1=[]
        column1num=[]
        column1index=[]
        for i in range(rowsnumtotal):
            a = self.tableWidget.item(i,1).text()
            column1.append(a)
        for i in column1:
            column1num.append(column1.count(i))                                     #单信号数量
        column1norep = sorted(set(column1),key=column1.index)          #信号名
        for i in column1norep:
            column1index.append(column1.index(i))                                      #单个信号下测试内容数量
        print(column1norep)
        print(column1num)
        print('test signal index: ')
        print(column1index)

        column2=[]
        for i in range(rowsnumtotal):
            a = self.tableWidget.item(i,2).text()
            column2.append(a)
        print('column2 is loaded')
        column3=[]
        for i in range(rowsnumtotal):
            a =self.tableWidget.cellWidget(i,3)
            b = a.currentText()
            column3.append(b)
        print('column3 is loaded')
        column4=[]
        for i in range(rowsnumtotal):
            a = self.tableWidget.cellWidget(i, 4)
            b = a.currentText()
            column4.append(b)
        print('column4 is loaded')
        column5 = []
        for i in range(rowsnumtotal):
            try:
                a = self.tableWidget.item(i, 5).text()
            except:
                a=''
            column5.append(a)
        print('column5 is loaded')
        column6=[]
        for i in range(rowsnumtotal):
            try:
                a = self.tableWidget.item(i,6).text()
            except:
                a= ''
            column6.append(a)
        column7 = []
        for i in range(rowsnumtotal):
            try:
                a = self.tableWidget.item(i, 7).text()
            except:
                a=''
            column7.append(a)
        column8 = []
        for i in range(rowsnumtotal):
            try:
                a = self.tableWidget.item(i, 8).text()
            except:
                a=''
            column8.append(a)
        print('column8 is loaded')
        tablelist =[]
        for i in column1index:
            if column1index.index(i)!=len(column1index)-1:
                m = column1index[column1index.index(i)+1]
                print('hello'+str(m))
            else:
                m = rowsnumtotal
            subpara = column2[i:m]
            instpara = column3[i:m]
            chanpara = column4[i:m]
            vpara = column5[i:m]
            hpara = column6[i:m]
            trigs = column7[i:m]
            trigl = column8[i:m]
            para = [column0[i], column1[i], instpara, chanpara, subpara, vpara, hpara, trigs, trigl]
            tablelist.append(para)
        print(tablelist)

        self.thread = MyThread()                            #测试线程
        a = tablelist
        self.thread.setIdentity(tablelist)
        uartsetdata=[self.combobox.currentText(),self.lineEdit_19.text(),self.lineEdit.text(),self.lineEdit_2.text(),self.lineEdit_3.text(),self.lineEdit_4.text(),self.lineEdit_5.text(),self.lineEdit_18.text()]
        self.thread.setUartport(uartsetdata)
        self.thread.sinOut.connect(self.connectmessage)
        self.thread.sintestingOut.connect(self.testingmessage)
        #self.thread.sintestingOut.connect(self.loadpic)
        self.thread.sinendOut.connect(self.testendmessage)
        self.thread.sinendOut.connect(self.resultreport)

        self.loadpicthread=MyLoadpicThread()
        self.loadpicthread.sinout.connect(self.loadpicmessage)

        self.testingdialog = QDialog()
        self.testinglabel = QLabel('Testing', self.testingdialog)
        self.testinglabel.move(20, 10)
        self.testingpiclabel=QLabel(self.testingdialog)
        self.testingpiclabel.setGeometry(QRect(20,30,1020,530))
        self.testingpiclabel.setText("")

        #label.setPixmap(QPixmap(r'D:\PycharmProjects\untitled\file\SCL1_rise_time.png'))
        self.testingdialog.setWindowTitle('测试中。。。。。。')
        self.testingdialog.setWindowFlags(Qt.WindowCloseButtonHint)
        self.testingdialog.setFixedSize(1060, 570)
        #self.testingdialog.setWindowIcon(r'\hht.jpg')
        self.testingdialog.setWindowModality(Qt.ApplicationModal)
        self.testingdialog.exec_()

    def resultreport(self):
        print('resultreport')
        print(self.catitem)
        print(self.itemdata)
        rep=report(self.itemdata,self.catitem)
        rep.go()
    def outText(self, text):
        print(text)
    def testendmessage(self,text):
        self.testingdialog.close()
        self.loadpicthread.setonoff('')
        dialog = QDialog()
        label = QLabel('Everything is OK!!!!', dialog)
        label.move(100, 50)
        #label.setPixmap(QPixmap(r'D:\PycharmProjects\untitled\file\SCL1_rise_time.png'))
        dialog.setWindowTitle('测试结束！')
        dialog.setWindowFlags(Qt.WindowCloseButtonHint)
        dialog.setFixedSize(300, 200)
        # dialog.setWindowIcon(r'D:\PycharmProjects\untitled\file\SCL1_rise_time.png')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def testingmessage(self,signal,subpara):
        signal =signal
        print('the name from thread')
        print(signal)
        self.testinglabel.setText('')
        self.testinglabel.setText(signal)
        self.testingpiclabel.setPixmap(QPixmap(''))
        print('return the testing signal')
        self.loadpicthread.setonoff('')
        self.loadpicthread.setIdentity(signal)
        print('begin to get the pic')
        self.loadpicthread.setonoff('load thread begin')
        self.loadpicthread.start()

        #dialog.setWindowIcon(r'D:\PycharmProjects\untitled\file\SCL1_rise_time.png')
    def loadpicmessage(self,pic):
        print('have found a pic')
        self.testingpiclabel.setPixmap(QPixmap('.\\file\\'+pic))
        self.testingpiclabel.setScaledContents(True)
        #self.testinglabel.setPixmap(QPixmap('.\\file\\' +pic))

    def connectmessage(self, signal,subpara):
        self.myinst =instrument()
        #instlisttemp = ['adfdfad::dadf::sss::adfadf::werew::5656']
        self.dialogmsg = QDialog()
        channnum = len(subpara)
        self.combo1 = [''] * channnum
        self.combo2 = [''] * channnum
        for i in range(channnum):
            label = QLabel(subpara[i], self.dialogmsg)
            label.move(50, 5 + 20 * (i + 1))
            self.combo1[i] = QComboBox(self.dialogmsg)
            #print('myinst.instlist')
            print(self.myinst.instlist)
            for m in  self.myinst.instlist: #instlisttemp:
                self.combo1[i].addItem((m.split('::'))[-2][0:4])
            self.combo1[i].move(150, 20 * (i + 1))
            self.combo2[i] = QComboBox(self.dialogmsg)
            self.combo2[i].move(250, 20 * (i + 1))
            self.combo2[i].addItem('1')
            self.combo2[i].addItem('2')
            self.combo2[i].addItem('3')
            self.combo2[i].addItem('4')
            #self.combo2[i].selectText='4'
        btn = QPushButton('OK', self.dialogmsg)
        btn.move(130, 150)
        btn.clicked.connect(self.savechannel)
        self.dialogmsg.setWindowTitle(signal+' 通道选择')
        self.dialogmsg.setWindowFlags(Qt.WindowCloseButtonHint)
        self.dialogmsg.setFixedSize(350, 180)
            # dialog.setWindowIcon(r'D:\PycharmProjects\untitled\file\SCL1_rise_time.png')
        self.dialogmsg.setWindowModality(Qt.ApplicationModal)
        self.dialogmsg.exec_()

    def savechannel(self):
        instseledata=[]
        chanseledata=[]
        for i in range(len(self.combo2)):
            instseledata.append(self.combo1[i].currentText())
            chanseledata.append(self.combo2[i].currentText())
        print('instseledata and chanseledata')
        seledata = [instseledata,chanseledata]
        print(seledata)
        self.thread.setchannelok(seledata)
        self.dialogmsg.close()



        #self.test_volumelinear()
        #gpio ,uart ,ac, dc, sequence,
        #self.pixmap = QPixmap(path+testexample[0]+'.png')
        #self.label_17.setPixmap(self.pixmap)
class MyLoadpicThread(QThread):
    sinout=pyqtSignal(str)        #when pic is found ,emit this signal
    def __init__(self, parent=None):
        super(MyLoadpicThread, self).__init__(parent)
        self.identity = None
        self.onoffflag=''

    def setIdentity(self, a):
        print('the signal received :')
        print(a)
        self.identity = a
        self.signallist=[]
    def setonoff(self,c):
        self.onoffflag=c
    def run(self):
        b = self.identity
        while self.onoffflag !='':
            filelist = os.listdir('.\\file')
            #print(filelist)
            for i in filelist:
                if ((self.identity+'_') in i) and (i not in self.signallist) and (i.index(self.identity)==0):
                    self.signallist.append(i)
                    time.sleep(0.5)
                    self.sinout.emit(i)
                    time.sleep(0.5)


class MyThread(QThread):
    sinOut = pyqtSignal(str,list)                 #when have not selected the channel ,then emit this signal
    sinendOut=pyqtSignal(str)                  #when whole test is finish ,then emit this signal
    sintestingOut=pyqtSignal(str,list)       # when one signal is tested ,then emit this signal

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)
        self.identity = None
        self.channelok =None
        self.threadchannelselect=None

    def setIdentity(self, a):
        self.identity = a
    def setchannelok(self,b):
        self.channelok =b

    def setUartport(self, val):
        self.uartport = val
        ##执行线程的run方法
        self.start()

    def run(self):
        #while self.times > 0 and self.identity:
            ##发射信号
            #self.sinOut.emit(self.identity)
            #time.sleep(2)
            #self.times -= 1
        self.myinst=instrument()
        self.myinst.setuart(self.uartport)
        for i in self.identity:
            if i[0]!= 'AC_TEST':
                if ('------' in i[2] )|('无' in i[2]):
                    self.sinOut.emit(i[1],i[4])
                    while self.channelok ==None:
                        pass
                    i[2] = self.channelok[0]
                    i[3]=  self.channelok[1]
                self.channelok=None

                #para = [column0[i], column1[i], instpara, chanpara, subpara, vpara, hpara, trigs, trigl]
            print(i[0])
            print('the signal is:')
            print(i[1])
            time.sleep(1)
            print('Setted from main thread : inst and channel set OK')
            print(i)
            time.sleep(1.5)
            self.sintestingOut.emit(i[1], i[4])
            if i[0] == 'DC_TEST':
                self.dc_test(i)
            elif i[0] == 'AC_TEST':
                pass#self.ac_test(i)
            elif i[0] == 'GPIO_TEST':
                self.gpio_test(i)
            elif i[0] == 'SEQ_TEST':
                self.seq_test(i)
            elif i[0] == 'UART_TEST':
                self.uart_test(i)
            elif i[0] == 'AUDIO_TEST':
                self.audio_test(i)
            elif i[0] == 'BL_TEST':
                self.bl_test(i)
            else:
                pass  #self.other_test(i)

        time.sleep(1)
        self.sinendOut.emit('over')
        self.quit()

    def dc_test(self, para):
        signal = para[1]
        print(signal)
        instmodel = para[2][0]
        for i in list(self.myinst.instlist):
            if instmodel in i:
                instmodelsel = i
        channel = para[3][1:3]
        subpara = para[4]
        vpara = para[5]
        hpara = para[6]
        testset = [instmodelsel, channel, signal, subpara, vpara, hpara]  # 单独一个信号测试
        self.myinst.inst_dc_test(testset)
        print(instmodel)
        print(channel)


    def ac_test(self, para):
        pass

    def gpio_test(self, para):
        signal = para[1]
        instmodel = para[2][0]
        for i in list(self.myinst.instlist):
            if instmodel in i:
                instmodelsel = i
        channel = para[3][0]
        subpara = para[4][0]
        vpara = para[5][0]
        hpara = para[6][0]
        testset = [instmodelsel, channel, signal, subpara, vpara, hpara]
        self.myinst.inst_gpio_test(testset)
        print(instmodel)
        print(channel)

    def seq_test(self,para):
        signal = para[1]
        instmodel = para[2][0]
        for i in list(self.myinst.instlist):
            if instmodel in i:
                instmodelsel = i
        n = len(signal.split(','))
        channel = para[3][0:n]
        subpara = para[4]
        vpara = para[5]
        hpara = para[6]
        testset = [instmodelsel, channel, signal, subpara, vpara, hpara]  # 单独一信号测试
        self.myinst.inst_seq_test(testset)
        print(instmodel)
        print(channel)

    def uart_test(self,para):
        signal = para[1]
        instmodel = para[2][0]
        for i in list(self.myinst.instlist):
            if instmodel in i:
                instmodelsel = i
        channel = para[3][0]
        subpara = para[4][0]
        vpara = para[5][0]
        hpara = para[6][0]
        testset = [instmodelsel, channel, signal, subpara, vpara, hpara]
        self.myinst.inst_gpio_test(testset)

    def audio_test(self,para):
        signal = para[1]
        print(signal)
        instmodel = para[2][0]
        for i in list(self.myinst.instlist):
            if instmodel in i:
                instmodelsel = i
        channel = para[3]
        subpara = para[4]
        vpara = para[5]
        hpara = para[6]
        getvolumelinearvalueset = [instmodelsel, channel, signal, subpara, vpara, hpara]
        # self.finduartport()
        print('begin to test the audio')
        #while self.combobox.currentText() == '无':
            #message = QMessageBox.information(self, '连接串口设备', '没有找到串口设备 ', QMessageBox.Yes)
            #self.finduartport()
        self.myinst.getvolumelinear(getvolumelinearvalueset)

    def bl_test(self,para):
        signal = para[1]
        print(signal)
        instmodel = para[2][0]
        for i in list(self.myinst.instlist):
            if instmodel in i:
                instmodelsel = i
        channel = para[3]
        subpara = para[4]
        vpara = para[5]
        hpara = para[6]
        getbllinearvalueset = [instmodelsel, channel, signal, subpara, vpara, hpara]
        # self.finduartport()
        print('begin to test bl')
        #while self.combobox.currentText() == '无':
            #message = QMessageBox.information(self, '连接串口设备', '没有找到串口设备 ', QMessageBox.Yes)
            #self.finduartport()
        self.myinst.getbllinear(getbllinearvalueset)


    def other_test(self,para):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Layoutwave()
    ui.show()
    app.exec_()
    #sys.exit(app.exec_())
