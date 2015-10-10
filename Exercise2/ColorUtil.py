import math

# From HSV to RGB
def hsv2rgb(h, s, v):
    (s, v) = (s / 100.0, v / 100.0)     
           
    h = h % 360
    hi = int(math.floor(h / 60.0))
    f = h / 60.0 - hi
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    
    if hi == 0:
        r = v
        g = t
        b = p
    elif hi == 1:
        r = q
        g = v
        b = p
    elif hi == 2:
        r = p
        g = v
        b = t
    elif hi == 3:
        r = p
        g = q
        b = v
    elif hi == 4:
        r = t
        g = p
        b = v
    elif hi == 5:
        r = v
        g = p
        b = q     
         
    return (int(round(255.0 * r)), int(round(255.0 * g)), int(round(255.0 * b)))

# From RGB to HSV
def rgb2hsv(r, g, b): 
    (r, g, b) = (r / 255.0, g / 255.0, b / 255.0)  
                
    maxValue = max(r, g, b)
    minValue = min(r, g, b)
     
    if maxValue == minValue:
        h = 0
    elif maxValue == r and g >= b:
        h = 60 * (g - b) / (maxValue - minValue) + 0
    elif maxValue == r and g < b:
        h = 60 * (g - b) / (maxValue - minValue) + 360
    elif maxValue == g:
        h = 60 * (b - r) / (maxValue - minValue) + 120
    elif maxValue == b:
        h = 60 * (r - g) / (maxValue - minValue) + 240

    if maxValue == 0:
        s = 0
    else:
        s = (maxValue - minValue) / maxValue
        
    v = maxValue
    
    return (int(round(h)), int(round(s * 100.0)), int(round(v * 100.0)))
