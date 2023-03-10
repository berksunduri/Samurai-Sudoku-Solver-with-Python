import multiprocessing
import os
import threading

from dogrumu import dogrumu
import time


def cartesianProd(A, B, c=''):
    # cartesian dondur
    return [a + b + c for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits

id_var = 'a'  # sol ust
box_a = cartesianProd(rows, cols, id_var)
unit_a = ([cartesianProd(rows, c, id_var) for c in cols] +
          [cartesianProd(r, cols, id_var) for r in rows] +
          [cartesianProd(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
           for cs in ('123', '456', '789')])

id_var = 'b'  # sag ust
box_b = cartesianProd(rows, cols, id_var)
unit_b = ([cartesianProd(rows, c, id_var) for c in cols] +
          [cartesianProd(r, cols, id_var) for r in rows] +
          [cartesianProd(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
           for cs in ('123', '456', '789')])

id_var = 'c'  # sol alt
box_c = cartesianProd(rows, cols, id_var)
unit_c = ([cartesianProd(rows, c, id_var) for c in cols] +
          [cartesianProd(r, cols, id_var) for r in rows] +
          [cartesianProd(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
           for cs in ('123', '456', '789')])

id_var = 'd'  # sag alt
box_d = cartesianProd(rows, cols, id_var)
unit_d = ([cartesianProd(rows, c, id_var) for c in cols] +
          [cartesianProd(r, cols, id_var) for r in rows] +
          [cartesianProd(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
           for cs in ('123', '456', '789')])


def replaceFileData(c):
    a = b = 0
    s = ""
    if c[0] in 'ABCGHI' and c[1] in '123789':  # dosyada ki sayilari dogru sekilde kodla
        if c[0] in 'ABC':  # ve replacele
            s += chr(ord(c[0]) + 6)
            a = 1
        elif c[0] in 'GHI':
            s += chr(ord(c[0]) - 6)
            a = 2
        if c[1] in '123':
            s += chr(ord(c[1]) + 6)
            b = 1
        elif c[1] in '789':
            s += chr(ord(c[1]) - 6)
            b = 2
    else:
        return c
    if a == 1 and b == 1:
        s += 'a'
    elif a == 1 and b == 2:
        s += 'b'
    elif a == 2 and b == 1:
        s += 'c'
    elif a == 2 and b == 2:
        s += 'd'
    return s


id_var = '+'
box_mid = [replaceFileData(x) for x in cartesianProd(rows, cols, id_var)]  # ortada ki sudoku icin ayri islem
unit_mid = ([box_mid[x * 9:x * 9 + 9] for x in range(0, 9)] +  # anca diger kutulari tam olarak tanimlayabildigimizde
            [box_mid[x::9] for x in range(0, 9)] +  # bu islemi yapabiliyoruz
            [cartesianProd(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
             for cs in ('123', '456', '789')
             if not (rs in 'ABCGHI' and cs in '123789')])

box_all = set(box_a + box_b + box_c + box_d + box_mid)
unit_all = unit_a + unit_b + unit_c + unit_d + unit_mid

units = dict((s, [u for u in unit_all if s in u])
             for s in box_all)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in box_all)


# grid parsing

def parseGrid(grid):
    # baslangic icin herhangi bir kutucuk herhangi bir rakam olabilir
    values = dict((s, digits) for s in box_all)
    for s, d in gridValues(grid).items():
        if d in digits and not assign(values, s, d):
            return False  # eger d yi s kutusuna atamazsak
    return values


def flatten(arr):
    return [x for sub in arr for x in sub]


def gridValues(grid):
    a = flatten([x[:9] for x in grid[:9]])
    b = flatten([x[12:] for x in grid[:9]])
    c = flatten([x[:9] for x in grid[12:]])
    d = flatten([x[12:] for x in grid[12:]])
    mid = flatten([x[6:15] for x in grid[6:15]])
    chars = a + b + c + d + mid
    boxes = box_a + box_b + box_c + box_d + box_mid
    # assert len(chars) == 405
    return dict(zip(boxes, chars))


# kisitlamalar

def assign(values, s, d):
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    if d not in values[s]:
        # zaten elimine edilmis sonra ki sayiya gec
        return values
    values[s] = values[s].replace(d, '')  # boslukla replace et
    if len(values[s]) == 0:
        return False  # yanlis tekrarla
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False  # yanlis tekrarla
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  # yanlis tekrarla
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False  # yanlis tekrarla
    return values  # elimine edildi sonra ki sayiya gec


# Konsola yazdirma

def display(values, sqr):
    width = 1 + max(len(values[s]) for s in sqr)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(
            values[sqr[(ord(r) - 65) * 9 + int(c) - 1]].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    print()


def displaySamurai(vals):
    # Sudokuyu konsolda solustten baslayarak dogru sekilde yazdirma
    # a=solUst,b=sagUst,c=solAlt,d=sagAlt,mid=orta
    print(vals)
    if not vals:
        print("Cozum yok")
        return
    print("Sol Ust:")
    display(vals, box_a)
    print("Sag Ust:")
    display(vals, box_b)
    print("Sol Alt:")
    display(vals, box_c)
    print("Sag Alt:")
    display(vals, box_d)
    print("Orta:")
    display(vals, box_mid)
    # ayri dosyadan sudokunun dogrulugunu kontrol etmek
    dogrumu(vals, [box_a, box_b, box_c, box_d, box_mid])


# ARAMA


def solve(*grid):
    return search(parseGrid(grid))  # girdigimiz gridi aramasini kolaylastirmak icin parse
    # ornegin sol ust sudokunun ilk kutusunun degeri A1a
    # A=sira,1=sutun,a=sol ust sudoku


def search(values):#depth first search
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in box_all):
        return values
    n, s = min((len(values[s]), s) for s in box_all if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])


# herhangi bir deger dondurmesi (stackOverflow yardimi alindi)
def some(seq):
    for e in seq:
        if e:
            return e
    return False


if __name__ == '__main__':
    prompt = 1
    while prompt:
        txt = input("Sudoku dosyasini gir:")
        try:
            f = open(txt, 'r')
            prompt = 0
        except FileNotFoundError:
            print("Dosya bulunamadi ")
    samurai_grid = f.read().split('\n')
    import concurrent.futures
    workers=10

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        start_time = time.time()
        ans = executor.submit(solve, samurai_grid)
    # ans = solve(samurai_grid)

    displaySamurai(ans.result())
    print("Gecen Sure:" + str(time.time() - start_time))
