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

    with dpg.window(tag="Primary Window"):
        with dpg.menu_bar():
            dpg.add_menu_item(label="Cockverter", callback=CreateConverterWindow)

    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

def CreateConverterWindow():
    with dpg.window(label="Converter", width=320, height=320, tag="Conv"):
        dpg.add_combo(items=keylog, tag="FirstVal")
        dpg.add_input_float(tag="FloatVal")
        dpg.add_image("arrow")
        dpg.add_combo(items=keylog, tag="SecVal")
        dpg.add_text(tag="ConvRes")
        dpg.add_button(label="Convert", callback=Convert)

def Process():
    global keylog, currency
    now = datetime.now()
    print('Сегодня:', now)
    if now.day < 10:
        u = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + "0" + str(now.day) + '/' + '0' + str(now.month) + '/' + str(
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

    print(keylog,currency)

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
    FloatValue = dpg.get_value("FloatVal")
    Second = currency[dpg.get_value("SecVal")]
    print(First, FloatValue, Second)

    Res = (float(First) / float(Second)) * FloatValue
    dpg.set_value("ConvRes", Res)

if __name__ == "__main__":
    App()