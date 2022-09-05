import datetime
import tkinter
from tkinter import *
import tkinter.ttk as ttk
import urllib.request
import xml.dom.minidom
import datetime
from datetime import *
import matplotlib
import dateutil.relativedelta
import matplotlib.pyplot as plot
###
import matplotlib.pyplot as plt

window = Tk()
window.title("THE CALCULATOR")
#window.resizable(width=False, height=False)
window.geometry("1080x640")
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Калькулятор валюты")
tab_control.add(tab2, text="Динамика курса")

now = datetime.now()
print('Сегодня:', now)
print(now.year)
if now.day < 10:
    u = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + "0" + str(now.day) + '/' + '0' + str(
        now.month) + '/' + str(
        now.year)
else:
    u = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + str(now.day) + '/' + '0' + str(
        now.month) + '/' + str(now.year)
res = urllib.request.urlopen(str(u))
dom = xml.dom.minidom.parse(res)
dom.normalize()
nodeArray = dom.getElementsByTagName("Valute")
currency = {}
count = 0
keylog = []
for node in nodeArray:
    childList = node.childNodes
    for child in childList:
        if child.nodeName == 'Name':
            currency.update({child.childNodes[0].nodeValue:0})
        if child.nodeName == 'Value':
            value = child.childNodes[0].nodeValue.replace(',', '.')
            currency.update({list(currency)[-1]:value})
for key in currency.keys():
    keylog.append(key)
print(currency)
print(u)

def GetCurrencyIdList(cur):
    u = 'http://www.cbr.ru/scripts/XML_val.asp?d=0'
    res = urllib.request.urlopen(str(u))
    dom = xml.dom.minidom.parse(res)
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Item")
    currency_id = {}
    for node in nodeArray:
        childList = node.childNodes
        for child in childList:
            if child.nodeName == 'Name':
                currency_id.update({child.childNodes[0].nodeValue: 0})
            if child.nodeName == 'ParentCode':
                value = child.childNodes[0].nodeValue.replace('    ', '')
                currency_id.update({list(currency_id)[-1]: value})
    return currency_id.get(cur)

def SwitchDate():
    now = datetime.now()
    if r_var.get() == 0:
        print('МЕНЯЕМ МАСШТАБ')
        x = []
        for i in range(4):
            delta = dateutil.relativedelta.relativedelta(days=7)
            x.append(
                f'{(now - delta).strftime("%d")}.{(now - delta).strftime("%m")}.{(now - delta).year}-{now.strftime("%d")}.{now.strftime("%m")}.{now.year}')
            now = now - delta
        date_switch['values'] = x
    if r_var.get() == 1:
        print('МЕНЯЕМ МАСШТАБ')
        x = []
        for i in range(4):
            delta = dateutil.relativedelta.relativedelta(months=1)
            x.append(f'{(now-delta).strftime("%m")}')
            now = now - delta
        date_switch['values'] = x
    if r_var.get() == 2:
        print('МЕНЯЕМ МАСШТАБ')
        x = []
        delta = dateutil.relativedelta.relativedelta(months=1)
        while (now).strftime("%m") != '01':
            now = now - delta
        for i in range(4):
            delta = dateutil.relativedelta.relativedelta(months=3)
            x.append(f'{(now).strftime("%m")}')
            now = now + delta
        date_switch['values'] = x
    if r_var.get() == 3:
        print('МЕНЯЕМ МАСШТАБ')
        x = []
        for i in range(4):
            delta = dateutil.relativedelta.relativedelta(years=1)
            x.append(f"{now.year}")
            now = now - delta
        date_switch['values'] = x

def GetCurrencyCurs_1():
    cur = cur_switch.get()
    id = GetCurrencyIdList(cur)
    dat = date_switch.get().split('-')
    date_req = []
    for i in dat:
        date_req.append(i.replace('.', '/'))
    u = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=' + date_req[0] + '&date_req2=' + date_req[1] + '&VAL_NM_RQ=' + str(id)
    print(u)
    res = urllib.request.urlopen(str(u))
    dom = xml.dom.minidom.parse(res)
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Record")
    curs_list = []
    for node in nodeArray:
        childList = node.childNodes
        for child in childList:
            if child.nodeName == 'Value':
                curs_list.append(float(child.childNodes[0].nodeValue.replace(',', '.')))
    print(curs_list)
    return curs_list

def GetCurrencyCurs_2():
    cur = cur_switch.get()
    month = date_switch.get()
    if int(month) % 2 == 1:
        day = '31'
    elif (int(month) % 2 == 0) & (int(month) != 2):
        day = '30'
    elif month == '02':
        day = '28'
    id = GetCurrencyIdList(cur)
    u = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=' + '01/' + month + '/2021' + '&date_req2=' + day + '/' + month + '/2021' + '&VAL_NM_RQ=' + str(id)
    print(u)
    res = urllib.request.urlopen(str(u))
    dom = xml.dom.minidom.parse(res)
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Record")
    curs_list = []
    for node in nodeArray:
        childList = node.childNodes
        for child in childList:
            if child.nodeName == 'Value':
                curs_list.append(float(child.childNodes[0].nodeValue.replace(',', '.')))
    print(curs_list)
    return curs_list

def GetCurrencyCurs_3():
    cur = cur_switch.get()
    month = date_switch.get()
    if int(month) == 1:
        month2 = '0' + str(int(date_switch.get()) + 2)
    elif int(month) == 4:
        month2 = '0' + str(int(date_switch.get()) + 2)
    elif int(month) == 7:
        month2 = '0' + str(int(date_switch.get()) + 2)
    elif int(month) == 10:
        month2 = str(int(date_switch.get()) + 2)
    id = GetCurrencyIdList(cur)
    u = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=' + '01/' + month + '/2021' + '&date_req2=' + '31/' + month2 + '/2021' + '&VAL_NM_RQ=' + str(id)
    print(u)
    res = urllib.request.urlopen(str(u))
    dom = xml.dom.minidom.parse(res)
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Record")
    curs_list = []
    for node in nodeArray:
        childList = node.childNodes
        for child in childList:
            if child.nodeName == 'Value':
                curs_list.append(float(child.childNodes[0].nodeValue.replace(',', '.')))
    print(curs_list)
    return curs_list

def GetCurrencyCurs_4():
    cur = cur_switch.get()
    year = date_switch.get()
    id = GetCurrencyIdList(cur)
    if year == now.year:
        u = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=' + '01/01/' + str(
            now.year) + '&date_req2=' + '0' + str(now.day) + '/' + '0' + str(now.month) + '/' + str(
            now.year) + '&VAL_NM_RQ=' + str(id)
    else:
        u = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=' + '01/01/' + str(
            year) + '&date_req2=' + '31/12/' + str(year) + '&VAL_NM_RQ=' + str(id)
    print(u)
    res = urllib.request.urlopen(str(u))
    dom = xml.dom.minidom.parse(res)
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Record")
    curs_list = []
    for node in nodeArray:
        childList = node.childNodes
        for child in childList:
            if child.nodeName == 'Value':
                curs_list.append(float(child.childNodes[0].nodeValue.replace(',', '.')))
    print(curs_list)
    return curs_list

def CreatePlot():
    if r_var.get() == 0: # недели
        x = []
        y = GetCurrencyCurs_1()
        print(y)
        for i in range(len(y)):
            x.append(i)
        print(x)
    elif r_var.get() == 1: # месяцы
        x = []
        y = GetCurrencyCurs_2()
        print(y)
        for i in range(len(y)):
            x.append(i)
        print(x)
    elif r_var.get() == 2: # кварталы
        x = []
        y = GetCurrencyCurs_3()
        print(y)
        for i in range(len(y)):
            x.append(i)
        print(x)
    elif r_var.get() == 3:  # годы
        x = []
        y = GetCurrencyCurs_4()
        print(y)
        date = datetime.now()
        for i in range(len(y)):
            x.append(i)
        print(x)
    matplotlib.use('TkAgg')
    fig = plt.figure()
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
    plot_widget = canvas.get_tk_widget()
    fig.clear()
    plt.plot(x, y)
    plt.grid()
    plot_widget.grid(column=4, row=4)

def Convert():
    quant = float(quantity.get())
    First_Cur = comboFirstCur.get()
    Second_Cur = comboSecondCur.get()
    First_Cur = float(currency.get(First_Cur))
    Second_Cur = float(currency.get(Second_Cur))
    res = (First_Cur/Second_Cur)*quant
    lbl['text']=str(res)

top_frame = Frame(tab1)
bottom_frame = Frame(tab1)
right_topframe = Frame(tab1)
button_frame = Frame(tab1)
lbl_frame = Frame(tab1)
comboFirstCur = ttk.Combobox(top_frame)
comboSecondCur = ttk.Combobox(bottom_frame)
quantity = ttk.Entry(right_topframe)
lbl = Label(lbl_frame)
top_frame.grid(column=0)
bottom_frame.grid(column=0)
right_topframe.grid(column=1, row=0, padx=20)
button_frame.grid(column=2, row=0, padx=20)
lbl_frame.grid(column=1, row=1, ipadx=50)
button = Button(button_frame, text='Конвертировать', command=Convert)
comboFirstCur["values"] = keylog
comboSecondCur["values"] = keylog
comboFirstCur.grid(ipadx=30, pady=20)
comboSecondCur.grid(ipadx=30, pady=20)
quantity.grid()
button.grid()
lbl.grid(padx=15)
tab_control.pack(expand=1, fill='both')

top_left_lbl = Label(tab2, text='Валюта')
top_center_lbl = Label(tab2, text='Период')
top_right_lbl = Label(tab2, text='Выбор периода')
top_left_lbl.grid(column=0, row=0, ipadx=15)
top_center_lbl.grid(column=1, row=0, ipadx=15)
top_right_lbl.grid(column=2, row=0, ipadx=15)
plot_but = Button(tab2, text='Построить график', command=CreatePlot)
plot_but.grid(column=0, row=3)
top_left_frame = Frame(tab2)
top_center_frame = Frame(tab2)
top_right_frame = Frame(tab2)
cur_switch = ttk.Combobox(top_left_frame)
cur_switch['values'] = keylog
cur_switch.grid()
date_switch = ttk.Combobox(top_right_frame)
top_left_frame.grid(column=0, row=1)
top_right_frame.grid(column=2, row=1)
r_var = IntVar()
r_var.set(0)
r1 = Radiobutton(top_center_frame, text='Неделя', variable=r_var, value=0, command=SwitchDate)
r2 = Radiobutton(top_center_frame, text='Месяц', variable=r_var, value=1, command=SwitchDate)
r3 = Radiobutton(top_center_frame, text='Квартал', variable=r_var, value=2, command=SwitchDate)
r4 = Radiobutton(top_center_frame, text='Год', variable=r_var, value=3, command=SwitchDate)
date_switch.grid()
r1.grid()
r2.grid()
r3.grid()
r4.grid()
top_center_frame.grid(column=1, row=1)
window.mainloop()