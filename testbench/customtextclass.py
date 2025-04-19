import customtext
import time

class CustomText():
    
    def __init__(bitmap, posx, posy, text):
        pass
    
    def draw_text(text):
        pass
    
class CustomTimer():
    
    def __init__(self, bitmap, textboxw, textboxh, timens=0):
        self.bitmap = bitmap
        self.timens = timens
        self.textboxw = textboxw
        self.textboxh = textboxh
        self.prev_time = self.time_to_str(timens)
        self.elapsedtimens = 0
        self.starttime = 0
        self.firstdraw=True
        self.running = False
        
        self.update(redraw=True)
        
    def reset(self):
        self.running = False
        self.firstdraw=True
        self.starttime = time.monotonic_ns()
        self.elapsedtimens = 0
        customtext.clear_bitmap(self.bitmap, self.textboxw, self.textboxh)
        self.update(redraw=True)
        
    def start(self):
        # self.starttime = time.monotonic_ns()
        if self.running:
            return
        self.running = True
        self.starttime = time.monotonic_ns()
        
    def restart(self):
        self.running = True
        self.reset()
        self.start()
        
    def stop(self):
        if self.running:
            self.elapsedtimens += time.monotonic_ns() - self.starttime
        self.running = False
        self.starttime = time.monotonic_ns()
        self.update(redraw=True)
    
    def time_to_str(self, ns):
        s = ns // 1000000000
        m = s // 60
        #s = s % 60
        hs = ns // 10000000
        hs = hs % 100
        
    #     return ("%02d" % (m,)) + ":" + ("%02d" % (s,)) + "," + ("%02d" % (hs,))
        return ("%02d" % (s,)) + "," + ("%02d" % (hs,))
    
    def update(self, redraw=False):
        if not self.running and not redraw:
            return
        
        
        if self.running:
            self.timens = time.monotonic_ns() - self.starttime + self.elapsedtimens
            new_time = self.time_to_str(self.timens)
        else:
            new_time = self.time_to_str(self.elapsedtimens)
        text_width = (len(new_time)-1)*8+5+4
        width_diff = self.textboxw - text_width
        
        if len(new_time) is not len(self.prev_time) or self.firstdraw == True:
            customtext.draw_text(self.bitmap, self.textboxw, self.textboxh, new_time, width_diff//2, 0, size=3, color=1)
            self.firstdraw = False
            # print("test", new_time, self.prev_time, len(new_time), len(self.prev_time))
            self.prev_time = new_time
            return
        
        for i, symbol in enumerate(new_time):
            if symbol == self.prev_time[i]:
                continue
            
            offset = 0
            if i < len(new_time) - 3:  # longer times have the colon, which is smaller than a symbol
                offset = 9*i  # offset full symbol width
            else:
                offset = 9*(i-1) + 5  # width of symbols and colon
            customtext.draw_symbol(self.bitmap, self.textboxw, self.textboxh, symbol, width_diff//2 + offset, 0, size=3, color=1)            
        
        self.prev_time = new_time
