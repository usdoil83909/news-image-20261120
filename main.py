"""A display-list typesetter and deterministic raster press for a daily edition."""

import base64 as radix
import hashlib as digests
import json as reporting
import math as geometry
import os as filesystem
import struct as binary
import zlib as deflate


RESOLUTION = 1 << 10
ZOOM = 3
RASTER_EDGE = RESOLUTION * ZOOM
COLORS = {
    'paper': (244, 239, 227), 'ink': (27, 27, 27),
    'red': (116, 31, 41), 'blue': (31, 78, 156),
    'amber': (217, 142, 43), 'grey': (88, 82, 74),
    'rule': (174, 164, 147), 'land': (116, 110, 99),
}
MARGIN, LIVE_WIDTH, LEAD_WIDTH = 28, 968, 308


def pigment(value):
    return COLORS[value] if isinstance(value, str) else value


def device(value):
    return round(ZOOM * value)


class DisplayList:
    """Collect geometry before allocating or painting the raster surface."""

    def __init__(self):
        self.operations = []
        self.copy_bounds = []
        self.stories = []
        self.pin_count = 0

    def box(self, left, top, width, height, shade):
        edges = tuple(map(device, (left, top, left + width, top + height)))
        self.operations.append(('box', edges, pigment(shade)))

    def circle(self, cx, cy, radius, shade):
        self.operations.append(('disc', (device(cx), device(cy), radius * ZOOM), pigment(shade)))

    def trace(self, vertices, shade, thickness):
        self.operations.append(('pen', (tuple(vertices), thickness), pigment(shade)))

    def segment(self, begin, finish, shade, thickness=3):
        vertices = tuple((device(a), device(b)) for a, b in (begin, finish))
        self.trace(vertices, shade, max(1, round(thickness * ZOOM / 2)))


class RasterPress:
    """Interpret three drawing instructions on an integer RGB backing store."""

    def __init__(self):
        self.buffer = bytearray(bytes(COLORS['paper']) * (RASTER_EDGE ** 2))

    def span(self, y, first, stop, rgb):
        assert 0 <= first <= stop <= RASTER_EDGE
        assert 0 <= y < RASTER_EDGE
        address = 3 * (y * RASTER_EDGE + first)
        self.buffer[address:address + 3 * (stop - first)] = rgb * (stop - first)

    def dab(self, x, y, rgb):
        self.span(y, x, x + 1, rgb)

    def pen(self, vertices, diameter, rgb):
        negative = -(diameter // 2)
        brush = range(negative, negative + diameter)
        for start, end in zip(vertices[:-1], vertices[1:]):
            horizontal, vertical = start
            target_x, target_y = end
            run = abs(target_x - horizontal)
            fall = -abs(target_y - vertical)
            vertical_brush = -fall <= run
            direction_x = 1 if horizontal < target_x else -1
            direction_y = 1 if vertical < target_y else -1
            balance = run + fall
            while True:
                for displacement in brush:
                    px = horizontal if vertical_brush else horizontal + displacement
                    py = vertical + displacement if vertical_brush else vertical
                    self.dab(px, py, rgb)
                if (horizontal, vertical) == end:
                    break
                doubled = balance * 2
                if doubled >= fall:
                    balance = balance + fall
                    horizontal = horizontal + direction_x
                if doubled <= run:
                    balance = balance + run
                    vertical = vertical + direction_y
        cap_radius = diameter / 2
        cap_limit = geometry.floor(cap_radius)
        for horizontal, vertical in vertices:
            for offset in range(-cap_limit, cap_limit + 1):
                reach = geometry.floor(geometry.sqrt(max(0, cap_radius ** 2 - offset ** 2)))
                self.span(vertical + offset, horizontal - reach, horizontal + reach + 1, rgb)

    def paint(self, instructions):
        for opcode, operands, color in instructions:
            rgb = bytes(color)
            if opcode == 'pen':
                self.pen(operands[0], operands[1], rgb)
            elif opcode == 'box':
                west, north, east, south = operands
                for scan in range(north, south):
                    self.span(scan, west, east, rgb)
            else:
                horizontal, vertical, radius = operands
                for offset in range(-round(radius), round(radius) + 1):
                    reach = geometry.floor(geometry.sqrt(max(0, radius ** 2 - offset ** 2)))
                    self.span(vertical + offset, horizontal - reach, horizontal + reach + 1, rgb)

    def encode(self):
        reduced = bytearray()
        row_bytes = RASTER_EDGE * 3
        for output_y in range(RESOLUTION):
            reduced.extend(b'\0')
            origin = output_y * ZOOM * row_bytes
            for output_x in range(RESOLUTION):
                start = origin + output_x * 9
                for component in range(3):
                    address = start + component
                    sample = 0
                    for row_offset in (0, row_bytes, row_bytes * 2):
                        cell = address + row_offset
                        sample += self.buffer[cell] + self.buffer[cell + 3] + self.buffer[cell + 6]
                    reduced.append((sample + 4) // 9)
        blocks = [(b'IHDR', binary.pack('>2I5B', RESOLUTION, RESOLUTION, 8, 2, 0, 0, 0)),
                  (b'IDAT', deflate.compress(reduced, level=9)), (b'IEND', bytes())]
        payload = bytearray.fromhex('89504e470d0a1a0a')
        for name, content in blocks:
            payload.extend(binary.pack('>I', len(content)))
            payload.extend(name + content)
            payload.extend(binary.pack('>I', deflate.crc32(name + content) & 0xffffffff))
        return bytes(payload)


# One record per printable ASCII character; the separator is not a pen command.
LETTER_SOURCE = r'''JZ|MWRFRT RRYQZR[SZRY|JZNFNM RVFVM
H]SBLb RYBRb RLOZO RKUYU
H\PBP_ RTBT_ RYIWGTFPFMGKIKKLMMNOOUQWRXSYUYXWZT[P[MZKX
F^[FI[ RNFPHPJOLMMKMIKIIJGLFNFPGSHVHYG[F RWTUUTWTYV[X[ZZ[X[VYTWT
E_\O\N[MZMYNXPVUTXRZP[L[JZIYHWHUISJRQNRMSKSIRGPFNGMIMKNNPQUXWZY[[[\Z\Y
MWRHQGRFSGSIRKQL|KYVBTDRGPKOPOTPYR]T`Vb|KYNBPDRGTKUPUTTYR]P`Nb
JZRLRX RMOWU RWOMU|E_RIR[ RIR[R|NVSWRXQWRVSWSYQ[|E_IR[R
NVRVQWRXSWRV|G][BIb|H\QFNGLJKOKRLWNZQ[S[VZXWYRYOXJVGSFQF
H\NJPISFS[|H\LKLJMHNGPFTFVGWHXJXLWNUQK[Y[
H\MFXFRNUNWOXPYSYUXXVZS[P[MZLYKW|H\UFKTZT RUFU[
H\WFMFLOMNPMSMVNXPYSYUXXVZS[P[MZLYKW
H\XIWGTFRFOGMJLOLTMXOZR[S[VZXXYUYTXQVOSNRNOOMQLT|H\YFO[ RKFYF
H\PFMGLILKMMONSOVPXRYTYWXYWZT[P[MZLYKWKTLRNPQOUNWMXKXIWGTFPF
H\XMWPURRSQSNRLPKMKLLINGQFRFUGWIXMXRWWUZR[P[MZLX
NVROQPRQSPRO RRVQWRXSWRV|NVROQPRQSPRO RSWRXQWRVSWSYQ[
F^ZIJRZ[|E_IO[O RIU[U|F^JIZRJ[|I[LKLJMHNGPFTFVGWHXJXLWNVORQRT RRYQZR[SZRY
E`WNVLTKQKOLNMMPMSNUPVSVUUVS RQKOMNPNSOUPV RWKVSVUXVZV\T]Q]O\L[JYHWGTFQFNGLHJJILHOHRIUJWLYNZQ[T[WZYYZX RXKWSWUXV
I[RFJ[ RRFZ[ RMTWT|G\KFK[ RKFTFWGXHYJYLXNWOTP RKPTPWQXRYTYWXYWZT[K[
H]ZKYIWGUFQFOGMILKKNKSLVMXOZQ[U[WZYXZV|G\KFK[ RKFRFUGWIXKYNYSXVWXUZR[K[
H[LFL[ RLFYF RLPTP RL[Y[|HZLFL[ RLFYF RLPTP
H]ZKYIWGUFQFOGMILKKNKSLVMXOZQ[U[WZYXZVZS RUSZS|G]KFK[ RYFY[ RKPYP
NVRFR[|JZVFVVUYTZR[P[NZMYLVLT|G\KFK[ RYFKT RPOY[|HYLFL[ RL[X[
F^JFJ[ RJFR[ RZFR[ RZFZ[|G]KFK[ RKFY[ RYFY[
G]PFNGLIKKJNJSKVLXNZP[T[VZXXYVZSZNYKXIVGTFPF
G\KFK[ RKFTFWGXHYJYMXOWPTQKQ
G]PFNGLIKKJNJSKVLXNZP[T[VZXXYVZSZNYKXIVGTFPF RSWY]
G\KFK[ RKFTFWGXHYJYLXNWOTPKP RRPY[|H\YIWGTFPFMGKIKKLMMNOOUQWRXSYUYXWZT[P[MZKX
JZRFR[ RKFYF|G]KFKULXNZQ[S[VZXXYUYF|I[JFR[ RZFR[|F^HFM[ RRFM[ RRFW[ R\FW[
H\KFY[ RYFK[|I[JFRPR[ RZFRP|H\YFK[ RKFYF RK[Y[|KYOBOb RPBPb ROBVB RObVb
KYKFY^|KYTBTb RUBUb RNBUB RNbUb|JZRDJR RRDZR|I[Ib[b|NVSKQMQORPSORNQO
I\XMX[ RXPVNTMQMONMPLSLUMXOZQ[T[VZXX|H[LFL[ RLPNNPMSMUNWPXSXUWXUZS[P[NZLX
I[XPVNTMQMONMPLSLUMXOZQ[T[VZXX|I\XFX[ RXPVNTMQMONMPLSLUMXOZQ[T[VZXX
I[LSXSXQWOVNTMQMONMPLSLUMXOZQ[T[VZXX|MYWFUFSGRJR[ ROMVM
I\XMX]W`VaTbQbOa RXPVNTMQMONMPLSLUMXOZQ[T[VZXX|I\MFM[ RMQPNRMUMWNXQX[
NVQFRGSFREQF RRMR[|MWRFSGTFSERF RSMS^RaPbNb|IZMFM[ RWMMW RQSX[|NVRFR[
CaGMG[ RGQJNLMOMQNRQR[ RRQUNWMZM\N]Q][|I\MMM[ RMQPNRMUMWNXQX[
I\QMONMPLSLUMXOZQ[T[VZXXYUYSXPVNTMQM|H[LMLb RLPNNPMSMUNWPXSXUWXUZS[P[NZLX
I\XMXb RXPVNTMQMONMPLSLUMXOZQ[T[VZXX|KXOMO[ ROSPPRNTMWM
J[XPWNTMQMNNMPNRPSUTWUXWXXWZT[Q[NZMX|MYRFRWSZU[W[ ROMVM
I\MMMWNZP[S[UZXW RXMX[|JZLMR[ RXMR[|G]JMN[ RRMN[ RRMV[ RZMV[
J[MMX[ RXMM[|JZLMR[ RXMR[P_NaLbKb|J[XMM[ RMMXM RM[X[
KYTBRCQDPFPHQJRKSMSOQQ RRCQEQGRISJTLTNSPORSTTVTXSZR[Q]Q_Ra RQSSUSWRYQZP\P^Q`RaTb
NVRBRb
KYPBRCSDTFTHSJRKQMQOSQ RRCSESGRIQJPLPNQPURQTPVPXQZR[S]S_Ra RSSQUQWRYSZT\T^S`RaPb
F^IUISJPLONOPPTSVTXTZS[Q RISJQLPNPPQTTVUXUZT[Q[O'''


def unpack_letter(record):
    bearings = [ord(mark) - ord('R') for mark in record[:2]]
    contours = []
    for section in record[2:].split(' R'):
        coordinates = [ord(mark) - ord('R') for mark in section]
        assert len(coordinates) % 2 == 0, record
        if coordinates:
            contours.append(tuple(zip(coordinates[0::2], coordinates[1::2])))
    return (*bearings, tuple(contours))


def squeeze(alphabet, ratio):
    result = {}
    for character, (west, east, contours) in alphabet.items():
        transformed = []
        for contour in contours:
            transformed.append(tuple((abscissa * ratio, ordinate) for abscissa, ordinate in contour))
        result[character] = west * ratio, east * ratio, tuple(transformed)
    return result


def assemble_typefaces():
    records = LETTER_SOURCE.replace('|', '\n').splitlines()
    assert len(records) == 95
    plain = {chr(32 + index): unpack_letter(record) for index, record in enumerate(records)}
    plain.update({'·': (-5, 5, (((-.7, 0), (.7, 0)),)),
                  '—': (-12, 12, (((-10, 0), (10, 0)),))})
    roman = plain.copy()
    punctuation = [('*', 'JZRFRR RMIWO RWIMO'), (',', r'MWSZR[QZRYSZS\R^Q_'),
                   ('.', 'MWRYQZR[SZRY'), (':', 'MWRMQNROSNRM RRYQZR[SZRY'),
                   (';', r'MWRMQNROSNRM RSZR[QZRYSZS\R^Q_'),
                   ('^', 'JZPLRITL RMORJWO RRJR['), ('_', 'JZJ]Z]'),
                   ('`', 'MWSFRGQIQKRLSKRJ')]
    for character, record in punctuation:
        roman[character] = unpack_letter(record)
    decorated = roman.copy()
    for character in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':
        west, east, contours = roman[character]
        ends, reinforcements = set(), []
        for contour in contours:
            if len(contour) <= 1:
                continue
            for tip, neighbor in [(contour[0], contour[1]), (contour[-1], contour[-2])]:
                if tip[1] in {-12, -5, 9} and abs(neighbor[1] - tip[1]) >= 3:
                    ends.add(tip)
            for first, second in zip(contour[:-1], contour[1:]):
                if abs(second[0] - first[0]) <= 1 and abs(second[1] - first[1]) >= 5:
                    reinforcements.append(((first[0] + .65, first[1]), (second[0] + .65, second[1])))
        additions = [((u - 2.5, v), (u + 2.5, v)) for u, v in sorted(ends)]
        if character in '0235689':
            for contour in contours:
                if len(contour) > 2 and contour[0] != contour[-1]:
                    for u, v in (contour[0], contour[-1]):
                        additions.append(((u, v - 2), (u, v + 2)))
        extra_paths = tuple(reinforcements + additions)
        extremes = [u for contour in extra_paths for u, v in contour]
        if extremes:
            west, east = min(west, min(extremes) - 1), max(east, max(extremes) + 1)
        decorated[character] = west, east, contours + extra_paths
    return dict(body=plain, narrow=squeeze(plain, .72), tag=squeeze(plain, .86),
                mast=squeeze(decorated, .82), hero=squeeze(decorated, .72))


FACES = assemble_typefaces()


class Typesetter:
    """Measure copy and compile glyph strokes into the display list."""

    def __init__(self, display):
        self.display = display

    def extent(self, words, point_size, face='body', spacing=0):
        alphabet = FACES[face]
        units = sum(alphabet[letter][1] - alphabet[letter][0] for letter in words)
        return units * point_size / 21 + max(0, len(words) - 1) * spacing

    def paragraphs(self, words, point_size, available, face):
        rows = []
        pending = []
        for token in words.split():
            candidate = ' '.join(pending + [token])
            if pending and self.extent(candidate, point_size, face) > available:
                rows.append(' '.join(pending))
                pending = []
            pending.append(token)
        if pending:
            rows.append(' '.join(pending))
        return rows

    def put(self, words, left, top, available, point_size=8, shade='grey',
            thickness=2, face='tag', spacing=.38, align='left'):
        advance = self.extent(words, point_size, face, spacing)
        if align == 'center':
            inset = (available - advance) / 2
            assert inset >= 1, words
            left, available = left + inset, available - inset
        cursor = device(left) / ZOOM
        assert advance <= left + available - cursor + .001, words
        factor = point_size / 21
        paths = []
        for letter in words:
            west, east, contours = FACES[face][letter]
            for contour in contours:
                if len(contour) > 1:
                    paths.append(tuple((device(cursor + (u - west) * factor),
                                        device((v + 12) * factor)) for u, v in contour))
            cursor += (east - west) * factor + spacing
        if not paths:
            return
        radius = thickness // 2
        ceiling = min(v for contour in paths for u, v in contour) - radius
        correction = device(top) - ceiling
        shifted = [tuple((u, v + correction) for u, v in contour) for contour in paths]
        for contour in shifted:
            self.display.trace(contour, shade, thickness)
        west = min(u for contour in shifted for u, v in contour) - radius
        east = max(u for contour in shifted for u, v in contour) + radius + 1
        south = max(v for contour in shifted for u, v in contour) + radius + 1
        bounds = west / ZOOM, device(top) / ZOOM, east / ZOOM, south / ZOOM
        assert device(left) / ZOOM <= bounds[0] and bounds[2] <= left + available, (words, bounds)
        self.display.copy_bounds.append((words, bounds))

    def credit(self, words, left, available, floor):
        prior = self.display.copy_bounds[-1][1][3]
        top = geometry.ceil((prior + 8) * ZOOM) / ZOOM
        self.display.box(left, top + 3, 8, 1, 'red')
        self.put(words, left + 13, top, available - 13, 7.2, spacing=.62)
        assert floor - self.display.copy_bounds[-1][1][3] >= 10, words


DESKS = {
    'ASIA': ('AS', (142, 65, 38)),
    'EUROPE': ('EU', COLORS['blue']),
    'MIDDLE EAST': ('ME', (136, 82, 20)),
    'AFRICA': ('AF', (130, 52, 99)),
    'AMERICAS': ('AM', (164, 57, 48)),
    'RUSSIA & UKRAINE': ('RU', (48, 89, 112)),
    'TECHNOLOGY & BUSINESS': ('TB', (39, 104, 91)),
}

# Records are field-delimited editorial copy, independent of layout commands.
LEADS = '''SHENZHEN SUMMIT|APEC 2026 · SHENZHEN · THREE-WAY PEACE DECLARATION|Trump, Xi and Putin/issue peace declaration|Unprecedented three-way meeting dominated APEC leaders' gathering.|FROM AP
UKRAINE UNDER FIRE|KYIV · RUSSIA & UKRAINE · OVERNIGHT ATTACK|Russia launches/massive Ukraine attack|Kyiv bridges struck hours after Trump-Putin Xi peace declaration.|BY REUTERS
MARKETS IN ROUT|GLOBAL MARKETS · TECHNOLOGY & BUSINESS|Global stock rout/wipes nearly $9 trillion|VIX hits 30, highest since late March, amid AI fears.|BY REUTERS'''

CITY_COPY = '''EUROPE|LONDON|bridge|Britain and EU clinch trade deals|Summit reset still stuck on university tuition fee differences.|BY REUTERS
MIDDLE EAST|RIYADH|missile|Houthis fire missiles at Riyadh|Coalition also intercepted five drones and a ballistic missile.|BY AP
AFRICA|BADME|fist|Ethiopia and Eritrea mass troops|ACLED reports drone strikes near Badme; Eritrea denies buildup.|BY REUTERS
ASIA|TAIPEI|chart|Taiwan stocks suffer worst week since 1990|AI selloff wipes more than 16 percent from benchmark index.|BY REUTERS
AMERICAS|WASHINGTON|court|Senate rejects Iran war powers bid|Vote 51-48 defeats measure previously passed by House.|BY AP
TECHNOLOGY & BUSINESS|NEW YORK|chart|Anthropic shares tumble 9%|AI valuation concerns weigh heavily on technology stocks.|BY REUTERS
ASIA|TOKYO|chart|Japan inflation hits 2.6 percent|Prices remain in focus as Tokyo inflation reaches 2.6 percent.|BY REUTERS
AFRICA|DAKAR|fist|Senegal party expels President Faye|Party expels President Faye in a fresh political rupture.|BY REUTERS'''

BRIEF_COPY = '''ASIA|Trump, Xi and Putin issue peace deal
EUROPE|Russia violates Polish airspace three times
EUROPE|France seeks UN meeting after Kyiv strikes
RUSSIA & UKRAINE|Russia accuses Estonia of new Iron Curtain
EUROPE|Italy strike draws thousands into streets
EUROPE|de Villepin launches 2027 bid in Paris
MIDDLE EAST|Houthi attacks worry over Saudi nuclear pact
MIDDLE EAST|Two oil tankers hit mines in Hormuz
MIDDLE EAST|Israeli strikes kill six in central Gaza
AFRICA|Nigeria states approve state police change
AFRICA|Bayelsa funeral barge capsizes
AFRICA|South Sudan groups reject election delay
ASIA|Xi hails China-Australia turnaround
ASIA|Nepal PM Shah plans India visit
ASIA|Malaysia to resettle 10,000 Rohingya
AMERICAS|Virginia judge blocks Trump arch
AMERICAS|Florida carries out record 20th execution
AMERICAS|LatAm stocks tumble to one-year low
TECHNOLOGY & BUSINESS|Dollar index reaches 19-month high
TECHNOLOGY & BUSINESS|Gold falls 2 percent; copper weekly drop'''


def records(copy):
    return [record.split('|') for record in copy.splitlines()]


# Base64 transport is split into independent rows for review and maintenance.
WORLD_BITS = ''.join((
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    'AP//7//wAAAAAAAAAAAAAAAAAAAAAAB///////AA/wDwAAHgAAAAAAAAAAAHf//////4AB/gAAAAD+AAAAAAAAAAD/v/8///',
    '/4AA/gAA+ADf4AGAAAAAAAH///4A///4AAAAAH4Af/8AP8AAAAAAH///+Af//wAAAAAeD////+H4AAwH/gf////4P//wAAD8',
    'AeH///////wRw//////9/4P//AAAP/nP//////////+///////3/H/wuAAf//////////////////////+H/B/AB////////',
    '//////Df/////7/8D8A8AP//////////////A//////gf8B4AAAP/////////////8A/8////wP+AAAAGP5///////////fQ',
    'AHwB///8H/AAAAPD7/////////8B8AAeAB////v/wAAAfD//////////9B8AAAAB//////4AAAfv///////////B4AAAAAf/',
    '////4AAAX////////////AwAAAAAf/////8AAAH////////////gAAAAAAH/////8AAAH////////////AAAAAAAD/////gA',
    'AAB//7////////7gAAAAAAH////8AAAAf//7f///////3gAAAAAAH////wAAAAfy/////////+HAAAAAAAD///+AAAAAfi//',
    '///////+GAAAAAAAD///+AAAAAf/7////////+OAAAAAAAB///+AAAAAP/Bz///////n+AAAAAAAA///4AAAAAf/zB//////',
    '/jwAAAAAAAAf//wAAAAAf//////////hAAAAAAAAAP/9wAAAAB///////////wAAAAAAAAAP/A8AAAAD///////////gAAAA',
    'AAAAAH/AcAAAAD///////////gAAAAACAAAD/B8AAAAH//////H///+gAAAAADgAAAfPeAAAAH//////B///wgAAAAABgAAA',
    'f+P8AAAH////v+A/j/wwAAAAAAAAAAP+EsAAAH/////+A/B/hwAAAAAAAAAABfgAAAAH/////4A+B/hwAAAAAAAAAAAPgwAA',
    'AH/////wAeAfg4AAAAAAAAAAADj/AAAH/////wAcAXh4AAAAAAAAAAAB//gAAD/////wAOAbDcAAAAAAAAAAAAf/4AAB////',
    '/gAOAcC8AAAAAAAAAAAAH/+AAAfv///gACB8HIAAAAAAAAAAAAP/+AAAAD///AAAA8/EAAAAAAAAAAAAf//AAAAD//+AAAAe',
    '/+AAAAAAAAAAAAf//wAAAD//8AAAAO/38AAAAAAAAAAAf//+AAAD//4AAAAPf//mAAAAAAAAAAf///gAAB//wAAAAHHw/vAA',
    'AAAAAAAAf///gAAA//wAAAAD8AX9wAAAAAAAAAP///gAAA//wAAAAAf8PcYAAAAAAAAAP///AAAA//4AAAAAA57cMAAAAAAA',
    'AAH///AAAA//5wAAAAAH7AAAAAAAAAAAH//+AAAB//7wAAAAAP7gBAgAAAAAAAB//+AAAB///wAAAAAf/wBDAAAAAAAAA//+',
    'AAAB//jgAAAAB//4ADAAAAAAAAA//8AAAA//HgAAAAH//4DAAAAAAAAAA//8AAAAf/HAAAAAP//8BAAAAAAAAAA//gAAAAf/',
    'HAAAAAP//+AAAAAAAAAAA//AAAAAf+AAAAAAP//+AAAAAAAAAAA//AAAAAP+AAAAAAH//+AAAAAAAAAAA/+AAAAAP8AAAAAA',
    'H//+AAAAAAAAAAA/8AAAAAP4AAAAAAH8/+AAAAAAAAAAB/8AAAAAGAAAAAAAHQf8AMAAAAAAAAB/wAAAAAAAAAAAAAAAH8AP',
    'AAAAAAAAB/wAAAAAAAAAAAAAAADwAPAAAAAAAAD+AAAAAAAAAAAAAAAAA4AeAAAAAAAAD+AAAAAAAAAAAAAAAAA4A4AAAAAA',
    'AAD8AAAAAAAAAAAAAAAAAABwAAAAAAAAD8AAAAAAAAAAAAAAAAAABgAAAAAAAAD8AAAAAAAAAADAAAAAAAAAAAAAAAAADxwA',
    'AAAAAAAAAAAAAAAAAAAAAAAAAAD5gAAAAAAAAAAAAAAAAAAAAAAAAAAAB8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAAAAAAAAAAA',
    'AAAAAAAAAAAAAAAHgAAAAAAAAOAAAGIAQAAAAAAAAAAAAOAAAAAAAAD/+D/////wAAAAAAAAAAA+AAAAAEsH//+///////wA',
    'AAAAAAPAD/AAAA///////////////wAAAAPkP///AAAH///////////////wAAD///////AAAf///////////////AAD////',
    '///wAgf///////////////+AAP//////+BD4/////////////////AAB////////v/////////////////4ABAf/////////',
    '/////////////////g//////////////////////////////////////////////////////////////////////////////',
    '////////////',
))


class Artboard:
    """Translate a compact illustration program into page-space instructions."""

    def __init__(self, newspaper, origin, dimensions):
        self.display = newspaper.scene
        self.letters = newspaper.type
        self.origin = origin
        self.width, self.height = dimensions
        self.elements = 0

    def check(self, west, north, east, south):
        assert 0 <= west <= east <= self.width
        assert 0 <= north <= south <= self.height
        self.elements += 1
        assert self.elements <= 60

    def fill_polygon(self, vertices, shade):
        horizontal, vertical = zip(*vertices)
        self.check(min(horizontal), min(vertical), max(horizontal), max(vertical))
        perimeter = list(zip(vertices, vertices[1:] + vertices[:1]))
        for scan in range(device(min(vertical)), device(max(vertical))):
            ordinate = (scan + .5) / ZOOM
            crossings = []
            for (u, v), (end_u, end_v) in perimeter:
                if min(v, end_v) <= ordinate < max(v, end_v):
                    crossings.append(u + (ordinate - v) * (end_u - u) / (end_v - v))
            crossings.sort()
            assert not len(crossings) % 2
            for start, stop in zip(crossings[::2], crossings[1::2]):
                self.display.box(self.origin[0] + start, self.origin[1] + scan / ZOOM,
                                 stop - start, 1 / ZOOM, shade)

    def draw(self, *program):
        ox, oy = self.origin
        for command in program:
            opcode, *values = command
            if opcode == 'r':
                u, v, width, height, shade = values
                self.check(u, v, u + width, v + height)
                self.display.box(ox + u, oy + v, width, height, shade)
            elif opcode == 'd':
                u, v, radius, shade = values
                self.check(u - radius, v - radius, u + radius + .5, v + radius + .5)
                self.display.circle(ox + u, oy + v, radius, shade)
            elif opcode == 'p':
                vertices, shade = values
                self.fill_polygon(vertices, shade)
            elif opcode == 'l':
                vertices, shade, *custom_weight = values
                thickness = custom_weight[0] if custom_weight else 3
                horizontal, vertical = zip(*vertices)
                padding = thickness / (2 * ZOOM) + .5
                self.check(min(horizontal) - padding, min(vertical) - padding,
                           max(horizontal) + padding, max(vertical) + padding)
                translated = [(ox + u, oy + v) for u, v in vertices]
                for begin, end in zip(translated[:-1], translated[1:]):
                    self.display.segment(begin, end, shade, thickness)
            elif opcode == 't':
                words, u, v, width, size, shade, *settings = values
                options = settings[0] if settings else {}
                self.letters.put(words, ox + u, oy + v, width, size, shade,
                                 spacing=0, align='center', **options)
            else:
                raise ValueError(opcode)


def portrait_program(board):
    ivory, bullion, vermilion = (252, 242, 221), (242, 185, 79), (219, 70, 53)
    board.draw(('r', 0, 0, board.width, board.height, (39, 36, 44)),
               ('r', 12, 12, board.width - 24, 112, (66, 54, 60)))
    board.draw(*(('r', 16, scan, board.width - 32, 1, (103, 77, 73))
                 for scan in [16, 20, 102]))
    people = [
        dict(center=56, name='TRUMP', coat=COLORS['blue'], aura=(81, 109, 157),
             skin=(242, 177, 136), hair=bullion),
        dict(center=154, name='XI', coat=vermilion, aura=(164, 65, 51),
             skin=(232, 167, 119), hair=(40, 32, 32)),
        dict(center=252, name='PUTIN', coat=COLORS['blue'], aura=(92, 118, 159),
             skin=(235, 188, 158), hair=(180, 156, 133)),
    ]
    for person in people:
        middle = person['center']

        def silhouette(points, shade):
            return 'p', tuple((middle + u, v) for u, v in points), shade

        skin, coat = person['skin'], person['coat']
        is_xi = person['name'] == 'XI'
        board.draw(
            ('d', middle, 57, 41, person['aura']),
            ('r', middle - 7, 67, 14, 17, skin),
            silhouette([(-40, 109), (-35, 88), (-10, 77), (10, 77), (35, 88), (40, 109)], coat),
            ('r', middle - 14, 34, 28, 26, skin),
            ('d', middle, 58, 13.5, skin),
            silhouette([(-14, 44), (-16, 35), (-7, 27), (11, 26), (16, 32),
                        (13, 42), (9, 35), (-8, 37)], person['hair']),
            ('r', middle - 8, 50, 3, 2, 'ink'),
            ('r', middle + 5, 50, 3, 2, 'ink'),
            ('l', [(middle, 51), (middle - 2, 57), (middle + 1, 57)], (158, 96, 73), 2),
            ('r', middle - 4, 62, 8, 1, (138, 79, 59)),
            silhouette([(-11, 77), (11, 77), (0, 98)], bullion if is_xi else ivory),
            silhouette([(0, 82), (3, 89), (0, 104), (-3, 89)], bullion if is_xi else vermilion),
        )
        seam_color = tuple(component * 3 // 4 for component in coat)
        for direction in [-1, 1]:
            board.draw(('l', [(middle + direction * 15, 82), (middle + direction * 19, 89),
                               (middle + direction * 8, 102)], seam_color))
        if person['name'] == 'TRUMP':
            board.draw(*(('r', middle - 28, scan, 11, 2, shade)
                         for scan, shade in zip([92, 95, 98], [vermilion, ivory, vermilion])))
        elif is_xi:
            board.draw(silhouette([(-23, 87), (-21, 91), (-17, 92), (-21, 95),
                                   (-23, 99), (-25, 95), (-29, 92), (-25, 91)], bullion))
        else:
            board.draw(*(('r', middle - 28, scan, 11, 3, shade)
                         for scan, shade in zip([91, 94, 97], [ivory, (82, 136, 207), vermilion])))
        board.draw(('r', middle - 37, 108, 74, 18, ivory),
                   ('t', person['name'], middle - 37, 112, 74, 8.5, 'ink'))


def casualty_program(board):
    board.draw(('r', 0, 0, board.width, board.height, (43, 39, 39)),
               ('r', 0, 0, 5, board.height, 'red'),
               ('t', 'OVERNIGHT ATTACK · UKRAINE', 12, 12, board.width - 24, 8, 'paper'),
               ('t', '8', 14, 33, 86, 62, 'paper', dict(face='narrow', thickness=7)))
    for slot in range(8):
        column, row = slot % 4, slot // 4
        horizontal, vertical = 132 + column * 39, 43 + row * 37
        board.draw(('d', horizontal, vertical, 5, (211, 182, 158)),
                   ('r', horizontal - 7, vertical + 8, 14, 15, (173, 114, 105)))
    board.draw(('r', 15, 111, board.width - 30, 1, (140, 106, 99)),
               ('t', 'KILLED IN UKRAINE', 15, 120, board.width - 30, 9, 'paper'))


def equities_program(board):
    board.draw(('r', 0, 0, board.width, board.height, (41, 49, 53)),
               ('r', 0, 0, 5, board.height, 'red'),
               ('t', 'GLOBAL EQUITIES · VALUE WIPED OUT', 12, 12, board.width - 24, 8, 'paper'),
               ('t', '$9tn', 12, 34, 144, 43, 'paper', dict(face='narrow', thickness=6)))
    board.draw(*(('l', [(169, scan), (289, scan)], (78, 86, 88), 2)
                 for scan in [42, 65, 88]))
    board.draw(('l', [(177, 36), (177, 51), (278, 92)], (225, 138, 118), 6),
               ('p', [(263, 91), (283, 97), (278, 77)], (225, 138, 118)),
               ('r', 15, 111, board.width - 30, 1, (105, 116, 119)),
               ('t', 'VIX 30 · AI FEARS HIT STOCKS', 15, 120, board.width - 30, 9, 'paper'))


def pictogram(board, subject, shade):
    """Each symbol is a short data program in the same illustration ISA."""
    board.draw(('r', 0, 0, 49, 49, (232, 223, 205)))
    symbols = {
        'bridge': [
            ('r', 6, 28, 37, 4, shade),
            ('r', 13, 14, 3, 23, shade), ('r', 33, 14, 3, 23, shade),
            ('l', [(7, 25), (14, 15), (24, 25), (34, 15), (42, 25)], shade, 4),
            ('l', [(8, 40), (41, 40)], shade, 2),
        ],
        'missile': [
            ('p', [(12, 30), (30, 12), (40, 9), (37, 19), (19, 37), (13, 36)], shade),
            ('p', [(14, 26), (10, 24), (17, 17), (23, 17), (31, 25),
                   (31, 31), (24, 38), (22, 33)], shade),
            ('l', [(9, 39), (14, 34)], 'amber', 4),
        ],
        'chart': [
            ('l', [(9, 10), (9, 39), (41, 39)], shade),
            ('l', [(13, 15), (22, 22), (27, 19), (39, 32)], shade, 5),
            ('p', [(32, 32), (40, 25), (40, 34)], shade),
        ],
        'court': [
            ('p', [(7, 18), (24, 8), (42, 18)], shade),
            ('r', 8, 20, 33, 3, shade),
            *(('r', pillar, 25, 4, 13, shade) for pillar in [12, 22, 32]),
            ('r', 8, 40, 33, 3, shade),
        ],
        'fist': [
            ('p', [(16, 37), (16, 29), (10, 23), (10, 18), (14, 16),
                   (18, 21), (18, 13), (35, 13), (38, 18), (38, 26),
                   (32, 33), (32, 37)], shade),
            *(('r', u, v, 4, 11, shade) for u, v in [(18, 10), (23, 8), (28, 9), (33, 11)]),
            ('l', [(14, 20), (23, 24), (29, 22)], 'paper', 3),
            ('r', 16, 39, 16, 3, shade),
        ],
    }
    board.draw(*symbols[subject])


class Newspaper:
    """Compile the edition's sections in their required compositing order."""

    def __init__(self):
        self.scene = DisplayList()
        self.type = Typesetter(self.scene)

    def section(self, name, summary, top):
        self.scene.box(MARGIN, top, 4, 12, 'red')
        self.type.put(name, MARGIN + 11, top, 389, 10.5, 'red', thickness=3, spacing=.92)
        length = self.type.extent(summary, 8.5, 'tag', .75)
        self.type.put(summary, MARGIN + LIVE_WIDTH - length - 2, top + 1,
                      length + 2, 8.5, spacing=.75)

    def nameplate(self):
        t, s = self.type, self.scene
        story_total = len(records(LEADS)) + len(records(CITY_COPY)) + len(records(BRIEF_COPY))
        banner = f'THE WORLD IN ONE DAY · {story_total} STORIES · ACROSS THE GLOBE'
        t.put(banner, MARGIN, 23, 783, 10, 'red', spacing=.7)
        t.put('WORLD EDITION', 872, 23, 124, 10, spacing=.7)
        t.put('FRIDAY 20 NOVEMBER 2026', MARGIN, 51, LIVE_WIDTH, 44, 'ink',
              thickness=9, face='mast', spacing=1.5, align='center')
        for top, height in [(128, 4), (136, 1)]:
            s.box(MARGIN, top, LIVE_WIDTH, height, 'red')
        metrics = records('''3|PEACE DECLARATION
8|KILLED IN UKRAINE
$9tn|MARKET ROUT
$93.5bn|ANTHROPIC IPO
51-48|IRAN WAR POWERS
2.6%|TOKYO INFLATION
10,000|ROHINGYA RESETTLED''')
        cell_width = LIVE_WIDTH / len(metrics)
        for position, (figure, caption) in enumerate(metrics):
            left = MARGIN + position * cell_width
            if position != 0:
                s.box(left, 145, .5, 49, 'rule')
            t.put(figure, left + 4, 147, cell_width - 8, 27,
                  'blue' if position % 2 else 'red', thickness=5,
                  face='narrow', spacing=0, align='center')
            t.put(caption, left + 4, 187, cell_width - 8, 8, spacing=.4, align='center')
        s.box(MARGIN, 202, LIVE_WIDTH, 2, 'red')

    def front_page(self):
        self.section('THE FRONT PAGE', 'DIPLOMACY · CONFLICT · MARKETS', 214)
        for divider in [1, 2]:
            self.scene.box(MARGIN + divider * 330 - 11 - .5, 229, 1, 275, 'rule')
        artwork = [portrait_program, casualty_program, equities_program]
        for slot, fields in enumerate(records(LEADS)):
            heading, dateline, title, description, source = fields
            left = MARGIN + slot * 330
            artwork[slot](Artboard(self, (left, 229), (LEAD_WIDTH, 138)))
            first_copy = len(self.scene.copy_bounds)
            self.type.put(heading, left, 373, LEAD_WIDTH, 10, 'red', thickness=3, spacing=.7)
            self.type.put(dateline, left, 387, LEAD_WIDTH, 7.3, spacing=.25)
            title_rows = title.split('/')
            for row, words in enumerate(title_rows):
                self.type.put(words, left, 399 + row * 28, LEAD_WIDTH, 18, 'grey',
                              thickness=4, face='hero', spacing=.15)
            body_rows = self.type.paragraphs(description, 8, LEAD_WIDTH - 3, 'body')
            assert len(body_rows) == 2
            for row, words in enumerate(body_rows):
                self.type.put(words, left, 457 + row * 14, LEAD_WIDTH, 8,
                              face='body', spacing=0)
            self.type.credit(source, left, LEAD_WIDTH, 510)
            placed = self.scene.copy_bounds[first_copy:]
            for previous, following in zip(placed[:-1], placed[1:]):
                assert device(following[1][1] - previous[1][3]) >= 2
            self.scene.stories.append(title_rows[0])

    def city_reports(self):
        self.scene.box(MARGIN, 510, LIVE_WIDTH, 3, 'red')
        self.section('AROUND THE WORLD', 'EIGHT STORIES · CITY DISPATCHES', 523)
        for ordinal, fields in enumerate(records(CITY_COPY)):
            desk, city, symbol, title, description, source = fields
            row, column = divmod(ordinal, 4)
            left = device(MARGIN + column * (226 + 64 / 3)) / ZOOM
            top = 544 + row * 119
            shade = DESKS[desk][1]
            first = len(self.scene.copy_bounds)
            self.scene.box(left, top, 226, 2, 'red')
            self.scene.box(left, top + 9, 3, 10, shade)
            self.type.put(desk, left + 8, top + 10, 218, 6.7,
                          shade, thickness=3, spacing=.25)
            self.type.put(city, left, top + 21, 173, 7.2, spacing=.8)
            pictogram(Artboard(self, (left + 177, top + 18), (49, 49)), symbol, shade)
            headline_rows = self.type.paragraphs(title, 11.5, 164, 'narrow')
            assert 1 <= len(headline_rows) <= 3
            for line_number, words in enumerate(headline_rows):
                self.type.put(words, left, top + 31 + line_number * 18, 167, 11.5,
                              'ink', thickness=3, face='narrow', spacing=0)
            description_top = top + 31 + len(headline_rows) * 18 + 2
            for line_number, words in enumerate(self.type.paragraphs(description, 6.3, 224, 'tag')):
                self.type.put(words, left, description_top + line_number * 11,
                              226, 6.3, spacing=0)
            self.type.credit(source, left, 226, top + 118)
            for words, (west, north, east, south) in self.scene.copy_bounds[first:]:
                assert left <= west < east <= left + 226, words
                assert top <= north < south <= top + 118, words
            self.scene.stories.append(title)

    def locator(self, left, top):
        spacing = 1.45
        packed = radix.b64decode(WORLD_BITS, validate=True)
        assert len(packed) * 8 == 180 * 90
        for northing in range(0, 90, 2):
            for easting in range(0, 180, 2):
                ordinal = northing * 180 + easting
                byte_index, shift = divmod(ordinal, 8)
                if (packed[byte_index] >> (7 - shift)) & 1:
                    self.scene.circle(left + (easting + .5) * spacing,
                                      top + (northing + .5) * spacing, .55, 'land')
        clusters = {}
        for ordinal, (desk, headline) in enumerate(records(BRIEF_COPY), start=1):
            clusters.setdefault(desk, []).append(ordinal)
        anchors = {
            'ASIA': (195, 35, 220, 63), 'EUROPE': (125, 14, 150, 28),
            'RUSSIA & UKRAINE': (177, 9, 202, 23), 'MIDDLE EAST': (151, 44, 176, 58),
            'AFRICA': (124, 76, 149, 90), 'AMERICAS': (53, 48, 78, 76),
            'TECHNOLOGY & BUSINESS': (65, 24, 90, 38),
        }
        ordered = []
        for rank in range(max(len(numbers) for numbers in clusters.values())):
            for desk, numbers in clusters.items():
                if rank < len(numbers):
                    ordered.append((desk, numbers[rank], rank))
        occupied = []
        for desk, ordinal, rank in ordered[:16]:
            west, north, east, south = anchors[desk]
            column, row = rank % 2, rank // 2
            horizontal_jitter = ((ordinal * 7) % 3 - 1) / 3
            vertical_jitter = ((ordinal * 11) % 3 - 1) / 3
            px = left + west + column * (east - west) + horizontal_jitter
            py = top + north + row * (south - north) + column * 2 + vertical_jitter
            assert all(geometry.hypot(px - u, py - v) >= 12 for u, v in occupied)
            occupied.append((px, py))
            self.scene.circle(px, py, 2.5, DESKS[desk][1])
            digits = format(ordinal, '02d')
            self.type.put(digits, px + 4 + 1, py - 4 + 1, 15, 6.7,
                          'paper', thickness=5, spacing=0)
            self.scene.copy_bounds.pop()
            self.type.put(digits, px + 4, py - 4, 15, 6.7,
                          'ink', thickness=3, spacing=0)
        self.scene.pin_count = len(occupied)

    def briefs(self):
        self.scene.box(MARGIN, 787, LIVE_WIDTH, 3, 'red')
        self.section('WHERE IT HAPPENED', '20 BRIEFS · MAP PINS MATCH REGION CODES', 800)
        self.locator(MARGIN, 827)
        self.type.put('REGION CENTROIDS · NATURAL EARTH 1:110M', MARGIN, 959,
                      260, 6, spacing=.15)
        news = records(BRIEF_COPY)
        for column, left in enumerate([307, 654]):
            self.scene.box(left - 9, 827, .5, 137, 'rule')
            for row in range(10):
                ordinal = column * 10 + row
                desk, headline = news[ordinal]
                code, shade = DESKS[desk]
                top = 830 + row * 14
                self.scene.box(left, top, 2, 8, shade)
                self.type.put(format(ordinal + 1, '02d'), left + 5, top, 16, 7, spacing=0)
                self.type.put(code, left + 24, top, 17, 7, shade, thickness=3, spacing=0)
                self.type.put(headline, left + 45, top, 292 + 5 * column, 7.3,
                              'ink', spacing=0)
                self.scene.stories.append(headline)

    def colophon(self):
        self.scene.box(MARGIN, 971, LIVE_WIDTH, 2, 'red')
        self.scene.box(MARGIN, 975, LIVE_WIDTH, .5, 'rule')
        checks = 'DATE CHECK: Every story on this paper happened on or before 20 Nov 2026'
        sources = ('SOURCES: REUTERS, AP, AFP, BBC, AL JAZEERA, CNN, NBC, '
                   'TIMES OF INDIA, GUARDIAN — 2026-11-20')
        self.type.put(checks, MARGIN, 987, LIVE_WIDTH, 8.8, 'ink', face='body',
                      spacing=.22, align='center')
        self.type.put(sources, MARGIN, 1003, LIVE_WIDTH, 8, spacing=.32, align='center')

    def finish(self):
        self.nameplate()
        self.front_page()
        self.city_reports()
        self.briefs()
        self.colophon()
        assert len(self.scene.stories) == len(set(self.scene.stories)) == 31
        assert self.scene.pin_count == 16
        assert len(self.scene.copy_bounds) == 188
        for index, (words, bounds) in enumerate(self.scene.copy_bounds):
            for other_words, other_bounds in self.scene.copy_bounds[index + 1:]:
                shared_width = min(bounds[2], other_bounds[2]) - max(bounds[0], other_bounds[0])
                shared_height = min(bounds[3], other_bounds[3]) - max(bounds[1], other_bounds[1])
                assert shared_width <= 0 or shared_height <= 0, (words, other_words)
        return self.scene


def build_edition():
    return Newspaper().finish()


def run_press():
    edition = build_edition()
    machine = RasterPress()
    machine.paint(edition.operations)
    image_bytes = machine.encode()
    assert len(image_bytes) <= 1 << 20
    directory = filesystem.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    filesystem.makedirs(directory, exist_ok=True)
    destination = filesystem.path.join(directory, 'entry.png')
    with open(destination, 'wb') as stream:
        stream.write(image_bytes)
    with open(__file__, encoding='utf-8') as source_stream:
        authored_lines = sum(1 for source_line in source_stream)
    print(reporting.dumps(dict(output=destination, bytes=len(image_bytes),
          sha256=digests.sha256(image_bytes).hexdigest(), lines=authored_lines,
          stories=len(edition.stories), map_pins=edition.pin_count,
          cards=len(records(CITY_COPY)), ticker_items=len(records(BRIEF_COPY)),
          text_bounds_checked=len(edition.copy_bounds), width=RESOLUTION,
          height=RESOLUTION), sort_keys=True))


if __name__ == "__main__":
    run_press()
