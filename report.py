import os

class report:
     def __init__(self,signal,cata):
        self.testsignal=signal
        self.testcata=cata
     def go(self):
        a = os.listdir(r'./file')
        print(a)
        datafile = os.listdir(r'./data')
        print(datafile)
        allfile = a + datafile
        print(allfile)

        # testsignal = [['5VSB', '5V_NORMAL', '12V', '18VA', '18VB'], ['STANDBY', 'NORMAL'],
        # ['PS_ON,5V_NORMAL,12V,18V', 'BL_ONOFF,12V_PANEL,VBY1-D1,BL_ADJ', '5V_OPS,OPS_OK,OPS_ONOFF,OPS_DET'],
        # ['OPS_OK', 'OPS_ONOFF', 'OPS_DET', 'BL_ONOFF', 'BL_ADJ', 'PS_ON', 'LED_R', 'LED_G', 'IR', 'KEY0'],
        # ['UART1_TX', 'UART1_RX', 'OPS_TX', 'OPS_RX'], ['HDMI_LINEAR', 'VGA_LINEAR', 'VGA_FR'], ['BL_LINEAR']]
        # testcata = ['DC_TEST', 'AC_TEST', 'SEQUENCE_TEST', 'GPIO_TEST', 'UART_TEST', 'AUDIO_TEST', 'BL_TEST']
        dcnum = len(self.testsignal[self.testcata.index('DC_TEST')])

        standf = open('standard.txt', 'r')
        stand = standf.readlines()
        standf.close()
        dcstandsignal = []
        blstandsignal = []
        for i in stand:
            if '+++DC' in i:
                for j in range(2, dcnum + 2):
                    dcstandsignal.append(stand[(stand.index(i)) + j][:-1])
            if '+++BL' in i:
                for j in range(2, 3):
                    blstandsignal.append(stand[stand.index(i) + j][:-1])
        print(dcstandsignal)
        print(blstandsignal)
        dcbl = dcstandsignal + blstandsignal
        ss = []
        for i in range(0, dcnum + 1):
            j = (dcbl[i].replace('\t', '')).split()
            ss.append(j)
        print(ss)
        dcbldic = {}
        for i in ss:
            dcbldic[i[0]] = list(map(float, i[1:]))
        print(dcbldic)

        filefst = '<br /><DIV class="TESTHEADER"><SPAN class="passfail"><img src="./file/'
        filesec = '.gif" /></SPAN><SPAN class="testname">'
        filetrd = '</SPAN><SPAN class="SpecReference">Reference:Test ID '
        filefor = '</SPAN></DIV><br style="clear:both" /><SPAN class="TestDescription"><SPAN class="TestSummary"><span style="valign:top;padding-left:2pt;padding-right:2pt;background-color=black;color:white;">Test Summary:</span><span class="'
        filefif = '</span></SPAN><span><span style="margin-left:4px;valign:top;flow:left;padding-top:0px;padding-left:4px;padding-right:4px">Test Description:</span>' + '<span style="text-indent:2em;margin-left:6px;margin-right:4px"><nbsp />'
        filesix = '</span></span>' + '<br style="clear:both" /><br style="clear:both" /><SPAN class="FieldValueBlock"><span class="Field">Pass Limits:</span><span class="Value"> '
        filesev = '</span></SPAN><SPAN class="FieldValueBlock"><span class="Field">'
        fileeig = '</span><span class="Value">'
        filenin = '</span></SPAN></SPAN><DIV style="clear:both" /><DIV class="ReferenceDivider"><span class="ReferenceDividerSpan">Result Details:</span></DIV>'
        fileten = '<td><img src="' + r'./file/'

        infonum = 0
        failnum = 0
        passnum = 0
        totalnum = 0
        detailwr = {}
        tablewr = {}
        for i in self.testsignal:
            for j in i:  # each signal
                if self.testcata[self.testsignal.index(i)] == 'DC_TEST':
                    para = ['voltage', 'current', 'ripple', 'inrush current']
                    desc = ['When is working on full load and light load', 'full load', '20MHz', 'power off and on ']
                    pic = []
                    for k in datafile:
                        if j in k:
                            print(j + ' have tested')
                            for m in range(0, 4):
                                for p in a:
                                    if (j in p) and ((para[m][0:3]).lower() in p.lower()):
                                        pic.append(p)
                            print('pic')
                            print(pic)
                            recordf = open(r'./data/' + k, 'r')
                            record = recordf.readlines()
                            recordf.close()
                            rec = record[1:]
                            volt = float(rec[0][:-1])
                            curr = '{:.5f}'.format(float(rec[1][:-1]))
                            ripp = float(rec[2][:-1])
                            rush = float(rec[3][:-1])
                            testvalue = [rec[0][:-1], rec[1][:-1], rec[2][:-1], rec[3][:-1]]
                            b = dcbldic[j]
                            sta = ['<' + str(b[1]) + ' and ' + '>' + str(b[0]), '<' + str(b[3]), '<' + str(b[4]),
                                   '<' + str(b[5])]
                            flag = []
                            for n in range(0, 4):
                                if n == 0:
                                    if volt >= b[0] and volt <= b[1]:
                                        failnum = failnum + 1
                                        flag.append('fail')
                                    else:
                                        passnum = passnum + 1
                                        flag.append('pass')
                                    totalnum = totalnum + 1
                                else:
                                    if float(rec[n][:-1]) >= b[n + 2]:
                                        failnum = failnum + 1
                                        flag.append('fail')
                                    else:
                                        passnum = passnum + 1
                                        flag.append('pass')
                                    totalnum = totalnum + 1
                                print(flag)
                                # detailwr[totalnum]=' '
                                tablewr[totalnum] = '<tr>\n ' + '<td >' + '<img src="' + r'./file/' + flag[
                                    n] + '.gif"></td><td >' + \
                                                    self.testcata[self.testsignal.index(i)] + ':  ' + j + ' ' + para[
                                                        n] + '</td><td>' + \
                                                    str('{:.5f}'.format(float(rec[n][:-1]))) + '</td><td>' + sta[
                                                        n] + '</td></tr>'
                                detailwr[totalnum] = filefst + flag[n] + filesec + self.testcata[
                                    self.testsignal.index(i)] + ':  ' + j + ' ' + para[n] + filetrd + \
                                                     self.testcata[self.testsignal.index(i)] + filefor + flag[
                                                         n] + '">' + flag[
                                                         n] + filefif + desc[n] + filesix + sta[n] + \
                                                     filesev + para[n] + fileeig + str(
                                    '{:.5f}'.format(float(rec[n][:-1]))) + filenin + fileten + pic[n] + '"></td><br />'
                if (self.testcata[self.testsignal.index(i)] == 'GPIO_TEST') or (
                        self.testcata[self.testsignal.index(i)] == 'UART_TEST'):
                    if (self.testcata[self.testsignal.index(i)] == 'GPIO_TEST'):
                        sta = ['<5V' + ' and ' + '>2.4V', '<0.4V']
                        para = ['max voltage', 'min voltage']
                        desc = ['When is working on full load and light load', 'full load and light load']
                        num = 2
                    else:
                        sta = ['<5V' + ' and ' + '>2.4V', '<0.4V', '<1us', '<1us']
                        para = ['max voltage', 'min voltage', 'rise time', 'fall time']
                        desc = ['When is working on full load and light load', 'full load and light load',
                                'just send signal', 'just send signal']
                        num = 4
                    pic = []
                    for k in datafile:
                        if j in k:
                            print(j + ' have tested')
                            for m in range(0, num):
                                for p in a:
                                    if (j in p) and ((para[m][0:3]).lower() in p.lower()) and (',' not in p):
                                        pic.append(p)
                            print('pic')
                            print(pic)
                            recordf = open(r'./data/' + k, 'r')
                            record = recordf.readlines()
                            recordf.close()
                            rec = record[1:]
                            maxv = float(rec[0][:-1])
                            minv = float(rec[1][:-1])
                            if (self.testcata[self.testsignal.index(i)] == 'GPIO_TEST'):
                                testvalue = [rec[0][:-1], rec[1][:-1]]
                            else:
                                testvalue = [rec[0][:-1], rec[1][:-1], rec[2][:-1], rec[4][:-1]]
                            flag = []
                            for n in range(0, num):
                                if n == 0:
                                    if maxv >= 2.4 and maxv <= 5:
                                        failnum = failnum + 1
                                        flag.append('fail')
                                    else:
                                        passnum = passnum + 1
                                        flag.append('pass')
                                    totalnum = totalnum + 1
                                else:
                                    if float(rec[n][:-1]) >= 0.4:
                                        failnum = failnum + 1
                                        flag.append('fail')
                                    else:
                                        passnum = passnum + 1
                                        flag.append('pass')
                                    totalnum = totalnum + 1
                                print(flag)
                                # detailwr[totalnum]=' '
                                tablewr[totalnum] = '<tr>\n ' + '<td >' + '<img src="' + r'./file/' + flag[
                                    n] + '.gif"></td><td >' + \
                                                    self.testcata[self.testsignal.index(i)] + ':  ' + j + ' ' + para[
                                                        n] + '</td><td>' + str(
                                    '{:.5f}'.format(float(rec[n][:-1]))) + '</td><td>' + \
                                                    sta[n] + '</td></tr>'
                                detailwr[totalnum] = filefst + flag[n] + filesec + self.testcata[
                                    self.testsignal.index(i)] + ':  ' + j + ' ' + para[n] + filetrd + \
                                                     self.testcata[self.testsignal.index(i)] + filefor + flag[
                                                         n] + '">' + flag[
                                                         n] + filefif + desc[n] + filesix + sta[n] + \
                                                     filesev + para[n] + fileeig + str(
                                    '{:.5f}'.format(float(rec[n][:-1]))) + filenin + fileten + pic[n] + '"></td><br />'
                if self.testcata[self.testsignal.index(i)] == 'SEQUENCE_TEST':
                    para = ['uart power on', 'uart power on 0.05s', 'uart power off', 'uart power off 0.02s', 'ac on',
                            'ac on 0.05s', 'ac off', 'ac off 0.05s']
                    desc = ['uart power on', 'uart power on', 'uart power off', 'uart power off', 'ac on', 'ac on',
                            'ac off', 'ac off']
                    pic = []
                    for p in a:
                        if j in p:
                            print(j + ' have tested')
                            if (j in p) and ('pon' in p.lower()):
                                pic.append(p)
                            if (j in p) and ('pon' in p.lower()) and ('0.0s' in p.lower()):
                                pic.append(p)
                            if (j in p) and ('poff' in p.lower()):
                                pic.append(p)
                            if (j in p) and ('poff' in p.lower()) and ('0.0s' in p.lower()):
                                pic.append(p)
                            if (j in p) and ('ac_on' in p.lower()):
                                pic.append(p)
                            if (j in p) and ('ac_on' in p.lower()) and ('0.0s' in p.lower()):
                                pic.append(p)
                            if (j in p) and ('ac_off' in p.lower()):
                                pic.append(p)
                            if (j in p) and ('ac_off' in p.lower()) and ('0.0s' in p.lower()):
                                pic.append(p)
                    print('pic')
                    print(pic)
                    testvalue = ['info'] * len(pic)
                    sta = ['info'] * len(pic)
                    flag = ['info'] * len(pic)
                    rec = ['info '] * len(pic)
                    print(flag)
                    # detailwr[totalnum]=' '
                    for n in range(0, len(pic)):
                        infonum = infonum + 1
                        totalnum = totalnum + 1
                        tablewr[totalnum] = '<tr>\n ' + '<td >' + '<img src="' + r'./file/' + flag[
                            n] + '.gif"></td><td >' + \
                                            self.testcata[self.testsignal.index(i)] + ':  ' + j + ' ' + para[
                                                n] + '</td><td>' + \
                                            rec[n][:-1] + '</td><td>' + sta[n] + '</td></tr>'
                        detailwr[totalnum] = filefst + flag[n] + filesec + self.testcata[
                            self.testsignal.index(i)] + ':  ' + j + ' ' + \
                                             para[n] + filetrd + \
                                             self.testcata[self.testsignal.index(i)] + filefor + flag[n] + '">' + flag[
                                                 n] + filefif + \
                                             desc[n] + filesix + sta[n] + \
                                             filesev + para[n] + fileeig + rec[n][:-1] + filenin + fileten + pic[
                                                 n] + '"></td><br />'
                if self.testcata[self.testsignal.index(i)] == 'AUDIO_TEST':
                    if 'FR' in j:
                        para = ['frequence response']
                        desc = ['HDMI -10dB 1kHz, VGA 0.5Vpp 1KHz']
                    if 'LINEA' in j:
                        para = ['volume non_linear']
                        desc = ['HDMI 0dB 1KHz,VGA 0.5Vrms 1KHz,volume from 0 to 100']
                    pic = []
                    for p in a:
                        if j in p:
                            print(j + ' have tested')
                            pic.append(p)
                            print('pic')
                            print(pic)
                            testvalue = ['info']
                            sta = ['info']
                            flag = ['info']
                            rec = ['info ']
                            print(flag)
                            # detailwr[totalnum]=' '
                            infonum = infonum + 1
                            totalnum = totalnum + 1
                            n = 0
                            tablewr[totalnum] = '<tr>\n ' + '<td >' + '<img src="' + r'./file/' + flag[
                                n] + '.gif"></td><td >' + \
                                                self.testcata[self.testsignal.index(i)] + ':  ' + j + ' ' + para[
                                                    n] + '</td><td>' + \
                                                rec[n][:-1] + '</td><td>' + sta[n] + '</td></tr>'
                            detailwr[totalnum] = filefst + flag[n] + filesec + self.testcata[
                                self.testsignal.index(i)] + ':  ' + j + ' ' + para[n] + filetrd + \
                                                 self.testcata[self.testsignal.index(i)] + filefor + flag[n] + '">' + \
                                                 flag[
                                                     n] + filefif + desc[n] + filesix + sta[n] + \
                                                 filesev + para[n] + fileeig + rec[n][:-1] + filenin + fileten + pic[
                                                     n] + '"></td><br />'
                if self.testcata[self.testsignal.index(i)] == 'BL_TEST':
                    print('enter in bl_test --------------------------------')
                    para = ['backlight adj duty', 'backlight adj freq', 'backlight current', 'backlight voltage']
                    desc = ['backlight from 0 to 100', 'backlight from 0 to 100', 'backlight from 0 to 100',
                            'backlight from 0 to 100']
                    pic = []
                    for p in a:
                        if 'BL' in p:
                            print(j + ' have tested')
                            if 'adjduty' in p.lower():
                                pic.append(p)
                            if 'adjfreq' in p.lower():
                                pic.append(p)
                            if 'current' in p.lower():
                                pic.append(p)
                            if 'voltage' in p.lower():
                                pic.append(p)
                    print('pic')
                    print(pic)
                    bl_adj = ['Backlight adj']
                    bl_curr = ['Backlight current']
                    bl_volt = ['Backlight voltage']
                    for t in ['_0_', '25_', '50_', '75_', '100_']:
                        for s in a:
                            if 'BL' in s and 'adj' in s and t in s:
                                bl_adj.append(s)
                            elif 'BL' in s and 'curr' in s and t in s:
                                bl_curr.append(s)
                            elif 'BL' in s and 'volt' in s and t in s:
                                bl_volt.append(s)
                    print(bl_adj)
                    print(bl_curr)
                    print(bl_volt)
                    bl_title = ['Backlight set', '0', '25', '50', '75', '100']
                    bl = [bl_title, bl_adj, bl_curr, bl_volt]
                    b = open('BL_LINEA.txt', "r")
                    bldata = b.readlines()
                    b_duty = (bldata[3][1:-1]).split(',')
                    b_duty = map(eval, b_duty)
                    bd = list(b_duty)
                    print(bd)
                    b_freq = (bldata[2][1:-2]).split(',')
                    b_freq = map(eval, b_freq)
                    bf = list(b_freq)
                    print(bf)
                    b_volt = (bldata[0][1:-2]).split(',')
                    b_volt = map(eval, b_volt)
                    bv = list(b_volt)
                    print(bv)
                    b_curr = (bldata[1][1:-2]).split(',')
                    b_curr = map(eval, b_curr)
                    bc = list(b_curr)
                    print(bc)
                    b.close()
                    print(max(bc))
                    print(min(bc))
                    print(max(bf))
                    print(min(bf))
                    print(max(bv))
                    print(min(bv))
                    rec = [max(bd), min(bd), max(bf), min(bf), max(bc), min(bc), max(bv), min(bv)]
                    print('rec')
                    print(rec)
                    sta = [1, 0.2, 180.02, 179.98, dcbldic['LED'][3], dcbldic['LED'][2], dcbldic['LED'][1],
                           dcbldic['LED'][0]]
                    flag = []
                    # detailwr[totalnum]=' '
                    for n in range(0, 4):
                        if (rec[n * 2] <= sta[n * 2]) and (rec[n * 2 + 1] >= sta[n * 2 + 1]):
                            flag.append('pass')
                            passnum = passnum + 1
                            totalnum = totalnum + 1
                        else:
                            flag.append('fail')
                            failnum = failnum + 1
                            totalnum = totalnum + 1
                        tablewr[totalnum] = '<tr>\n ' + '<td >' + '<img src="' + r'./file/' + flag[
                            n] + '.gif"></td><td >' + \
                                            self.testcata[self.testsignal.index(i)] + ':  ' + j + ' ' + para[
                                                n] + '</td><td>' + \
                                            'max ' + str(rec[2 * n]) + ' min ' + str(
                            rec[2 * n + 1]) + '</td><td>' + '<=' + str(sta[2 * n]) + ' and ' + '>=' + str(
                            sta[2 * n + 1]) + '</td></tr>'
                        detailwr[totalnum] = filefst + flag[n] + filesec + self.testcata[
                            self.testsignal.index(i)] + ':  ' + j + ' ' + \
                                             para[n] + filetrd + \
                                             self.testcata[self.testsignal.index(i)] + filefor + flag[n] + '">' + flag[
                                                 n] + filefif + \
                                             desc[n] + filesix + '<=' + str(sta[2 * n]) + ' and ' + '>=' + str(
                            sta[2 * n + 1]) + \
                                             filesev + para[n] + fileeig + 'max ' + str(rec[2 * n]) + ' min ' + str(
                            rec[2 * n + 1]) + filenin + fileten + pic[n] + '"></td><br />'
                    flag = ['info']
                    para = ['backlight non-linear']
                    infonum = infonum + 1
                    totalnum = totalnum + 1
                    n = 0
                    tablewr[totalnum] = '<tr>\n ' + '<td >' + '<img src="' + r'./file/' + flag[n] + '.gif"></td><td >' + \
                                        self.testcata[self.testsignal.index(i)] + ':  ' + j + ' ' + para[
                                            n] + '</td><td>' + \
                                        'info' + '</td><td>' + 'info' + '</td></tr>'
                    detailwr[totalnum] = filefst + flag[n] + filesec + self.testcata[
                        self.testsignal.index(i)] + ':  ' + j + ' ' + \
                                         para[n] + filetrd + \
                                         self.testcata[self.testsignal.index(i)] + filefor + flag[n] + '">' + flag[
                                             n] + filefif + \
                                         desc[n] + filesix + '<=' + str(sta[n]) + ' and ' + '>=' + str(sta[n + 1]) + \
                                         filesev + para[n] + fileeig + 'info' + filenin

                    detailwr[totalnum] = detailwr[totalnum] + ' <table border="1">\n'  # backlight picture table
                    for m in range(0, 4):
                        detailwr[totalnum] = detailwr[totalnum] + '<tr>\n '
                        for n in range(0, 6):
                            if m == 0 or n == 0:
                                detailwr[totalnum] = detailwr[totalnum] + '<td align ="center">' + bl[m][n] + '</td>'
                            else:
                                detailwr[totalnum] = detailwr[totalnum] + '<td><img src="' + r'./file/' + bl[m][
                                    n] + '" width="200" height="120"' + '></td>'
                        detailwr[totalnum] = detailwr[totalnum] + '</tr>\n '
                    detailwr[totalnum] = detailwr[totalnum] + ' </table>\n'

        f = open('setup_app.txt', 'r')
        testconfigcontent = f.readlines()
        f.close()
        testconfigtitle = ['Model name', 'Duration', 'Main board', 'Power Supply', 'Panel', 'Keyboard', \
                           'OPS con board', 'Touch board', 'F/W', 'Who Test ', 'Test time']
        print(len(testconfigtitle))

        if failnum == 0:
            overallresult = "Pass"
        else:
            overallresult = 'Fail'

        f = open('webfirst.html', 'w')
        f.write('<html>\n')
        f.write('<head><link id="ss1" href="file/Compact.css" rel="stylesheet" type="text/css" />\
            <link id="sscommon" href="file/common.css" rel="stylesheet" \
            type="text/css" /><link rel="stylesheet" href="file/print.css" media="print" /></head>')
        f.write('<body>\n')
        f.write('<img src="hht.jpg"/>\n')
        f.write('<h1 align="center" > Interactive Panel Test Result </h1>')
        f.write(
            '<p style="margin:0.25em"><center><b>Overall Result: </b><span class="' + overallresult + '">' + overallresult + '</span></center></p>\n')

        f.write(' <table align="center" border="1" >\n')  # configure
        f.write('<tr bgcolor="grey">\n ')
        f.write('<th  colspan="2" align ="center">Test Configure Details</th>')
        f.write('</tr>\n ')
        for i in range(0, 11):
            f.write('<tr>\n ')
            f.write('<td bgcolor="grey">' + testconfigtitle[i] + '</td>')
            f.write('<td align ="center">' + testconfigcontent[i][:-1] + '</td>')
            f.write('</tr>\n ')
        f.write(' </table>\n')

        f.write('<h2 style="page-break-before:always">Summary of Results</h2>\n')
        f.write('<table border="1">')
        f.write('<tr>\n')
        f.write('<th  bgcolor="grey" colspan="2" align ="center">Test Statistics</th>')
        f.write('</tr>\n')
        f.write('<tr>\n')
        f.write('<td >Pass</td><td>' + str(passnum) + '</td>')
        f.write('</tr>\n')
        f.write('<tr>\n')
        f.write('<td >Fail</td><td>' + str(failnum) + '</td>')
        f.write('</tr>\n')
        f.write('<tr>\n')
        f.write('<td >Info</td><td>' + str(infonum) + '</td>')
        f.write('</tr>\n')
        f.write('<tr>\n')
        f.write('<td >Total</td><td>' + str(totalnum) + '</td>')
        f.write('</tr>\n')
        f.write('</table>')
        f.write(' <br />')
        f.write(' <br />')

        f.write(' \n')
        f.write(' \n')
        f.write('<a name="OverallSummaryTable" />')
        f.write('<table border="1">')
        f.write('<tr bgcolor="grey">\n')
        f.write('<th >Pass</th><th>Test name</th><th>Actual Value</th><th>Limit</th>')
        f.write('</tr>\n')
        for i in range(1, totalnum + 1):
            if i % 2 == 0:
                f.write(tablewr[i][:3] + ' bgcolor="grey"' + tablewr[i][3:])
                print(tablewr)
            else:
                f.write(tablewr[i])
        f.write('</table>')
        f.write(' <br />')

        f.write('<h2 style="page-break-before:always">Results Detail</h2>\n')

        fgfir = '<span class="Navigation"><a href="#OverallSummaryTable">Top</a></span>'
        fgsec = '<span class="Navigation"><a href="&#xA;                     #'
        # 'Test20000'
        fgthd = '">Previous  </a></span><a name="'
        # 'EndTest20000'
        fgfor = '"/><a name="'
        #  'Test20100'
        fgfif = '"/><span class="Navigation"><a href="&#xA;  #'
        # 'EndTest20100'
        fglas = '">Next</a></span>'  # <br />

        for i in range(1, totalnum + 1):
            f.write(fgfir)
            if i == 1 and totalnum >= 2:
                f.write(fgfor[3:] + str(i) + fgfif + 'end' + str(i) + fglas)
            elif i > 1 and totalnum >= i + 1:
                f.write(
                    fgsec + str(i - 1) + fgthd + 'end' + str(i - 1) + fgfor + str(i) + fgfif + 'end' + str(i) + fglas)
            elif i == totalnum:
                f.write(fgsec + str(i - 1) + fgthd + 'end' + str(i - 1) + fgfor[0:3])
            print(detailwr)
            f.write(detailwr[i])
        print('totalnum')
        print(totalnum)
        print('pass')
        print(passnum)
        print(failnum)
        print(infonum)

        f.write('</body>\n')
        f.write('</html>\n')
        f.close()
if __name__ == '__main__':
    testsignal = [['5VSB', '5V_NORMAL', '12V', '18VA', '18VB'], ['STANDBY', 'NORMAL'],
                  ['PS_ON,5V_NORMAL,12V,18V', 'BL_ONOFF,12V_PANEL,VBY1-D1,BL_ADJ', '5V_OPS,OPS_OK,OPS_ONOFF,OPS_DET'],
                  ['OPS_OK', 'OPS_ONOFF', 'OPS_DET', 'BL_ONOFF', 'BL_ADJ', 'PS_ON', 'LED_R', 'LED_G', 'IR', 'KEY0'],
                  ['UART1_TX', 'UART1_RX', 'OPS_TX', 'OPS_RX'], ['HDMI_LINEAR', 'VGA_LINEAR', 'VGA_FR'], ['BL_LINEAR']]
    testcata = ['DC_TEST', 'AC_TEST', 'SEQUENCE_TEST', 'GPIO_TEST', 'UART_TEST', 'AUDIO_TEST', 'BL_TEST']
    rep=report(testsignal,testcata)
    rep.go()

