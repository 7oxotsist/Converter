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


    with dpg.window(label="Converter", width=320, height=320, no_resize=True, no_close=True, no_scrollbar=True, no_move=True, autosize=True):
        with dpg.group():
            dpg.add_combo(items=keylog, tag="FirstVal")
            dpg.add_input_float(tag="FloatVal")
            dpg.add_image("arrow", indent=100)
            dpg.add_combo(items=keylog, tag="SecVal")
            dpg.add_button(label="Convert", callback=Convert)
            dpg.add_text(tag="ConvRes")


<<<<<<< HEAD
    with dpg.window(label="", pos=(0,320), height=240, width=336, no_title_bar=True, no_resize=True, no_close=True, no_scrollbar=True, no_move=True):
        pass

    with dpg.window(label="", pos=(336,0), height=560, width=448, no_title_bar=True, no_resize=True, no_close=True, no_scrollbar=True, no_move=True):
=======
    with dpg.window(label="", pos=(0,320), height=240, width=336, no_title_bar=True):
        pass

    with dpg.window(label="", pos=(336,0), height=560, width=448, no_title_bar=True):
>>>>>>> main
        pass
    dpg.create_viewport(title=' ', width=800, height=599)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

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

<<<<<<< HEAD
=======
    #print(keylog,currency)

# def GetCurrencyIdList(cur):
#     u = 'http://www.cbr.ru/scripts/XML_val.asp?d=0'
#     res = urllib.request.urlopen(str(u))
#     dom = xml.dom.minidom.parse(res)
#     dom.normalize()
#     nodeArray = dom.getElementsByTagName("Item")
#     currency_id = {}
#     for node in nodeArray:
#         childList = node.childNodes
#         for child in childList:
#             if child.nodeName == 'Name':
#                 currency_id.update({child.childNodes[0].nodeValue: 0})
#             if child.nodeName == 'ParentCode':
#                 value = child.childNodes[0].nodeValue.replace('    ', '')
#                 currency_id.update({list(currency_id)[-1]: value})
#     return currency_id.get(cur)

>>>>>>> main
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