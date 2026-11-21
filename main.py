"""A deterministic, self-contained vector-type newspaper. Python standard library only."""
import base64
import hashlib
import json
import math
import os
import struct
import zlib
SANS_COORDINATES = 'JZ\nMWRFRT RRYQZR[SZRY\nJZNFNM RVFVM\nH]SBLb RYBRb RLOZO RKUYU\nH\\PBP_ RTBT_ RYIWGTFPFMGKIKKLMMNOOUQWRXSYUYXWZT[P[MZKX\nF^[FI[ RNFPHPJOLMMKMIKIIJGLFNFPGSHVHYG[F RWTUUTWTYV[X[ZZ[X[VYTWT\nE_\\O\\N[MZMYNXPVUTXRZP[L[JZIYHWHUISJRQNRMSKSIRGPFNGMIMKNNPQUXWZY[[[\\Z\\Y\nMWRHQGRFSGSIRKQL\nKYVBTDRGPKOPOTPYR]T`Vb\nKYNBPDRGTKUPUTTYR]P`Nb\nJZRLRX RMOWU RWOMU\nE_RIR[ RIR[R\nNVSWRXQWRVSWSYQ[\nE_IR[R\nNVRVQWRXSWRV\nG][BIb\nH\\QFNGLJKOKRLWNZQ[S[VZXWYRYOXJVGSFQF\nH\\NJPISFS[\nH\\LKLJMHNGPFTFVGWHXJXLWNUQK[Y[\nH\\MFXFRNUNWOXPYSYUXXVZS[P[MZLYKW\nH\\UFKTZT RUFU[\nH\\WFMFLOMNPMSMVNXPYSYUXXVZS[P[MZLYKW\nH\\XIWGTFRFOGMJLOLTMXOZR[S[VZXXYUYTXQVOSNRNOOMQLT\nH\\YFO[ RKFYF\nH\\PFMGLILKMMONSOVPXRYTYWXYWZT[P[MZLYKWKTLRNPQOUNWMXKXIWGTFPF\nH\\XMWPURRSQSNRLPKMKLLINGQFRFUGWIXMXRWWUZR[P[MZLX\nNVROQPRQSPRO RRVQWRXSWRV\nNVROQPRQSPRO RSWRXQWRVSWSYQ[\nF^ZIJRZ[\nE_IO[O RIU[U\nF^JIZRJ[\nI[LKLJMHNGPFTFVGWHXJXLWNVORQRT RRYQZR[SZRY\nE`WNVLTKQKOLNMMPMSNUPVSVUUVS RQKOMNPNSOUPV RWKVSVUXVZV\\T]Q]O\\L[JYHWGTFQFNGLHJJILHOHRIUJWLYNZQ[T[WZYYZX RXKWSWUXV\nI[RFJ[ RRFZ[ RMTWT\nG\\KFK[ RKFTFWGXHYJYLXNWOTP RKPTPWQXRYTYWXYWZT[K[\nH]ZKYIWGUFQFOGMILKKNKSLVMXOZQ[U[WZYXZV\nG\\KFK[ RKFRFUGWIXKYNYSXVWXUZR[K[\nH[LFL[ RLFYF RLPTP RL[Y[\nHZLFL[ RLFYF RLPTP\nH]ZKYIWGUFQFOGMILKKNKSLVMXOZQ[U[WZYXZVZS RUSZS\nG]KFK[ RYFY[ RKPYP\nNVRFR[\nJZVFVVUYTZR[P[NZMYLVLT\nG\\KFK[ RYFKT RPOY[\nHYLFL[ RL[X[\nF^JFJ[ RJFR[ RZFR[ RZFZ[\nG]KFK[ RKFY[ RYFY[\nG]PFNGLIKKJNJSKVLXNZP[T[VZXXYVZSZNYKXIVGTFPF\nG\\KFK[ RKFTFWGXHYJYMXOWPTQKQ\nG]PFNGLIKKJNJSKVLXNZP[T[VZXXYVZSZNYKXIVGTFPF RSWY]\nG\\KFK[ RKFTFWGXHYJYLXNWOTPKP RRPY[\nH\\YIWGTFPFMGKIKKLMMNOOUQWRXSYUYXWZT[P[MZKX\nJZRFR[ RKFYF\nG]KFKULXNZQ[S[VZXXYUYF\nI[JFR[ RZFR[\nF^HFM[ RRFM[ RRFW[ R\\FW[\nH\\KFY[ RYFK[\nI[JFRPR[ RZFRP\nH\\YFK[ RKFYF RK[Y[\nKYOBOb RPBPb ROBVB RObVb\nKYKFY^\nKYTBTb RUBUb RNBUB RNbUb\nJZRDJR RRDZR\nI[Ib[b\nNVSKQMQORPSORNQO\nI\\XMX[ RXPVNTMQMONMPLSLUMXOZQ[T[VZXX\nH[LFL[ RLPNNPMSMUNWPXSXUWXUZS[P[NZLX\nI[XPVNTMQMONMPLSLUMXOZQ[T[VZXX\nI\\XFX[ RXPVNTMQMONMPLSLUMXOZQ[T[VZXX\nI[LSXSXQWOVNTMQMONMPLSLUMXOZQ[T[VZXX\nMYWFUFSGRJR[ ROMVM\nI\\XMX]W`VaTbQbOa RXPVNTMQMONMPLSLUMXOZQ[T[VZXX\nI\\MFM[ RMQPNRMUMWNXQX[\nNVQFRGSFREQF RRMR[\nMWRFSGTFSERF RSMS^RaPbNb\nIZMFM[ RWMMW RQSX[\nNVRFR[\nCaGMG[ RGQJNLMOMQNRQR[ RRQUNWMZM\\N]Q][\nI\\MMM[ RMQPNRMUMWNXQX[\nI\\QMONMPLSLUMXOZQ[T[VZXXYUYSXPVNTMQM\nH[LMLb RLPNNPMSMUNWPXSXUWXUZS[P[NZLX\nI\\XMXb RXPVNTMQMONMPLSLUMXOZQ[T[VZXX\nKXOMO[ ROSPPRNTMWM\nJ[XPWNTMQMNNMPNRPSUTWUXWXXWZT[Q[NZMX\nMYRFRWSZU[W[ ROMVM\nI\\MMMWNZP[S[UZXW RXMX[\nJZLMR[ RXMR[\nG]JMN[ RRMN[ RRMV[ RZMV[\nJ[MMX[ RXMM[\nJZLMR[ RXMR[P_NaLbKb\nJ[XMM[ RMMXM RM[X[\nKYTBRCQDPFPHQJRKSMSOQQ RRCQEQGRISJTLTNSPORSTTVTXSZR[Q]Q_Ra RQSSUSWRYQZP\\P^Q`RaTb\nNVRBRb\nKYPBRCSDTFTHSJRKQMQOSQ RRCSESGRIQJPLPNQPURQTPVPXQZR[S]S_Ra RSSQUQWRYSZT\\T^S`RaPb\nF^IUISJPLONOPPTSVTXTZS[Q RISJQLPNPPQTTVUXUZT[Q[O'
ROMAN_COORDINATES = {'*': 'JZRFRR RMIWO RWIMO', ',': 'MWSZR[QZRYSZS\\R^Q_', '.': 'MWRYQZR[SZRY', ':': 'MWRMQNROSNRM RRYQZR[SZRY', ';': 'MWRMQNROSNRM RSZR[QZRYSZS\\R^Q_', '^': 'JZPLRITL RMORJWO RRJR[', '_': 'JZJ]Z]', '`': 'MWSFRGQIQKRLSKRJ'}
MASK_COLS, MASK_ROWS = (180, 90)
LANDMASK_B64 = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP//7//wAAAAAAAAAAAAAAAAAAAAAAB///////AA/wDwAAHgAAAAAAAAAAAHf//////4AB/gAAAAD+AAAAAAAAAAD/v/8////4AA/gAA+ADf4AGAAAAAAAH///4A///4AAAAAH4Af/8AP8AAAAAAH///+Af//wAAAAAeD////+H4AAwH/gf////4P//wAAD8AeH///////wRw//////9/4P//AAAP/nP//////////+///////3/H/wuAAf//////////////////////+H/B/AB//////////////Df/////7/8D8A8AP//////////////A//////gf8B4AAAP/////////////8A/8////wP+AAAAGP5///////////fQAHwB///8H/AAAAPD7/////////8B8AAeAB////v/wAAAfD//////////9B8AAAAB//////4AAAfv///////////B4AAAAAf/////4AAAX////////////AwAAAAAf/////8AAAH////////////gAAAAAAH/////8AAAH////////////AAAAAAAD/////gAAAB//7////////7gAAAAAAH////8AAAAf//7f///////3gAAAAAAH////wAAAAfy/////////+HAAAAAAAD///+AAAAAfi/////////+GAAAAAAAD///+AAAAAf/7////////+OAAAAAAAB///+AAAAAP/Bz///////n+AAAAAAAA///4AAAAAf/zB///////jwAAAAAAAAf//wAAAAAf//////////hAAAAAAAAAP/9wAAAAB///////////wAAAAAAAAAP/A8AAAAD///////////gAAAAAAAAAH/AcAAAAD///////////gAAAAACAAAD/B8AAAAH//////H///+gAAAAADgAAAfPeAAAAH//////B///wgAAAAABgAAAf+P8AAAH////v+A/j/wwAAAAAAAAAAP+EsAAAH/////+A/B/hwAAAAAAAAAABfgAAAAH/////4A+B/hwAAAAAAAAAAAPgwAAAH/////wAeAfg4AAAAAAAAAAADj/AAAH/////wAcAXh4AAAAAAAAAAAB//gAAD/////wAOAbDcAAAAAAAAAAAAf/4AAB/////gAOAcC8AAAAAAAAAAAAH/+AAAfv///gACB8HIAAAAAAAAAAAAP/+AAAAD///AAAA8/EAAAAAAAAAAAAf//AAAAD//+AAAAe/+AAAAAAAAAAAAf//wAAAD//8AAAAO/38AAAAAAAAAAAf//+AAAD//4AAAAPf//mAAAAAAAAAAf///gAAB//wAAAAHHw/vAAAAAAAAAAf///gAAA//wAAAAD8AX9wAAAAAAAAAP///gAAA//wAAAAAf8PcYAAAAAAAAAP///AAAA//4AAAAAA57cMAAAAAAAAAH///AAAA//5wAAAAAH7AAAAAAAAAAAH//+AAAB//7wAAAAAP7gBAgAAAAAAAB//+AAAB///wAAAAAf/wBDAAAAAAAAA//+AAAB//jgAAAAB//4ADAAAAAAAAA//8AAAA//HgAAAAH//4DAAAAAAAAAA//8AAAAf/HAAAAAP//8BAAAAAAAAAA//gAAAAf/HAAAAAP//+AAAAAAAAAAA//AAAAAf+AAAAAAP//+AAAAAAAAAAA//AAAAAP+AAAAAAH//+AAAAAAAAAAA/+AAAAAP8AAAAAAH//+AAAAAAAAAAA/8AAAAAP4AAAAAAH8/+AAAAAAAAAAB/8AAAAAGAAAAAAAHQf8AMAAAAAAAAB/wAAAAAAAAAAAAAAAH8APAAAAAAAAB/wAAAAAAAAAAAAAAADwAPAAAAAAAAD+AAAAAAAAAAAAAAAAA4AeAAAAAAAAD+AAAAAAAAAAAAAAAAA4A4AAAAAAAAD8AAAAAAAAAAAAAAAAAABwAAAAAAAAD8AAAAAAAAAAAAAAAAAABgAAAAAAAAD8AAAAAAAAAADAAAAAAAAAAAAAAAAADxwAAAAAAAAAAAAAAAAAAAAAAAAAAAD5gAAAAAAAAAAAAAAAAAAAAAAAAAAAB8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAHgAAAAAAAAOAAAGIAQAAAAAAAAAAAAOAAAAAAAAD/+D/////wAAAAAAAAAAA+AAAAAEsH//+///////wAAAAAAAPAD/AAAA///////////////wAAAAPkP///AAAH///////////////wAAD///////AAAf///////////////AAD///////wAgf///////////////+AAP//////+BD4/////////////////AAB////////v/////////////////4ABAf//////////////////////////g//////////////////////////////////////////////////////////////////////////////////////////'
PAPER = (244, 239, 227)
INK = (27, 27, 27)
RED = (116, 31, 41)
BLUE = (31, 78, 156)
AMBER = (217, 142, 43)
GREY = (88, 82, 74)
RULE = (174, 164, 147)
LAND = (116, 110, 99)
EDGE = 28
WIDTH = 1024 - 2 * EDGE
GUTTER = 22
COLUMN = (WIDTH - 2 * GUTTER) // 3
SCALE = 3
SIDE = 1024 * SCALE

def parse_glyph(encoded):
    left, right = (ord(c) - 82 for c in encoded[:2])
    strokes = []
    for stroke in encoded[2:].split(' R'):
        assert len(stroke) % 2 == 0
        if stroke:
            strokes.append(tuple(((ord(stroke[i]) - 82, ord(stroke[i + 1]) - 82) for i in range(0, len(stroke), 2))))
    return (left, right, tuple(strokes))
SANS = {chr(i + 32): parse_glyph(s) for i, s in enumerate(SANS_COORDINATES.splitlines())}
assert len(SANS) == 95
SANS['·'] = (-5, 5, (((-0.7, 0), (0.7, 0)),))
SANS['—'] = (-12, 12, (((-10, 0), (10, 0)),))
ROMAN = dict(SANS)
ROMAN.update({c: parse_glyph(s) for c, s in ROMAN_COORDINATES.items()})

def condensed(width, font=SANS):
    return {c: (left * width, right * width, tuple((tuple(((x * width, y) for x, y in stroke)) for stroke in strokes))) for c, (left, right, strokes) in font.items()}
HEADLINE = condensed(0.72)
TAG = condensed(0.86)
SERIF = dict(ROMAN)
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':
    left, right, strokes = ROMAN[letter]
    terminals, stems = (set(), [])
    for stroke in strokes:
        if len(stroke) < 2:
            continue
        for (px, py), (qx, qy) in ((stroke[0], stroke[1]), (stroke[-1], stroke[-2])):
            if py in (-12, -5, 9) and abs(qy - py) >= 3:
                terminals.add((px, py))
        for (px, py), (qx, qy) in zip(stroke, stroke[1:]):
            if abs(qx - px) <= 1 and abs(qy - py) >= 5:
                stems.append(((px + 0.65, py), (qx + 0.65, qy)))
    serifs = tuple((((px - 2.5, py), (px + 2.5, py)) for px, py in sorted(terminals)))
    if letter in '0235689':
        serifs += tuple((((px, py - 2), (px, py + 2)) for stroke in strokes if len(stroke) > 2 for px, py in (stroke[0], stroke[-1]) if stroke[0] != stroke[-1]))
    extra = tuple(stems) + serifs
    xs = [px for stroke in extra for px, _ in stroke]
    SERIF[letter] = (min(left, min(xs) - 1) if xs else left, max(right, max(xs) + 1) if xs else right, strokes + extra)
MASTHEAD = condensed(0.82, SERIF)
HERO_HEADLINE = condensed(0.72, SERIF)

class Page:

    def __init__(self):
        self.pixels = bytearray(bytes(PAPER) * SIDE * SIDE)
        self.text_boxes = []
        self.rendered = []

    def rect(self, x, y, w, h, color):
        x0, y0, x1, y1 = (round(v * SCALE) for v in (x, y, x + w, y + h))
        assert 0 <= x0 <= x1 <= SIDE and 0 <= y0 <= y1 <= SIDE
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            start = (yy * SIDE + x0) * 3
            self.pixels[start:start + len(row)] = row

    def dot(self, x, y, radius, color):
        for dy in range(-round(radius * SCALE), round(radius * SCALE) + 1):
            half_width = math.sqrt(max(0, (radius * SCALE) ** 2 - dy ** 2))
            span = math.floor(half_width)
            self.rect((round(x * SCALE) - span) / SCALE, (round(y * SCALE) + dy) / SCALE, (2 * span + 1) / SCALE, 1 / SCALE, color)

    def line(self, x0, y0, x1, y1, color, weight):
        return self.polyline(((x0, y0), (x1, y1)), color, max(1, round(weight * SCALE / 2)))

    def polyline(self, points, color, weight):
        return self.stroke_pixels(tuple(((round(x * SCALE), round(y * SCALE)) for x, y in points)), color, weight)

    def stroke_pixels(self, points, color, weight):
        assert len(points) >= 2 and weight >= 1
        rgb = bytes(color)
        offsets = range(-(weight // 2), -(weight // 2) + weight)
        radius = weight / 2
        left = top = SIDE
        right = bottom = 0

        def pixel(px, py):
            nonlocal left, top, right, bottom
            assert 0 <= px < SIDE and 0 <= py < SIDE
            pos = (py * SIDE + px) * 3
            self.pixels[pos:pos + 3] = rgb
            left, top = (min(left, px), min(top, py))
            right, bottom = (max(right, px + 1), max(bottom, py + 1))
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            dx, dy = (abs(x1 - x0), -abs(y1 - y0))
            steep = abs(y1 - y0) > abs(x1 - x0)
            sx, sy = (1 if x0 < x1 else -1, 1 if y0 < y1 else -1)
            err = dx + dy
            while True:
                for offset in offsets:
                    pixel(x0 + offset if steep else x0, y0 if steep else y0 + offset)
                if x0 == x1 and y0 == y1:
                    break
                e = 2 * err
                if e >= dy:
                    err += dy
                    x0 += sx
                if e <= dx:
                    err += dx
                    y0 += sy
        extent = math.floor(radius)
        for cx, cy in points:
            for oy in range(-extent, extent + 1):
                span = math.floor(math.sqrt(max(0, radius * radius - oy * oy)))
                for ox in range(-span, span + 1):
                    pixel(cx + ox, cy + oy)
        return (left, top, right, bottom)

    def text(self, text, x, y, size, color=INK, weight=2, font=SANS, width=None, tracking=0, *, ink_top=False):
        advance = measure(text, size, font, tracking)
        if width is not None:
            assert advance <= width + 0.001, (text, advance, width)
        cursor = x
        scale = size / 21
        paths = []
        for ch in text:
            left, right, strokes = font[ch]
            for stroke in strokes:
                pts = [(cursor + (px - left) * scale, (py + 12) * scale + (0 if ink_top else y)) for px, py in stroke]
                if len(pts) >= 2:
                    paths.append(tuple(((round(px * SCALE), round(py * SCALE)) for px, py in pts)))
            cursor += (right - left) * scale + tracking
        if paths:
            if ink_top:
                pad = math.floor(weight / 2)
                min_y = min((min((py for _, py in path)) - pad for path in paths))
                dy = round(y * SCALE) - min_y
                paths = [tuple(((px, py + dy) for px, py in path)) for path in paths]
            ink = [self.stroke_pixels(path, color, weight) for path in paths]
            bounds = (min((b[0] for b in ink)) / SCALE, min((b[1] for b in ink)) / SCALE, max((b[2] for b in ink)) / SCALE, max((b[3] for b in ink)) / SCALE)
            if width is not None:
                assert x <= bounds[0] and bounds[2] <= x + width, (text, bounds, x, width)
            self.text_boxes.append((text, bounds))
        return advance

    def png(self):
        raw = bytearray()
        stride = SIDE * 3
        for y in range(1024):
            raw.append(0)
            a = 3 * y * stride
            b = a + stride
            c = b + stride
            for x in range(1024):
                p = x * 9
                for channel in range(3):
                    total = self.pixels[a + p + channel] + self.pixels[a + p + 3 + channel] + self.pixels[a + p + 6 + channel] + self.pixels[b + p + channel] + self.pixels[b + p + 3 + channel] + self.pixels[b + p + 6 + channel] + self.pixels[c + p + channel] + self.pixels[c + p + 3 + channel] + self.pixels[c + p + 6 + channel]
                    raw.append((total + 4) // 9)

        def chunk(kind, data):
            return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 4294967295)
        return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 1024, 1024, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')

def measure(text, size, font=SANS, tracking=0):
    return sum((font[c][1] - font[c][0] for c in text)) * size / 21 + max(0, len(text) - 1) * tracking

def wrap(text, size, width, font):
    lines, current = ([], '')
    for word in text.split():
        trial = (current + ' ' + word).strip()
        if current and measure(trial, size, font) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    assert all((measure(line, size, font) <= width for line in lines)), (text, size, width)
    return lines
HEROES = (('SHENZHEN SUMMIT', 'APEC 2026 · SHENZHEN · THREE-WAY PEACE DECLARATION', ('Trump, Xi and Putin', 'issue peace declaration'), "Unprecedented three-way meeting dominated APEC leaders' gathering.", 'FROM AP'), ('UKRAINE UNDER FIRE', 'KYIV · RUSSIA & UKRAINE · OVERNIGHT ATTACK', ('Russia launches', 'massive Ukraine attack'), 'Kyiv bridges struck hours after Trump-Putin Xi peace declaration.', 'BY REUTERS'), ('MARKETS IN ROUT', 'GLOBAL MARKETS · TECHNOLOGY & BUSINESS', ('Global stock rout', 'wipes nearly $9 trillion'), 'VIX hits 30, highest since late March, amid AI fears.', 'BY REUTERS'))
FEATURES = (('EUROPE', 'LONDON', 'bridge', 'Britain and EU clinch trade deals', 'Summit reset still stuck on university tuition fee differences.', 'BY REUTERS'), ('MIDDLE EAST', 'RIYADH', 'missile', 'Houthis fire missiles at Riyadh', 'Coalition also intercepted five drones and a ballistic missile.', 'BY AP'), ('AFRICA', 'BADME', 'fist', 'Ethiopia and Eritrea mass troops', 'ACLED reports drone strikes near Badme; Eritrea denies buildup.', 'BY REUTERS'), ('ASIA', 'TAIPEI', 'chart', 'Taiwan stocks suffer worst week since 1990', 'AI selloff wipes more than 16 percent from benchmark index.', 'BY REUTERS'), ('AMERICAS', 'WASHINGTON', 'court', 'Senate rejects Iran war powers bid', 'Vote 51-48 defeats measure previously passed by House.', 'BY AP'), ('TECHNOLOGY & BUSINESS', 'NEW YORK', 'chart', 'Anthropic shares tumble 9%', 'AI valuation concerns weigh heavily on technology stocks.', 'BY REUTERS'), ('ASIA', 'TOKYO', 'chart', 'Japan inflation hits 2.6 percent', 'Prices remain in focus as Tokyo inflation reaches 2.6 percent.', 'BY REUTERS'), ('AFRICA', 'DAKAR', 'fist', 'Senegal party expels President Faye', 'Party expels President Faye in a fresh political rupture.', 'BY REUTERS'))
DISPATCHES = (('ASIA', 'Japan inflation hits\n2.6 percent', 'TOKYO / REUTERS'), ('AMERICAS', '300 migrants cross\ninto southern Mexico', 'MEXICO / REUTERS'), ('AFRICA', 'Senegal party expels\nPresident Faye', 'DAKAR / REUTERS'), ('TECHNOLOGY & BUSINESS', 'OpenAI faces probe\nover rogue agents', 'ARIZONA / REUTERS'))
BULLETINS = (('ASIA', 'Trump, Xi and Putin issue peace deal', (114.1, 22.5)), ('EUROPE', 'Russia violates Polish airspace three times', (19.1, 52.2)), ('EUROPE', 'France seeks UN meeting after Kyiv strikes', (2.3, 48.9)), ('RUSSIA & UKRAINE', 'Russia accuses Estonia of new Iron Curtain', (24.8, 59.4)), ('EUROPE', 'Italy strike draws thousands into streets', (12.5, 41.9)), ('EUROPE', 'de Villepin launches 2027 bid in Paris', (2.3, 48.9)), ('MIDDLE EAST', 'Houthi attacks worry over Saudi nuclear pact', (46.7, 24.7)), ('MIDDLE EAST', 'Two oil tankers hit mines in Hormuz', (56.3, 26.6)), ('MIDDLE EAST', 'Israeli strikes kill six in central Gaza', (34.4, 31.4)), ('AFRICA', 'Nigeria states approve state police change', (7.5, 9.1)), ('AFRICA', 'Bayelsa funeral barge capsizes', (6.1, 4.9)), ('AFRICA', 'South Sudan groups reject election delay', (31.6, 4.8)), ('ASIA', 'Xi hails China-Australia turnaround', (116.4, 39.9)), ('ASIA', 'Nepal PM Shah plans India visit', (85.3, 27.7)), ('ASIA', 'Malaysia to resettle 10,000 Rohingya', (101.7, 3.1)), ('AMERICAS', 'Virginia judge blocks Trump arch', (-77.4, 38.9)), ('AMERICAS', 'Florida carries out record 20th execution', (-84.3, 30.4)), ('AMERICAS', 'LatAm stocks tumble to one-year low', (-58.4, -15.0)), ('TECHNOLOGY & BUSINESS', 'Dollar index reaches 19-month high', (-74.0, 40.7)), ('TECHNOLOGY & BUSINESS', 'Gold falls 2 percent; copper weekly drop', (-74.0, 40.7)))
REGION_CODES = dict(zip(('EUROPE', 'MIDDLE EAST', 'AMERICAS', 'AFRICA', 'ASIA', 'RUSSIA & UKRAINE', 'TECHNOLOGY & BUSINESS'), ('EU', 'ME', 'AM', 'AF', 'AS', 'RU', 'TB')))
DESK_COLORS = {'EUROPE': (31, 78, 156), 'MIDDLE EAST': (136, 82, 20), 'AMERICAS': (164, 57, 48), 'AFRICA': (130, 52, 99), 'ASIA': (142, 65, 38), 'RUSSIA & UKRAINE': (48, 89, 112), 'TECHNOLOGY & BUSINESS': (39, 104, 91)}

def label(page, text, x, y, width, size=8, color=GREY, *, weight=2, font=TAG, tracking=0.38):
    left = round(x * SCALE) / SCALE
    return page.text(text, left, y, size, color, weight, font, x + width - left, tracking, ink_top=True)

def centered(page, text, x, y, width, size, color=INK, *, weight=2, font=SANS, tracking=0):
    margin = (width - measure(text, size, font, tracking)) / 2
    assert margin >= 1, (text, width)
    label(page, text, x + margin, y, width - margin, size, color, weight=weight, font=font, tracking=tracking)

def byline(page, text, x, width, card_bottom):
    previous_bottom = page.text_boxes[-1][1][3]
    y = math.ceil((previous_bottom + 8) * SCALE) / SCALE
    first = len(page.text_boxes)
    page.rect(x, y + 3, 8, 1, RED)
    label(page, text, x + 13, y, width - 13, 7.2, GREY, weight=2, tracking=0.62)
    _, (_, top, _, bottom) = page.text_boxes[first]
    assert top - previous_bottom >= 8, (text, 'byline top gap')
    assert card_bottom - bottom >= 10, (text, 'byline bottom gap', card_bottom, bottom)
    return bottom

def check_bounds(page, first, x, y, w, h):
    for text, (left, top, right, bottom) in page.text_boxes[first:]:
        assert x <= left < right <= x + w and y <= top < bottom <= y + h, (text, 'section bounds', (left, top, right, bottom), (x, y, x + w, y + h))

def column_rules(page, top, bottom):
    assert 3 * COLUMN + 2 * GUTTER == WIDTH
    for index in (1, 2):
        center = EDGE + index * (COLUMN + GUTTER) - GUTTER / 2
        page.rect(center - 0.5, top, 1, bottom - top, RULE)

def desk_chip(page, desk, x, y):
    width = math.ceil(measure(desk, 7.5, TAG, 0.48)) + 14
    page.rect(x, y, width, 15, DESK_COLORS[desk])
    label(page, desk, x + 7, y + 4, width - 13, 7.5, PAPER, tracking=0.48)

def masthead(page, count):
    label(page, f'THE WORLD IN ONE DAY · {count} STORIES · ACROSS THE GLOBE', EDGE, 23, 783, 10, RED, tracking=0.7)
    label(page, 'WORLD EDITION', 872, 23, 124, 10, GREY, tracking=0.7)
    centered(page, 'FRIDAY 20 NOVEMBER 2026', EDGE, 51, WIDTH, 44, weight=9, font=MASTHEAD, tracking=1.5)
    page.rect(EDGE, 128, WIDTH, 4, RED)
    page.rect(EDGE, 136, WIDTH, 1, RED)

def stats_bar(page):
    stats = (('3', 'PEACE DECLARATION'), ('8', 'KILLED IN UKRAINE'), ('$9tn', 'MARKET ROUT'), ('$93.5bn', 'ANTHROPIC IPO'), ('51-48', 'IRAN WAR POWERS'), ('2.6%', 'TOKYO INFLATION'), ('10,000', 'ROHINGYA RESETTLED'))
    cell = WIDTH / len(stats)
    for index, (number, title) in enumerate(stats):
        x = EDGE + index * cell
        first = len(page.text_boxes)
        if index:
            page.rect(x, 145, 0.5, 49, RULE)
        centered(page, number, x + 4, 147, cell - 8, 27, (RED, BLUE)[index % 2], weight=5, font=HEADLINE)
        centered(page, title, x + 4, 187, cell - 8, 8, GREY, font=TAG, tracking=0.4)
        check_bounds(page, first, x + 4, 145, cell - 8, 53)
    page.rect(EDGE, 202, WIDTH, 2, RED)

class Illustration:

    def __init__(self, page, x, y, width, height):
        self.page, self.x, self.y = (page, x, y)
        self.width, self.height = (width, height)
        self.shapes = 0

    def bounds(self, left, top, right, bottom):
        assert 0 <= left <= right <= self.width and 0 <= top <= bottom <= self.height
        self.shapes += 1
        assert self.shapes <= 60

    def rect(self, x, y, w, h, color):
        self.bounds(x, y, x + w, y + h)
        self.page.rect(self.x + x, self.y + y, w, h, color)

    def dot(self, x, y, r, color):
        self.bounds(x - r, y - r, x + r + 0.5, y + r + 0.5)
        self.page.dot(self.x + x, self.y + y, r, color)

    def path(self, points, color, weight=3):
        xs, ys = zip(*points)
        pad = weight / (2 * SCALE) + 0.5
        self.bounds(min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)
        for (x, y), (xx, yy) in zip(points, points[1:]):
            self.page.line(self.x + x, self.y + y, self.x + xx, self.y + yy, color, weight)

    def polygon(self, points, color):
        xs, ys = zip(*points)
        self.bounds(min(xs), min(ys), max(xs), max(ys))
        edges = list(zip(points, points[1:] + points[:1]))
        for row in range(round(min(ys) * SCALE), round(max(ys) * SCALE)):
            y = (row + 0.5) / SCALE
            hits = sorted((x + (y - y0) * (xx - x) / (y1 - y0) for (x, y0), (xx, y1) in edges if min(y0, y1) <= y < max(y0, y1)))
            assert len(hits) % 2 == 0
            for left, right in zip(hits[::2], hits[1::2]):
                self.page.rect(self.x + left, self.y + row / SCALE, right - left, 1 / SCALE, color)

    def type(self, text, x, y, width, size, color, font=TAG, weight=2):
        first = len(self.page.text_boxes)
        centered(self.page, text, self.x + x, self.y + y, width, size, color, font=font, weight=weight)
        check_bounds(self.page, first, self.x + x, self.y + y, width, self.height - y)

def summit_art(art):
    backdrop = (39, 36, 44)
    cream, gold, scarlet = ((252, 242, 221), (242, 185, 79), (219, 70, 53))
    art.rect(0, 0, art.width, art.height, backdrop)
    art.rect(12, 12, art.width - 24, 112, (66, 54, 60))
    for y in (16, 20, 102):
        art.rect(16, y, art.width - 32, 1, (103, 77, 73))
    for center, name, jacket, halo, skin, hair in ((56, 'TRUMP', BLUE, (81, 109, 157), (242, 177, 136), gold), (154, 'XI', scarlet, (164, 65, 51), (232, 167, 119), (40, 32, 32)), (252, 'PUTIN', BLUE, (92, 118, 159), (235, 188, 158), (180, 156, 133))):

        def poly(points, color):
            art.polygon(tuple(((center + x, y) for x, y in points)), color)
        art.dot(center, 57, 41, halo)
        art.rect(center - 7, 67, 14, 17, skin)
        poly(((-40, 109), (-35, 88), (-10, 77), (10, 77), (35, 88), (40, 109)), jacket)
        art.rect(center - 14, 34, 28, 26, skin)
        art.dot(center, 58, 13.5, skin)
        poly(((-14, 44), (-16, 35), (-7, 27), (11, 26), (16, 32), (13, 42), (9, 35), (-8, 37)), hair)
        art.rect(center - 8, 50, 3, 2, INK)
        art.rect(center + 5, 50, 3, 2, INK)
        art.path(((center, 51), (center - 2, 57), (center + 1, 57)), (158, 96, 73), 2)
        art.rect(center - 4, 62, 8, 1, (138, 79, 59))
        poly(((-11, 77), (11, 77), (0, 98)), gold if name == 'XI' else cream)
        poly(((0, 82), (3, 89), (0, 104), (-3, 89)), gold if name == 'XI' else scarlet)
        seam = tuple((channel * 3 // 4 for channel in jacket))
        art.path(((center - 15, 82), (center - 19, 89), (center - 8, 102)), seam)
        art.path(((center + 15, 82), (center + 19, 89), (center + 8, 102)), seam)
        if name == 'TRUMP':
            for y, color in ((92, scarlet), (95, cream), (98, scarlet)):
                art.rect(center - 28, y, 11, 2, color)
        elif name == 'XI':
            poly(((-23, 87), (-21, 91), (-17, 92), (-21, 95), (-23, 99), (-25, 95), (-29, 92), (-25, 91)), gold)
        else:
            for y, color in ((91, cream), (94, (82, 136, 207)), (97, scarlet)):
                art.rect(center - 28, y, 11, 3, color)
        art.rect(center - 37, 108, 74, 18, cream)
        art.type(name, center - 37, 112, 74, 8.5, INK)

def court_art(art):
    backdrop, field = ((31, 46, 58), (39, 63, 79))
    stone, light, gold = ((190, 175, 145), (247, 232, 202), (245, 180, 72))
    art.rect(0, 0, art.width, art.height, backdrop)
    art.rect(12, 12, art.width - 24, 112, field)
    art.polygon(((29, 57), (113, 20), (197, 57)), light)
    art.polygon(((58, 51), (113, 29), (168, 51)), stone)
    art.dot(113, 43, 4, backdrop)
    art.rect(203, 23, 1, 96, (67, 89, 103))
    art.rect(37, 57, 152, 8, stone)
    for x in (48, 75, 102, 129, 156):
        art.rect(x, 67, 18, 5, light)
        art.rect(x + 3, 72, 12, 33, light)
        art.rect(x + 12, 72, 3, 33, stone)
        art.rect(x + 7, 74, 0.5, 29, stone)
        art.rect(x, 105, 18, 4, light)
    art.rect(38, 109, 151, 5, light)
    art.rect(31, 114, 165, 5, stone)
    art.rect(23, 119, 181, 5, light)
    art.path(((252, 31), (252, 85)), gold, 5)
    art.path(((230, 42), (274, 42)), gold, 5)
    art.dot(252, 33, 4, light)
    for x in (230, 274):
        art.path(((x - 11, 67), (x, 44), (x + 11, 67)), light)
        art.polygon(((x - 13, 67), (x + 13, 67), (x + 7, 74), (x - 7, 74)), gold)
    art.rect(236, 84, 32, 4, gold)
    art.rect(221, 99, 62, 25, light)
    art.type('9-6', 221, 105, 62, 13, INK, weight=3)

def climate_art(art):
    field, water, leaf = ((38, 69, 65), (67, 125, 170), (159, 198, 138))
    white, heat = ((250, 231, 191), (226, 76, 53))
    art.rect(0, 0, art.width, art.height, (29, 47, 45))
    art.rect(12, 12, art.width - 24, 112, field)
    for y in (33, 54, 75):
        art.path(((27, y), (43, y - 4), (59, y + 1), (76, y - 3)), (70, 106, 96), 2)
    art.dot(129, 60, 42, (73, 100, 85))
    art.dot(129, 60, 38, water)
    art.path(((94, 48), (164, 48)), (138, 174, 190))
    art.path(((92, 68), (166, 68)), (138, 174, 190))
    art.path(((128, 23), (115, 35), (110, 59), (116, 85), (128, 97)), (138, 174, 190))
    art.path(((130, 23), (143, 35), (148, 59), (142, 85), (130, 97)), (138, 174, 190))
    art.polygon(((102, 37), (116, 28), (129, 35), (127, 43), (112, 46), (115, 57), (107, 58), (98, 49)), leaf)
    art.polygon(((114, 56), (129, 60), (135, 70), (126, 82), (120, 91), (115, 78)), leaf)
    art.polygon(((146, 36), (153, 32), (163, 44), (166, 58), (156, 59), (152, 70), (145, 63), (147, 53), (135, 48)), leaf)
    art.dot(208, 79, 14, white)
    art.dot(208, 31, 8, white)
    art.rect(200, 31, 16, 48, white)
    art.rect(205, 48, 6, 32, heat)
    art.dot(208, 79, 9, heat)
    for y in (36, 46, 56, 66):
        art.rect(222, y, 9, 2, white)
    art.path(((246, 70), (258, 59), (270, 59), (281, 44)), (199, 149, 83))
    art.rect(25, 103, art.width - 50, 22, white)
    art.rect(25, 103, 3, 22, AMBER)
    first = len(art.page.text_boxes)
    art.type('"leaves out the goal for fossil-fuel aid"', 33, 108, art.width - 66, 8.5, INK, font=condensed(0.9, ROMAN), weight=3)
    check_bounds(art.page, first, art.x + 33, art.y + 107, art.width - 66, 15)

def casualty_art(art):
    art.rect(0, 0, art.width, art.height, (43, 39, 39))
    art.rect(0, 0, 5, art.height, RED)
    art.type('OVERNIGHT ATTACK · UKRAINE', 12, 12, art.width - 24, 8, PAPER)
    art.type('8', 14, 33, 86, 62, PAPER, font=HEADLINE, weight=7)
    for index in range(8):
        x, y = (132 + index % 4 * 39, 43 + index // 4 * 37)
        art.dot(x, y, 5, (211, 182, 158))
        art.rect(x - 7, y + 8, 14, 15, (173, 114, 105))
    art.rect(15, 111, art.width - 30, 1, (140, 106, 99))
    art.type('KILLED IN UKRAINE', 15, 120, art.width - 30, 9, PAPER)

def market_art(art):
    art.rect(0, 0, art.width, art.height, (41, 49, 53))
    art.rect(0, 0, 5, art.height, RED)
    art.type('GLOBAL EQUITIES · VALUE WIPED OUT', 12, 12, art.width - 24, 8, PAPER)
    art.type('$9tn', 12, 34, 144, 43, PAPER, font=HEADLINE, weight=6)
    for y in (42, 65, 88):
        art.path(((169, y), (289, y)), (78, 86, 88), 2)
    art.path(((177, 36), (177, 51), (278, 92)), (225, 138, 118), 6)
    art.polygon(((263, 91), (283, 97), (278, 77)), (225, 138, 118))
    art.rect(15, 111, art.width - 30, 1, (105, 116, 119))
    art.type('VIX 30 · AI FEARS HIT STOCKS', 15, 120, art.width - 30, 9, PAPER)

def section_header(page, title, right, y):
    page.rect(EDGE, y, 4, 12, RED)
    label(page, title, EDGE + 11, y, 389, 10.5, RED, weight=3, tracking=0.92)
    width = measure(right, 8.5, TAG, 0.75)
    label(page, right, EDGE + WIDTH - width - 2, y + 1, width + 2, 8.5, tracking=0.75)

def hero_row(page):
    section_header(page, 'THE FRONT PAGE', 'DIPLOMACY · CONFLICT · MARKETS', 214)
    art_top, bottom = (229, 510)
    column_rules(page, art_top, bottom - 6)
    for index, ((title, caption, lines, detail, source), draw) in enumerate(zip(HEROES, (summit_art, casualty_art, market_art))):
        x = EDGE + index * (COLUMN + GUTTER)
        first = len(page.text_boxes)
        draw(Illustration(page, x, art_top, COLUMN, 138))
        copy_start = len(page.text_boxes)
        label(page, title, x, 373, COLUMN, 10, RED, weight=3, tracking=0.7)
        label(page, caption, x, 387, COLUMN, 7.3, tracking=0.25)
        for line_index, line in enumerate(lines):
            label(page, line, x, 399 + line_index * 28, COLUMN, 18, weight=4, font=HERO_HEADLINE, tracking=0.15)
        detail_size = 8
        detail_lines = wrap(detail, detail_size, COLUMN - 3, SANS)
        assert len(detail_lines) == 2, (source, detail_lines)
        for line_index, line in enumerate(detail_lines):
            label(page, line, x, 457 + line_index * 14, COLUMN, detail_size, font=SANS, tracking=0)
        byline(page, source, x, COLUMN, bottom)
        copy = page.text_boxes[copy_start:]
        for (a, box), (b, following) in zip(copy, copy[1:]):
            assert round((following[1] - box[3]) * SCALE) >= 2, (a, b, box, following)
        check_bounds(page, first, x, art_top, COLUMN, bottom - art_top)
        page.rendered.append(lines[0])

def small_icon(art, icon, color):
    art.rect(0, 0, 49, 49, (232, 223, 205))
    if icon == 'bridge':
        art.rect(6, 28, 37, 4, color)
        for x in (13, 33):
            art.rect(x, 14, 3, 23, color)
        art.path(((7, 25), (14, 15), (24, 25), (34, 15), (42, 25)), color, 4)
        art.path(((8, 40), (41, 40)), color, 2)
    elif icon == 'missile':
        art.polygon(((12, 30), (30, 12), (40, 9), (37, 19), (19, 37), (13, 36)), color)
        art.polygon(((14, 26), (10, 24), (17, 17), (23, 17), (31, 25), (31, 31), (24, 38), (22, 33)), color)
        art.path(((9, 39), (14, 34)), AMBER, 4)
    elif icon == 'chart':
        art.path(((9, 10), (9, 39), (41, 39)), color)
        art.path(((13, 15), (22, 22), (27, 19), (39, 32)), color, 5)
        art.polygon(((32, 32), (40, 25), (40, 34)), color)
    elif icon == 'court':
        art.polygon(((7, 18), (24, 8), (42, 18)), color)
        art.rect(8, 20, 33, 3, color)
        for x in (12, 22, 32):
            art.rect(x, 25, 4, 13, color)
        art.rect(8, 40, 33, 3, color)
    elif icon == 'game':
        art.polygon(((9, 18), (39, 18), (43, 31), (39, 36), (34, 35), (29, 30), (20, 30), (15, 35), (9, 36), (6, 31)), color)
        art.rect(12, 23, 10, 2, PAPER)
        art.rect(16, 19, 2, 10, PAPER)
        art.dot(33, 23, 1.6, PAPER)
        art.dot(37, 27, 1.6, PAPER)
    elif icon == 'fist':
        art.polygon(((16, 37), (16, 29), (10, 23), (10, 18), (14, 16), (18, 21), (18, 13), (35, 13), (38, 18), (38, 26), (32, 33), (32, 37)), color)
        for x, y in ((18, 10), (23, 8), (28, 9), (33, 11)):
            art.rect(x, y, 4, 11, color)
        art.path(((14, 20), (23, 24), (29, 22)), PAPER, 3)
        art.rect(16, 39, 16, 3, color)
    else:
        assert icon == 'medal'
        art.polygon(((12, 8), (20, 8), (28, 27), (19, 29)), color)
        art.polygon(((28, 8), (36, 8), (29, 29), (21, 27)), color)
        art.dot(24, 32, 9, AMBER)
        art.dot(24, 32, 5, color)
        art.rect(23, 29, 2, 6, PAPER)

def secondary_grid(page):
    page.rect(EDGE, 510, WIDTH, 3, RED)
    section_header(page, 'AROUND THE WORLD', 'EIGHT STORIES · CITY DISPATCHES', 523)
    card_width, card_height, gap = (226, 118, 64 / 3)
    assert len(FEATURES) == 8
    for index, (desk, city, icon, headline, detail, source) in enumerate(FEATURES):
        row, col = divmod(index, 4)
        x, y = (round((EDGE + col * (card_width + gap)) * SCALE) / SCALE, 544 + row * 119)
        first = len(page.text_boxes)
        page.rect(x, y, card_width, 2, RED)
        page.rect(x, y + 9, 3, 10, DESK_COLORS[desk])
        label(page, desk, x + 8, y + 10, card_width - 8, 6.7, DESK_COLORS[desk], weight=3, tracking=0.25)
        label(page, city, x, y + 21, card_width - 53, 7.2, GREY, tracking=0.8)
        small_icon(Illustration(page, x + 177, y + 18, 49, 49), icon, DESK_COLORS[desk])
        inner, headline_size, leading = (167, 11.5, 18)
        lines = wrap(headline, headline_size, inner - 3, HEADLINE)
        assert 1 <= len(lines) <= 3
        for line_index, line in enumerate(lines):
            label(page, line, x, y + 31 + line_index * leading, inner, headline_size, INK, weight=3, font=HEADLINE, tracking=0)
        detail_y = y + 31 + len(lines) * leading + 2
        for line_index, line in enumerate(wrap(detail, 6.3, card_width - 2, TAG)):
            label(page, line, x, detail_y + line_index * 11, card_width, 6.3, font=TAG, tracking=0)
        byline(page, source, x, card_width, y + card_height)
        check_bounds(page, first, x, y, card_width, card_height)
        page.rendered.append(headline)

def dispatch_row(page):
    page.rect(EDGE, 727, WIDTH, 1, INK)
    cell = WIDTH / len(DISPATCHES)
    for index, (desk, headline, source) in enumerate(DISPATCHES):
        left = EDGE + index * cell
        x = round((left + (10 if index else 0)) * SCALE) / SCALE
        inner = left + cell - x - 7
        first = len(page.text_boxes)
        if index:
            page.rect(left, 735, 0.5, 61, RULE)
        label(page, desk, x, 736, inner, 7.5, DESK_COLORS[desk], weight=3, tracking=0.55)
        for line_index, line in enumerate(headline.splitlines()):
            label(page, line, x, 748 + line_index * 18, inner, 11.5, INK, weight=3, font=HEADLINE)
        label(page, source, x, 784, inner, 7.3, tracking=0.35)
        check_bounds(page, first, x, 735, inner, 61)
        page.rendered.append(headline)

def dot_map(page, x, y):
    step = 1.45
    mw, mh = (MASK_COLS * step, MASK_ROWS * step)
    packed = base64.b64decode(LANDMASK_B64, validate=True)
    assert len(packed) * 8 == MASK_COLS * MASK_ROWS
    for row in range(0, MASK_ROWS, 2):
        for col in range(0, MASK_COLS, 2):
            bit = row * MASK_COLS + col
            if packed[bit // 8] & 128 >> bit % 8:
                page.dot(x + (col + 0.5) * step, y + (row + 0.5) * step, 0.55, LAND)
    groups = {}
    for number, (region, _, _) in enumerate(BULLETINS, 1):
        groups.setdefault(region, []).append(number)
    boxes = {'ASIA': (195, 35, 220, 63), 'EUROPE': (125, 14, 150, 28), 'RUSSIA & UKRAINE': (177, 9, 202, 23), 'MIDDLE EAST': (151, 44, 176, 58), 'AFRICA': (124, 76, 149, 90), 'AMERICAS': (53, 48, 78, 76), 'TECHNOLOGY & BUSINESS': (65, 24, 90, 38)}
    selected = [(region, numbers[rank], rank) for rank in range(max(map(len, groups.values()))) for region, numbers in groups.items() if rank < len(numbers)][:16]
    pins, represented = ([], set())
    for region, number, rank in selected:
        left, top, right, bottom = boxes[region]
        col, row = (rank % 2, rank // 2)
        jitter_x = (number * 7 % 3 - 1) / 3
        jitter_y = (number * 11 % 3 - 1) / 3
        px = x + left + col * (right - left) + jitter_x
        py = y + top + row * (bottom - top) + col * 2 + jitter_y
        assert x + 3 <= px <= x + mw - 19 and y + 5 <= py <= y + mh - 8
        assert all((math.hypot(px - xx, py - yy) >= 12 for xx, yy in pins))
        pins.append((px, py))
        represented.add(region)
        page.dot(px, py, 2.5, DESK_COLORS[region])
        text, tx, ty = (f'{number:02d}', px + 4, py - 4)
        first = len(page.text_boxes)
        label(page, text, tx + 1, ty + 1, 15, 6.7, PAPER, weight=5, font=TAG, tracking=0)
        del page.text_boxes[first:]
        label(page, text, tx, ty, 15, 6.7, INK, weight=3, font=TAG, tracking=0)
    assert len(pins) == 16 and represented == set(groups)
    page.map_pins = len(pins)

def ticker(page):
    page.rect(EDGE, 787, WIDTH, 3, RED)
    section_header(page, 'WHERE IT HAPPENED', '20 BRIEFS · MAP PINS MATCH REGION CODES', 800)
    dot_map(page, EDGE, 827)
    label(page, 'REGION CENTROIDS · NATURAL EARTH 1:110M', EDGE, 959, 260, 6.0, tracking=0.15)
    for col, x in enumerate((307, 654)):
        page.rect(x - 9, 827, 0.5, 137, RULE)
        for row, (region, headline, _) in enumerate(BULLETINS[col * 10:(col + 1) * 10]):
            number = col * 10 + row + 1
            row_height = 14
            y = 830 + row * row_height
            color = DESK_COLORS[region]
            page.rect(x, y, 2, 8, color)
            label(page, f'{number:02d}', x + 5, y, 16, 7.0, GREY, tracking=0)
            label(page, REGION_CODES[region], x + 24, y, 17, 7.0, color, weight=3, tracking=0)
            label(page, headline, x + 45, y, 292 if col == 0 else 297, 7.3, INK, font=TAG, tracking=0)
            page.rendered.append(headline)

def footer(page):
    page.rect(EDGE, 971, WIDTH, 2, RED)
    page.rect(EDGE, 975, WIDTH, 0.5, RULE)
    centered(page, 'DATE CHECK: Every story on this paper happened on or before 20 Nov 2026', EDGE, 987, WIDTH, 8.8, INK, weight=2, tracking=0.22)
    centered(page, 'SOURCES: REUTERS, AP, AFP, BBC, AL JAZEERA, CNN, NBC, TIMES OF INDIA, GUARDIAN — 2026-11-20', EDGE, 1003, WIDTH, 8, GREY, font=TAG, tracking=0.32)

def main():
    page = Page()
    count = sum(map(len, (HEROES, FEATURES, BULLETINS)))
    masthead(page, count)
    stats_bar(page)
    hero_row(page)
    secondary_grid(page)
    ticker(page)
    footer(page)
    assert len(page.rendered) == len(set(page.rendered)) == count == 31
    for i, (a, box) in enumerate(page.text_boxes):
        for b, other in page.text_boxes[i + 1:]:
            overlap = min(box[2], other[2]) > max(box[0], other[0]) and min(box[3], other[3]) > max(box[1], other[1])
            assert not overlap, ('text overlap', a, b, box, other)
    png = page.png()
    assert len(png) <= 1048576
    output = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(output, exist_ok=True)
    path = os.path.join(output, 'entry.png')
    with open(path, 'wb') as f:
        f.write(png)
    print(json.dumps({'output': path, 'bytes': len(png), 'sha256': hashlib.sha256(png).hexdigest(), 'stories': len(page.rendered), 'cards': len(FEATURES), 'ticker_items': len(BULLETINS), 'map_pins': page.map_pins, 'width': 1024, 'height': 1024, 'text_bounds_checked': len(page.text_boxes), 'layout': 'The World in One Day newspaper front page'}, sort_keys=True))
if __name__ == '__main__':
    main()
