import dearpygui as dearpy
import dearpygui.dearpygui as dpg, xml.dom.minidom, urllib.request
from datetime import datetime


def App():
    Process()
    CreateMainMenu()

def CreateMainMenu():
    dpg.create_context()
    with dpg.font_registry():
        with dpg.font("Resources/SegoeUI.ttf", 20, default_font=True, id="DefFont"):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.bind_font("DefFont")
    width, height, channels, data = dpg.load_image("Resources/Arrow-down.png")
    with dpg.texture_registry():
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="arrow")
    #
    # with dpg.window():
    #     with dpg.menu_bar():
    #         dpg.add_menu_item(label="Converter", callback=CreateConverterWindow())
    #         dpg.add_menu_item(label="Graph", callback=CreateGraph())


    with dpg.window(label="Converter", width=320, height=320, no_resize=True, no_close=True, no_scrollbar=True, no_move=True, autosize=True):
        with dpg.group():
            dpg.add_combo(items=keylog, tag="FirstVal",)
            dpg.add_input_float(tag="FloatVal")
            dpg.add_image("arrow", indent=100)
            dpg.add_combo(items=keylog, tag="SecVal")
            dpg.add_button(label="Convert", callback=Convert)
            dpg.add_text(tag="ConvRes")


    with dpg.window(label="", pos=(0, 320), height=240, width=336, no_title_bar=True, no_resize=True, no_close=True,
                    no_scrollbar=True, no_move=True):
        global plot
        x = datetime.now()
        nowyear = x.year
        dpg.add_combo(items=keylog, tag="MyFirstVal")
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_combo(items=[i for i in range(1, 31)], width=75, tag="MyDay")
            dpg.add_combo(items=[i for i in range(1, 13)], width=75, tag="MyMonth")
            dpg.add_combo(items=[i for i in range(1990, nowyear + 1)], width=75, tag="MyYear")
        dpg.add_spacer(height=25)
        with dpg.group(horizontal=True):
            dpg.add_combo(items=[i for i in range(1, 31)], width=75, tag="MyDay2")
            dpg.add_combo(items=[i for i in range(1, 13)], width=75, tag="MyMonth2")
            dpg.add_combo(items=[i for i in range(1990, nowyear + 1)], width=75, tag="MyYear2")
        dpg.add_button(label="Рисуй!", callback=CreateGraphWindow)
        dpg.add_button(label="Очистить окно графиков", callback=clean)

    with dpg.window(tag="graphwin", pos=(336, 0), height=560, width=448, no_title_bar=True, no_resize=True, no_close=True,
                    no_scrollbar=True, no_move=True):
        pass

    dpg.create_viewport(title=' ', width=800, height=599)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def clean():
    dpg.delete_item("graphwin", children_only=True)

def ProcessForGraph():
    MyValue = dpg.get_value("MyFirstVal")
    id = GetCurrencyIdList(MyValue)
    x = dpg.get_value("MyDay")
    y = dpg.get_value("MyDay2")
    xx = dpg.get_value("MyMonth")
    yy = dpg.get_value("MyMonth2")
    if x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9':
        x = '0' + x
    if xx == '1' or xx == '2' or xx == '3' or xx == '4' or xx == '5' or xx == '6' or xx == '7' or xx == '8' or xx == '9':
        xx = '0' + xx
    if y == '1' or y == '2' or y == '3' or y == '4' or y == '5' or y == '6' or y == '7' or y == '8' or y == '9':
        y = '0' + y
    if yy == '1' or yy == '2' or yy == '3' or yy == '4' or yy == '5' or yy == '6' or yy == '7' or yy == '8' or yy == '9':
        yy = '0' + yy
    url_1 = 'https://cbr.ru/scripts/XML_dynamic.asp?date_req1=' + str(x) + '/' + str(xx) + '/' + str(dpg.get_value(
        "MyYear")) + '&date_req2=' + str(y) + '/' + str(yy) + '/' + str(dpg.get_value("MyYear2")) + '&VAL_NM_RQ=' + str(
        id)
    res = urllib.request.urlopen(str(url_1))
    dom = xml.dom.minidom.parse(res)
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Record")
    curs_list = []
    for node in nodeArray:
        childList = node.childNodes
        for child in childList:
            if child.nodeName == 'Value':
                curs_list.append(float(child.childNodes[0].nodeValue.replace(',', '.')))
    return curs_list


def ProcessX():
    MyValue = dpg.get_value("MyFirstVal")
    id = GetCurrencyIdList(MyValue)
    x = dpg.get_value("MyDay")
    y = dpg.get_value("MyDay2")
    xx = dpg.get_value("MyMonth")
    yy = dpg.get_value("MyMonth2")
    if x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9':
        x = '0' + x
    if xx == '1' or xx == '2' or xx == '3' or xx == '4' or xx == '5' or xx == '6' or xx == '7' or xx == '8' or xx == '9':
        xx = '0' + xx
    if y == '1' or y == '2' or y == '3' or y == '4' or y == '5' or y == '6' or y == '7' or y == '8' or y == '9':
        y = '0' + y
    if yy == '1' or yy == '2' or yy == '3' or yy == '4' or yy == '5' or yy == '6' or yy == '7' or yy == '8' or yy == '9':
        yy = '0' + yy
    url_1 = 'https://cbr.ru/scripts/XML_dynamic.asp?date_req1=' + str(x) + '/' + str(xx) + '/' + str(dpg.get_value(
        "MyYear")) + '&date_req2=' + str(y) + '/' + str(yy) + '/' + str(dpg.get_value("MyYear2")) + '&VAL_NM_RQ=' + str(id)
    print(url_1)
    res = urllib.request.urlopen(str(url_1))
    dom = xml.dom.minidom.parse(res)
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Record")
    curs_list = []
    for node in nodeArray:
        curs_list.append(node.getAttribute('Date'))
    return print(curs_list)


def CreateGraphWindow():
    sindatay = ProcessForGraph()
    sindatax = [i for i in range(1, len(sindatay))]
    global plot
    with dpg.plot(label=dpg.get_value("MyFirstVal"),parent="graphwin", height=400, width=400) as plot:
        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis)
        # series belong to a y axis
        dpg.add_line_series(sindatax, sindatay, parent=y_axis)


def Process():
    global keylog, currency
    now = datetime.now()
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
    keylog = []
    for node in nodeArray:
        childList = node.childNodes
        for child in childList:
            if child.nodeName == 'Name':
                currency.update({child.childNodes[0].nodeValue: 0})
            if child.nodeName == 'Value':
                value = child.childNodes[0].nodeValue.replace(',', '.')
                currency.update({list(currency)[-1]: value})
    for key in currency.keys():
        keylog.append(key)

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

def Convert():
    First = currency[dpg.get_value("FirstVal")]
    FirstVal = dpg.get_value("FirstVal")
    FloatValue = dpg.get_value("FloatVal")
    Second = currency[dpg.get_value("SecVal")]
    SecondVal = dpg.get_value("SecVal")

    Res = float(First) / float(Second) * FloatValue
    Res = "{:.2f}".format(Res)
    dpg.set_value("ConvRes", f'{FloatValue} {FirstVal} ~ {Res} {SecondVal}')


if __name__ == "__main__":
    App()
