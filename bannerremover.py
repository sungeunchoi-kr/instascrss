import subprocess
import time
import pyscreenshot as scrot
import pytesseract
from pytesseract import Output

def run():
    img = scrot.grab()
    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    
    prev_level = 0
    lines = [ { "text": "", "x": 0, "y": 0 } ]
    for i in range(len(data['level'])):
        (level, y, x, text) = (data['line_num'][i], data['top'][i], data['left'][i], data['text'][i])
    
        if prev_level != level:
            # if level changed
            lines.append({ "text": text, "x": x, "y": y })
            prev_level = level
        else:
           lines[len(lines)-1]["text"] += text
    
    for line in lines:
        if 'UsetheApp' in line["text"]:
            print(line)
            clickx = line['x'] + 230
            clicky = line['y'] + 5
            print('click position: {}'.format((clickx, clicky)))
            subprocess.run([ 'xdotool', 'mousemove', str(clickx), str(clicky) ])
            time.sleep(1)
            subprocess.run([ 'xdotool', 'click', '1' ])
            time.sleep(1)

