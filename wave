# -*- coding: utf-8 -*-
import visa
import time
import serial
import matplotlib.pyplot   as plt
import numpy as np
from matplotlib.ticker import  (MultipleLocator, FormatStrFormatter,AutoMinorLocator)

class instrument:
   def __init__(self):
      self.rm = visa.ResourceManager()
      self.instlist = self.rm.list_resources()
      print('class instrument initial,rm open')

      #if len(self.instlist)==0:
         #print('no 设备')

      #print('连接上的设备有：  ' + str(self.instlist))
   def setuart(self,val):
       self.uartport=val[0]
       self.baudrate=int(val[1])
       self.turnon=self.strtohex(val[2])
       self.turnoff=self.strtohex(val[3])
       self.setvol=self.strtohex(val[4])
       self.setbl=self.strtohex(val[5])
       self.govga=self.strtohex(val[6])
       self.gohdmi=self.strtohex(val[7])
       print('set volumn uart command:')
       print(self.setvol)
   def strtohex(self,val):
      b = val.split(' ')
      c = []
      for i in b:
         c.append(int(i, 16))
      return(c)
   def insttestset(self, testdemo,path):
      self.testdemo = testdemo  # [instnum,channel,vertical,unit,tbscale,couple,triggerlevel,triggerslope]
      self.numb = int(testdemo[1][0])
      self.channel = testdemo[1][1]
      self.vertical = testdemo[1][2]
      self.unit = testdemo[1][3]
      self.probe = testdemo[1][4]
      self.tbscale = testdemo[1][5]
      self.couple = testdemo[1][6]
      self.triggerlevel = testdemo[1][7]
      self.triggerslope = testdemo[1][8]
      self.triggersource = testdemo[1][9]
      self.testitem = testdemo[0]
      self.path = path

   def instfind(self):
      self.rm = visa.ResourceManager()
      self.instlist = self.rm.list_resources()

   def inst_dc_test(self,testset):
      instmodelsel =testset[0]
      self.inst=self.rm.open_resource(instmodelsel)
      volt_channel = testset[1][0]
      curr_channel= testset[1][1]
      signal = testset[2]
      voltageV =testset[4][0]
      rippleV = testset[4][1]
      currentV =testset[4][3]
      inrushV = testset[4][2]
      H = testset[5][0]
      inrushH=testset[5][2]
      print('create the data file')
      f=open('.\\data\\'+signal+'.txt','w')
      f.write('VOLTAGE,NORMAL CURRENT,RIPPLE,INRUSH CURRENT\n')
      self.inst.write(':RUN')
      self.inst.write(':CHAN' + volt_channel + ':DISP 1')
      self.inst.write(':CHAN' + volt_channel + ':COUPling DC')
      self.inst.write(':CHAN' + curr_channel + ':DISP 1')
      self.inst.write(':CHAN' + curr_channel + ':COUPling DC')
      self.inst.write(':CHAN' + volt_channel + ':SCAL ' + voltageV)
      self.inst.write(':CHAN' + curr_channel + ':SCAL ' + currentV)
      self.inst.write(':TIMebase:SCAL ' +H )
      self.inst.write(':TRIGger:COUPling ' + 'DC')
      self.inst.write(':TRIGger:EDGe:SOUR CHAN' + volt_channel)
      self.inst.write(':TRIGger:EDGe:LEVel ' + '1')
      self.inst.write(':TRIGger:EDGe:SLOP ' + 'POS')

      time.sleep(3)
      self.inst.write(':STOP')
      time.sleep(1)
      voltage =self.inst.query(':MEASure:VRMS? ' + 'CHAN'+volt_channel)
      print('voltage')
      print(voltage)
      f.write(str(voltage))

      current = self.inst.query(':MEASure:VRMS? ' + 'CHAN' + curr_channel)
      print('current')
      print(current)
      f.write(str(current) )

      channel=['']*2
      channel[0]=volt_channel
      channel[1]=curr_channel
      Label=['']*2
      Label[0]='Vrms '+str('%.2f'%(float(voltage)))+'V'
      Label[1]='Crms '+str('%.2f'%(float(current)))+'A'
      self.datatofigure(signal+'_Volt_Curr',channel,Label)             #voltage ,currentn绘图

      self.inst.write(':RUN')
      self.inst.write(':CHAN' + volt_channel + ':COUPling AC')
      self.inst.write(':CHAN' + volt_channel + ':SCAL ' + rippleV)
      time.sleep(3)
      self.inst.write(':STOP')
      time.sleep(0.5)
      ripple = self.inst.query(':MEASure:VAMP? ' + 'CHAN' + volt_channel)
      print('ripple')
      print(ripple)
      f.write(str(ripple) )
      channel=['']
      channel[0]=volt_channel
      Label=['']
      Label[0]='Ripple Vpp '+str('%.2f'%(float(ripple)))+'V'
      self.datatofigure(signal+'_Ripp', channel, Label)

      self.inst.write(':RUN')
      time.sleep(2)
      self.inst.write(':TIMebase:SCAL ' + inrushH)
      self.inst.write(':CHAN' + curr_channel + ':SCAL ' + inrushV)
      self.inst.write(':TRIGger:EDGe:SOUR CHAN' + curr_channel)
      self.inst.write(':TRIGger:EDGe:LEVel ' + '1')
      self.inst.write(':TRIGger:SWEep SING')

      while ('STOP' in (self.inst.query(':TRIGger:STATus?')))!=1 :
         time.sleep(1)
      inrush = self.inst.query(':MEASure:VMAX? ' + 'CHAN' + curr_channel)
      print('inrush')
      print(inrush)
      f.write(str(inrush) )
      channel=['']
      channel[0]=curr_channel
      Label=['']
      Label[0]='Inrush Current '+str('%.2f'%(float(inrush)))+'A'
      self.datatofigure(signal+'_Inrush', channel, Label)
      f.close()


   def inst_gpio_test(self,testset):
      instmodelsel =testset[0]
      self.inst=self.rm.open_resource(instmodelsel)
      volt_channel = testset[1]
      signal = testset[2]
      voltageV =testset[4]
      H = testset[5]
      f = open('.\\data\\' + signal + '.txt', 'w')
      f.write('MAX,MIN,|RT,OVERSHOOT,FT,OVERSHOOT|\n')
      self.inst.write(':RUN')
      self.inst.write(':CHAN' + volt_channel + ':DISP 1')
      self.inst.write(':CHAN' + volt_channel + ':COUPling DC')
      self.inst.write(':CHAN' + volt_channel + ':SCAL ' + voltageV)
      self.inst.write(':TIMebase:SCAL ' +H )
      if 'ADJ' in signal:
          self.inst.write(':TIMebase:SCAL ' + '0.01')
      time.sleep(7)
      self.inst.write(':TRIGger:COUPling ' + 'DC')
      self.inst.write(':TRIGger:EDGe:SOUR CHAN' + volt_channel)
      self.inst.write(':TRIGger:EDGe:LEVel ' + '1')
      if float(self.inst.query(':MEASure:VMAX? ' + 'CHAN' + volt_channel))>1:
         self.inst.write(':TRIGger:EDGe:SLOP ' + 'NEG')
      else:
         self.inst.write(':TRIGger:EDGe:SLOP ' + 'POS')

      self.inst.write(':TRIGger:SWEep SING')

      while ('STOP' in (self.inst.query(':TRIGger:STATus?')))!=1 :
         time.sleep(1)
      voltage1 = self.inst.query(':MEASure:VMAX? ' + 'CHAN' + volt_channel)
      f.write(str(voltage1) )
      time.sleep(0.5)
      voltage2 = self.inst.query(':MEASure:VMIN? ' + 'CHAN' + volt_channel)
      f.write(str(voltage2) )
      time.sleep(2)
      print('GPIO')
      print(voltage1)
      print(voltage2)
      channel=['']
      channel[0]=volt_channel
      Label=['']
      Label[0]='Volt '+str('%.2f'%(float(voltage1)))+'V   '+str('%.2f'%(float(voltage2)))+'V'
      self.datatofigure(signal+'_Max_Min', channel, Label)


      print('begin to test uart')
      if ('TX' in signal )|( 'RX' in signal)|('IR' in signal):
          self.inst.write(':RUN')
          print('test the uart rise time')
          self.inst.write(':TIMebase:SCAL ' + str(float(H)/25))
          self.inst.write(':TRIGger:EDGe:SLOP ' + 'POS')
          time.sleep(2)
          self.inst.write(':TRIGger:SWEep SING')
          while ('STOP' in (self.inst.query(':TRIGger:STATus?'))) != 1:
              time.sleep(1)
          time.sleep(1)
          risetime = self.inst.query(':MEASure:RTIM? ' + 'CHAN' + volt_channel)
          time.sleep(0.5)
          overshoot = self.inst.query(':MEASure:OVER? ' + 'CHAN' + volt_channel)
          time.sleep(2)
          print('UART/IR')
          print(risetime)
          print(overshoot)
          f.write(str(risetime) )
          f.write(str(overshoot) )
          channel = ['']
          channel[0] = volt_channel
          Label = ['']
          Label[0] = 'Risetime ' + str('%.9f' % (float(risetime))) + 's   ' + str('%.2f' % (float(overshoot)*100)) + '%'
          self.datatofigure(signal+'_Rise_Overshoot', channel, Label)

      if ('TX' in signal) | ('RX' in signal)|('IR' in signal):
          self.inst.write(':RUN')
          print('begin to test fall time')
          self.inst.write(':TIMebase:SCAL ' + str(float(H) / 1000))
          self.inst.write(':TRIGger:EDGe:SLOP ' + 'NEG')
          time.sleep(2)
          self.inst.write(':TRIGger:SWEep SING')
          while ('STOP' in (self.inst.query(':TRIGger:STATus?'))) != 1:
              time.sleep(1)
          time.sleep(1)
          falltime = self.inst.query(':MEASure:FTIM? ' + 'CHAN' + volt_channel)
          time.sleep(0.5)
          overshoot = self.inst.query(':MEASure:OVER? ' + 'CHAN' + volt_channel)
          time.sleep(2)
          print('UART/IR')
          print(falltime)
          print(overshoot)
          f.write(str(falltime))
          f.write(str(overshoot))
          channel = ['']
          channel[0] = volt_channel
          Label = ['']
          Label[0] = 'Falltime ' + str('%.9f' % (float(falltime))) + 's   ' + str('%.2f' % (float(overshoot)*100)) + '%'
          self.datatofigure(signal+'_Fall_Overshoot', channel, Label)
      f.close()

   def inst_seq_test(self, testset):
       instmodelsel = testset[0]
       self.inst = self.rm.open_resource(instmodelsel)
       channel = testset[1]
       signal = testset[2]
       voltageV = testset[4]
       H = testset[5][0]
       self.inst.write(':RUN')
       #######
       ########关机
       a=self.turnon.copy()
       a[-2]=0x37
       self.querystatus=a.copy()
       p = serial.Serial(port=self.uartport, baudrate=self.baudrate,timeout=1)
       r = serial.Serial(port='COM4', baudrate=115200, timeout=1)
       p.write(self.querystatus)
       b=p.readline()
       print(b)
       if b'\xcf' not in b:
           r.write([0x7f,0x08,0x99,0xa2,0xb3,0xc4,0x02,0xff,0x01,0x02,0xcf])
           time.sleep(5)
       p.write(self.querystatus)
       b = p.readline()
       if b'\x01\xcf' in b:      ###开机状态
           print('close the monitor')
           p.write(self.turnoff)
           time.sleep(0.5)
           p.write(self.turnoff)
           time.sleep(5)
       ########
       self.inst.write(':RUN')
       for i in range(0,len(channel)):
           self.inst.write(':CHAN' + channel[i] + ':DISP 1')
           self.inst.write(':CHAN' + channel[i] + ':COUPling DC')
           self.inst.write(':CHAN' + channel[i] + ':SCAL ' + voltageV[i])

       self.inst.write(':TIMebase:SCAL ' + H)

       self.inst.write(':TRIGger:COUPling ' + 'DC')
       self.inst.write(':TRIGger:EDGe:SOUR CHAN' + channel[0])
       self.inst.write(':TRIGger:EDGe:LEVel ' + '1')
       self.inst.write(':TRIGger:EDGe:SLOP ' + 'POS')
       time.sleep(7)
       self.inst.write(':TRIGger:SWEep SING')
       time.sleep(12)

       ########UART 开机
       p.write(self.turnon)
       ########

       while ('STOP' in (self.inst.query(':TRIGger:STATus?'))) != 1:
           time.sleep(1)
       print('SEQ rise')
       Label = signal.split(',')
       self.datatofigure(signal+'_pon ', channel, Label)
       if 'OPS' not in signal:
            self.inst.write(':TIMebase:SCAL ' + str(float(H)/25))
            time.sleep(1)
            self.datatofigure(signal + '_pon '+str(float(H)/25)+'s', channel, Label)

       time.sleep(0.5)
       self.inst.write(':RUN')
       time.sleep(0.5)
       self.inst.write(':TRIGger:EDGe:LEVel ' + '1')
       self.inst.write(':TRIGger:EDGe:SLOP ' + 'NEG')
       self.inst.write(':TIMebase:SCAL ' + H)
       self.inst.write(':TRIGger:SWEep SING')
       time.sleep(25)
       #########UART 关机###########################
       p.write(self.turnoff)
       time.sleep(0.5)
       p.write(self.turnoff)

       while ('STOP' in (self.inst.query(':TRIGger:STATus?'))) != 1:
           time.sleep(1)
       print('SEQ fall')
       Label = signal.split(',')
       self.datatofigure(signal+'_poff', channel, Label)
       if 'OPS' not in signal:
            self.inst.write(':TIMebase:SCAL ' + str(float(H)/25))
            time.sleep(1)
            self.datatofigure(signal + '_poff '+str(float(H)/25)+'s', channel, Label)

       if signal.count('V')> 2:       #test AC ON/OFF

           p.write(self.querystatus)
           b = p.readline()
           print(b)
           #if b'\xcf' in b:  ###有电状态
               #print('power off monitor')
           r.write([0x7f,0x08,0x99,0xa2,0xb3,0xc4,0x02,0xff,0x01,0x02,0xcf])
           time.sleep(2)
           self.inst.write(':TIMebase:SCAL ' + H)
           self.inst.write(':RUN')

           self.inst.write(':TRIGger:COUPling ' + 'DC')
           self.inst.write(':TRIGger:EDGe:SOUR CHAN' + channel[0])
           self.inst.write(':TRIGger:EDGe:LEVel ' + '1')
           self.inst.write(':TRIGger:EDGe:SLOP ' + 'POS')
           time.sleep(15)
           self.inst.write(':TRIGger:SWEep SING')
           time.sleep(6)

           ########AC 开机
           r.write([0x7f,0x08,0x99,0xa2,0xb3,0xc4,0x02,0xff,0x01,0x02,0xcf])
           ########

           while ('STOP' in (self.inst.query(':TRIGger:STATus?'))) != 1:
               time.sleep(1)
           print('SEQ ac on ')
           Label = signal.split(',')
           self.datatofigure(signal + '_ac on ', channel, Label)
           if 'OPS' not in signal:
               self.inst.write(':TIMebase:SCAL ' + str(float(H) / 10))
               time.sleep(1)
               self.datatofigure(signal + '_ac on ' + str(float(H) / 10) + 's', channel, Label)

           time.sleep(0.5)
           p.write(self.turnon)
           self.inst.write(':RUN')
           time.sleep(2)
           self.inst.write(':TRIGger:EDGe:LEVel ' + '2.5')
           self.inst.write(':TRIGger:EDGe:SLOP ' + 'NEG')
           self.inst.write(':TIMebase:SCAL ' + H)
           self.inst.write(':TRIGger:SWEep SING')
           time.sleep(10)
           #########AC 关机###########################
           r.write([0x7f,0x08,0x99,0xa2,0xb3,0xc4,0x02,0xff,0x01,0x02,0xcf])
           time.sleep(0.5)
           #p.write(self.turnoff)

           while ('STOP' in (self.inst.query(':TRIGger:STATus?'))) != 1:
               time.sleep(1)
           print('SEQ ac off')
           Label = signal.split(',')
           self.datatofigure(signal + '_AC off', channel, Label)
           if 'OPS' not in signal:
               self.inst.write(':TIMebase:SCAL ' + str(float(H) / 10))
               time.sleep(1)
               self.datatofigure(signal + '_AC off ' + str(float(H) / 10) + 's', channel, Label)

       p.close()
       r.close()


   def datatofigure(self,signal,channel,Label):
       yv=[]
       print(channel)
       print('channelshuliang  '+str(len(channel)))
       for i in channel:
            y = []
            indexnum = channel.index(i)
            time.sleep(1)
            self.inst.write(':WAVeform:SOURce CHANnel' + i)
            self.inst.write(":WAVeform:POINts 700")
            preamble_string = self.inst.query(":WAVeform:PREamble?")
            xincrement = self.inst.query(':WAVeform:XINCrement?')
            print(preamble_string)
            preamdata =preamble_string[:-1].split(',')
            print(preamdata)
            time.sleep(0.5)
            #point=self.inst.query(':WAVeform: POINts?')
            self.inst.write(":WAV:RESet")
            self.inst.write(":WAV:BEG")
            status= self.inst.query(':WAV:STATus?')
            print('status')
            print(status)
            self.inst.write(":WAVeform:DATA?")
            time.sleep(0.5)
            data = self.inst.read_raw()
            print(self.inst.query(':WAV:STATus?'))
            while self.inst.query(':WAV:STATus?')=='READ':
                self.inst.write(":WAVeform:DATA?")
                data.append(self.inst.read_raw())
            self.inst.write(":WAV:END")
            datah = data[11:-1]
            print(data[0:11])
            # f.write(datah)
            # f.close()
            print(len(datah))
            lenth=len(datah)
            print('index    '+str(indexnum))
            for k in range(0, lenth):
                y.append((float(datah[k]) - float(preamdata[-1]) - float(preamdata[-2])) * float(preamdata[-3]))
            yv.append(y)
            # f.close()
       print(yv[0])
       if (float(preamdata[4]) < 0.000001):
            x = np.linspace(0, float(xincrement) * lenth * 1000 * 1000, lenth)
            xvalue = float(xincrement) * lenth * 1000 * 1000
            xlabel = 'Time [us]'
       elif ((float(xincrement) <= 0.001) & (float(xincrement) >= 0.000001)):
            x = np.linspace(0, float(xincrement) * lenth * 1000, lenth)
            xvalue = float(xincrement) * lenth * 1000
            xlabel = 'Time [ms]'
       else:
            x = np.linspace(0, float(xincrement) * lenth, lenth)
            xvalue = float(xincrement) * lenth
            xlabel = 'Time [s]'
       #majorLocator = MultipleLocator(20)
       #majorFormatter = FormatStrFormatter('%d')
       #minorLocator = MultipleLocator(5)
       plt.cla()
       ax = plt.subplot(111)
       plt.figure(figsize=(10, 5))
       # plt.style.use('classic')

       plt.ylabel('Voltage [V]')
       plt.xlabel(xlabel)
       plt.title(signal + '  '  + '       ' + time.asctime(time.localtime(time.time())))
       for n in yv:
            plt.plot(x, n, label=Label[yv.index(n)])
       plt.xlim(0, xvalue)
       leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=False, fancybox=False)
       sublable=' '.join(Label)
       print(sublable)
       plt.savefig('.\\file\\' + signal  + r'.png')
       #plt.savefig('.\\file\\' + signal+'_'+sublable + r'.png')


   def gpioinstset(self):
      #f=open(r'D:\PycharmProjects\untitled\wavedata.bin','wb')
      #print(inst.query(':CHAN1:DISP?'))
      #my_instrument.write(':CHAN1:DISP 1')
      self.inst = self.rm.open_resource(self.instlist[self.numb])
      print('inst is openning')
      # inst= rm.open_resource('USB0::0x1AB1::0x04B0::DS2D154800818::INSTR')
      print(self.inst.query('*IDN?'))

      self.inst.write(':CHAN'+self.channel+':DISP 1')
      self.inst.write(':WAVeform:SOURce CHANnel'+self.channel)
      self.inst.write(':CHAN' + self.channel + ':SCAL '+self.vertical)
      self.inst.write(':CHAN' + self.channel + ':UNIT '+self.unit)
      self.inst.write(':CHAN' + self.channel + ':PROB ' + self.probe)
      self.inst.write(':TIMebase:SCAL ' + self.tbscale)
      self.inst.write(':TRIGger:COUPling ' + self.couple)
      self.inst.write(':TRIGger:EDGe:SOUR CHAN' + self.triggersource)
      self.inst.write(':TRIGger:EDGe:LEVel ' + self.triggerlevel)
      self.inst.write(':TRIGger:EDGe:SLOP ' + self.triggerslope)
      self.inst.write(':RUN')
      self.inst.write(':TRIGger:SWEep SING')

      while ('STOP' in (self.inst.query(':TRIGger:STATus?')))!=1 :
         time.sleep(1)



      #inst.write(":WAVeform:POINts 2000")
      #inst.write(":WAVeform:FORMat ASCii")

      self.testresult=self.inst.query(':MEASure:FTIMe?')
      if (float(self.testresult)<=0.001):
         self.result = str('%.5f'%(float(self.testresult) *1000))+'ms'
      else :
         self.result = str(float(self.testresult))+'s'
      print('the fall time is '+self.result)

      self.preamble_string = self.inst.query(":WAVeform:PREamble?")
      self.xincrement = self.inst.query(':WAVeform:XINCrement?')
      print(self.preamble_string)
      self.preamdata=self.preamble_string[:-1].split(',')
      print(self.preamdata)
      self.inst.write(":WAVeform:DATA?")
      self.data = self.inst.read_raw()
      self.datah=self.data[11:-1]
      print(self.data[0:11])
   #f.write(datah)
   #f.close()
      print(len(self.datah))

      self.yv= []
      for i in range(0,700):
         self.yv.append((float(self.datah[i])-float(self.preamdata[-1])-float(self.preamdata[-2]))*float(self.preamdata[-3]))
#print(yval)
#f.close()
#x= range(0,700)
      if(float(self.preamdata[4]) < 0.000001):
         self.x = np.linspace(0, float(self.xincrement)*700*1000*1000, 700)
         self.xvalue=float(self.xincrement)*700*1000*1000
         self.xlabel = 'Time [us]'
      elif((float(self.xincrement) <= 0.001) & (float(self.xincrement) >= 0.000001)):
         self.x = np.linspace(0, float(self.xincrement) * 700*1000 , 700)
         self.xvalue = float(self.xincrement) * 700 * 1000
         self.xlabel = 'Time [ms]'
      else:
         self.x = np.linspace(0, float(self.xincrement) * 700 , 700)
         self.xvalue = float(self.xincrement) * 700
         self.xlabel = 'Time [s]'
      #print(self.x)
      #print(self.yv)

      majorLocator = MultipleLocator(20)
      majorFormatter = FormatStrFormatter('%d')
      minorLocator = MultipleLocator(5)

      self.ax = plt
      self.ax.cla()
      #plt.style.use('classic')

      self.ax.ylabel('Voltage [V]')
      self.ax.xlabel(self.xlabel)
      self.ax.title(self.testitem+':'+self.result+'       '+time.asctime( time.localtime(time.time()) ))
      self.ax.plot(self.x,self.yv,color="brown")
      self.ax.xlim(0, self.xvalue)
   #ax.xaxis.set_major_locator(majorLocator)
   #ax.xaxis.set_major_formatter(majorFormatter)
   #ax.xaxis.set_minor_locator(minorLocator)
   #ax.yaxis.set_major_locator(majorLocator)
   #ax.yaxis.set_major_formatter(majorFormatter)
   #ax.yaxis.set_minor_locator(minorLocator)

      self.ax.savefig(self.path+ self.testitem+r'.png' )
      #plt.show()

   def getvolumelinear(self,testset):
       instmodelsel = testset[0]
       channel = testset[1]
       self.getvalue_item = testset[2]
       self.inst = self.rm.open_resource(instmodelsel)
       p = serial.Serial(port = self.uartport,baudrate=self.baudrate)  #,bytesize=8,parity='PARITY_NONE',stopbits=1,timeout=60
       #self.cmd = [0x7F, 0x08, 0x99, 0xA2, 0xB3, 0xC4, 0x02, 0xFF, 0x05, 0x00, 0xCF]

       if ('VGA' in self.getvalue_item) |('FR' in self.getvalue_item) :
           grinst = self.rm.open_resource('USB0::0x1AB1::0x0641::DG4E183950006::INSTR')    #信号发生器
           grinst.write(':FUNC SIN')
           grinst.write(':VOLT:HIGH 1.414')
           grinst.write(':VOLT:LOW 0')
           grinst.write(':FREQ 1000')
           grinst.write(':OUTP ON')
           self.setvol[-2] = 100
           p.write(self.setvol)
       print('getvolume')
       self.inst.write(':CHAN'+channel[0]+':DISP 1')
       self.inst.write(':CHAN' + channel[1] + ':DISP 1')
       self.inst.write(':TIMebase:SCAL ' + '0.0002')
       self.inst.write(':CHAN' + channel[0] + ':SCAL ' + '5')
       self.inst.write(':CHAN' + channel[1] + ':SCAL ' + '5')

       self.f = open(self.getvalue_item + '.txt', 'w')
       volumedata = []
       for i in range(0, 101):
           if 'FR' in self.getvalue_item:
               grinst.write(':FREQ '+str(100*(1.055**i)))
               if i <38:
                   self.inst.write(':TIMebase:SCAL ' + '0.001')
               elif i>=38 & i<75:
                   self.inst.write(':TIMebase:SCAL ' + '0.0002')
               elif i>=75:
                   self.inst.write(':TIMebase:SCAL ' + '0.0001')
           else:
               self.setvol[-2] = i
               p.write(self.setvol)
               if i < 20:
                    self.inst.write(':CHAN' + channel[0]+ ':SCAL ' + '2')
                    self.inst.write(':CHAN' + channel[1]+ ':SCAL ' + '2')
               else:
                    self.inst.write(':CHAN' + channel[0]+ ':SCAL ' + '5')
                    self.inst.write(':CHAN' + channel[1] + ':SCAL ' + '5')
           self.inst.write(':RUN')
           time.sleep(2.5)
           self.inst.write(':STOP')
           time.sleep(0.5)
           self.inst.write(':WAVeform:SOURce CHANnel' + channel[0])
           time.sleep(0.5)
           self.inst.write(":WAVeform:DATA?")
           self.data1 = self.inst.read_raw()
           print(self.data1[0:20])
           self.inst.write(':WAVeform:SOURce CHANnel' + channel[1])
           self.inst.write(":WAVeform:DATA?")
           self.data2 = self.inst.read_raw()
           print(self.data2[0:20])
           preambledata = self.inst.query(":WAVeform:PREamble?")
           pbdata = preambledata.split(',')
           d1 = np.array(list(self.data1[11:-1]))
           d2 = np.array(list(self.data2[11:-1]))
           d = d1 - d2
           # print(pbdata[-3])
           dd = d * d

           dmean = np.mean(dd)
           dsqrt = np.sqrt(dmean)
           mean = (dsqrt) * float(pbdata[-3])
           volumedata.append(mean)
           print('音量为' + str(i) + ' 时均方根值：' + str(mean))

       self.f.write(str(volumedata))
       print(volumedata)
       self.f.close()
       p.close()

       self.x = np.arange(0,101)
       if 'FR' in self.getvalue_item:
           self.x=[]
           for i in range(0,101):
                self.x.append( 100*1.055**i)
       print(self.x)
       self.xlabel = 'Volume'
       if 'FR' in self.getvalue_item:
           self.xlabel ='Frequence'
       self.ax = plt
       self.ax.figure(figsize=(10, 5))
       self.ax.cla()
       # plt.style.use('classic')
       self.ax.ylabel('Vrms @1kHz -10dB')
       self.ax.xlabel(self.xlabel)
       self.ax.title(self.getvalue_item + '       ' + time.asctime(time.localtime(time.time())))
       if 'FR' in self.getvalue_item:
           self.ax.semilogx(self.x,volumedata,'--b*')
           self.ax.grid(True)
       else:
           self.ax.plot(self.x, volumedata, color="brown")
       self.ax.savefig('.\\file\\'  + self.getvalue_item + r'.png')

   def getbllinear(self, testset):
       instmodelsel = testset[0]
       channel = testset[1]
       self.inst = self.rm.open_resource(instmodelsel)
       print('getbacklight')
       self.inst.write(':CHAN' + channel[0] + ':DISP 1')   #adj
       self.inst.write(':CHAN' + channel[1] + ':DISP 1')    #current
       self.inst.write(':CHAN' + channel[2] + ':DISP 1')    #voltage
       self.inst.write(':TIMebase:SCAL ' + '0.002')

       p = serial.Serial(port=self.uartport,baudrate=self.baudrate)  # ,bytesize=8,parity='PARITY_NONE',stopbits=1,timeout=60
       # self.cmd = [0x7F, 0x08, 0x99, 0xA2, 0xB3, 0xC4, 0x02, 0xFF, 0x05, 0x00, 0xCF]
       self.getvalue_item = testset[2]
       self.f = open(self.getvalue_item + '.txt', 'w')
       volumedata = []
       self.inst.write(':CHAN' + channel[0] + ':SCAL ' + '2')
       self.inst.write(':CHAN' + channel[1] + ':SCAL ' + '0.2')
       self.inst.write(':CHAN' + channel[2] + ':SCAL ' + '50')
       Label = ['ADJ', 'CURR', 'VOLT']
       signal = 'BL'
       volt=[]
       curr=[]
       adjfreq=[]
       adjduty=[]
       for i in range(0, 101):
           self.setbl[-2] = i
           p.write(self.setbl)

           self.inst.write(':RUN')
           time.sleep(2.5)
           self.inst.write(':STOP')
           time.sleep(0.5)
           if i in [0,25,50,75,100,101]:
                self.datatofigure(signal + ' bl adj '+str(i), channel[0], Label[0])
                time.sleep(1)
                self.datatofigure(signal + ' bl curr ' + str(i), channel[1], Label[1])
                time.sleep(1)
                self.datatofigure(signal + ' bl volt ' + str(i), channel[2], Label[2])
                time.sleep(1)


           v = self.inst.query(':MEASure:VRMS? ' + 'CHAN' + channel[2])
           volt.append(float(v))
           c = self.inst.query(':MEASure:VRMS? ' + 'CHAN' + channel[1])
           curr.append(float(c))
           f = self.inst.query(':MEASure:FREQ? ' + 'CHAN' + channel[0])
           adjfreq.append(float(f))
           d = self.inst.query(':MEASure:PDUT? ' + 'CHAN' + channel[0])
           adjduty.append(float(d))
           print('亮度为' + str(i) + ' 电流：' + str(c))

       self.f.write(str(volt)+'\n')
       self.f.write(str(curr) + '\n')
       self.f.write(str(adjfreq)+ '\n' )
       self.f.write(str(adjduty) )
       print(volt)
       self.f.close()
       p.close()

       self.x = np.arange(0, 101)
       print(self.x)
       self.xlabel = 'Back Light'
       self.ax = plt
       self.ax.figure(figsize=(10, 5))
       self.ax.cla()
       # plt.style.use('classic')
       self.ax.ylabel('Crms ')
       self.ax.xlabel(self.xlabel)
       self.ax.title(self.getvalue_item + '       ' + time.asctime(time.localtime(time.time())))
       self.ax.plot(self.x, curr, color="brown")
       self.ax.savefig('.\\file\\' + self.getvalue_item+'_current' + r'.png')
       self.ax.cla()
       # plt.style.use('classic')
       self.ax.ylabel('DUTY ')
       self.ax.xlabel(self.xlabel)
       self.ax.title(self.getvalue_item + '       ' + time.asctime(time.localtime(time.time())))
       self.ax.plot(self.x, adjduty, color="brown")
       self.ax.savefig('.\\file\\' + self.getvalue_item +'_adjduty'+ r'.png')
       self.ax.cla()
       # plt.style.use('classic')
       self.ax.ylabel('freq ')
       self.ax.xlabel(self.xlabel)
       self.ax.title(self.getvalue_item + '       ' + time.asctime(time.localtime(time.time())))
       self.ax.plot(self.x, adjfreq, color="brown")
       self.ax.savefig('.\\file\\' + self.getvalue_item +'_adjfreq'+ r'.png')






