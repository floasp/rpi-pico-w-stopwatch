# sizes are 4x5, 5x8, 8x15
import patterns.numbers as patnum
import patterns.symbols as patsym
import patterns.letters_small as patles
import patterns.letters_big as patleb

def draw_pattern(bitmap, textboxw, textboxh, pattern, x, y, color=1):
    for yi in range(len(pattern)):
        if y + yi > textboxh-1 or y + yi < 0:
            continue
        for xi in range(len(pattern[0])):
            if x + xi > textboxw-1 or x + xi < 0:
                continue
            if y + yi > textboxh-1 or y + yi < 0:
                continue
            if pattern[yi][xi] is not 0:
                bitmap[x+xi, y+yi] = color
            else:
                bitmap[x+xi, y+yi] = 0
        if x + len(pattern[0]) > textboxw-1 or x + len(pattern[0]) < 0:
            continue
        else:
            bitmap[x+len(pattern[0]), y+yi] = 0
            
    return len(pattern[0])

def draw_symbol(bitmap, textboxw, textboxh, symbol, x, y, size=1, color=1):
    symbols = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
               ",", ".", ";", ":", "-", "_",
               "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
               "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
               "u", "v", "w", "x", "y", "z",
               "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
               "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
               "U", "V", "W", "X", "Y", "Z"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    letters_small = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                     "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                     "u", "v", "w", "x", "y", "z"]
    letters_big = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                   "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "U", "V", "W", "X", "Y", "Z"]
    symbols = [",", ".", ";", ":", "-", "_"]


    if symbol not in symbols:
        pass

    pattern = [[0,1,1,0],
               [0,0,0,1],
               [0,1,1,0],
               [0,1,0,0],
               [0,0,1,0]]

    if symbol == None:
        if size == 1:
            pattern = [[0,0,0,0],
                       [0,0,0,0],
                       [0,0,0,0],
                       [0,0,0,0],
                       [0,0,0,0]]
        if size == 2:
            pattern = [[0,0,0,0,0],
                       [0,0,0,0,0],
                       [0,0,0,0,0],
                       [0,0,0,0,0],
                       [0,0,0,0,0],
                       [0,0,0,0,0],
                       [0,0,0,0,0],
                       [0,0,0,0,0]]
        if size == 3:
            pattern = [[0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0]]

    if symbol in numbers:
        pattern = patnum.get_pattern(symbol, size)
    elif symbol in symbols:
        pattern = patsym.get_pattern(symbol, size)
    elif symbol in letters_small:
        pattern = patles.get_pattern(symbol, size)
    elif symbol in letters_big:
        pattern = patleb.get_pattern(symbol, size)
        
                    
    xd = draw_pattern(bitmap, textboxw, textboxh, pattern, x, y, color)
    return xd
        

def draw_text(bitmap, textboxw, textboxh, text, x, y, size=1, color=1):
    x_current = x
    for symbol in text:
        x_current += draw_symbol(bitmap, textboxw, textboxh, symbol, x_current, y, size, color) + 1
        
def draw_text_bitmap(bitmap, text, x, y, size=1):
    pass

def clear_bitmap(bitmap, textboxw, textboxh):
    for y in range(textboxh):
        for x in range(textboxw):
            bitmap[x, y] = 0


def draw_wifi(bitmap, textboxw, textboxh, x, y, color=1):
    pattern = [[0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [1,1,1,0,0],
               [0,0,0,1,0],
               [1,1,0,0,1],
               [0,0,1,0,1],
               [1,0,1,0,1]]

    xd = draw_pattern(bitmap, textboxw, textboxh, pattern, x, y, color)
    return xd

def draw_buzzer(bitmap, textboxw, textboxh, x, y, color=1):
    pattern = [[0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,1,1,1,0],
               [1,0,0,0,1],
               [0,1,0,1,0],
               [0,1,1,1,0]]

    xd = draw_pattern(bitmap, textboxw, textboxh, pattern, x, y, color)
    return xd