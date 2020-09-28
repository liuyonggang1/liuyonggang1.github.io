##########################################################################################################################################
from browser import window, document, alert
from browser.html import *

plot = window.Plotly.plot
window.s = ""

##########################################################################################################################################

def main(event):
    document['zone-output'].clear()
    ele = document['zone-output']
    trace1 = {'x': [1, 2], 'y':[1, 2], 'name':'y=x', 'type':'scatter'}
    trace2 = {'x': [3, 4], 'y':[9, 16], 'name':'y=x^2', 'type':'scatter'}
    plot(ele, [trace1, trace2]).then(to_image)

def to_image(gd):
    def test1(res):
        document["zone-output1"] <= IMG(src=res)
        window.s = res
        print(res)
    return window.Plotly.toImage(gd).then(test1)

def click_btn_pptx(e):
    pres = window.PptxGenJS.new()
    slide = pres.addSlide()
    textboxText = "Hello World from PptxGenJS!"
    textboxOpts = { 'x': 1, 'y': 1, 'color': "363636" }
    slide.addText(textboxText, textboxOpts)
    slide = pres.addSlide()
    slide.addImage({"data": window.s[5:] })

    pres.writeFile("Sample.pptx")

    

##########################################################################################################################################
document["btn_pptx"].bind("click", click_btn_pptx)
main(None)

