from copy import deepcopy
'''
1 = dark Green
2 = light green
3 = yellow
4 = red
5 = light blue
6 = orange
7 = light violet
8 = dark blue
9 = firoz
10 = dark violet
11 = gray
12 = pink


'''
S = 0
Pallet = [[2,1,2,1], [3,3,4,5], [6,1,7,8], [9,6,10,6], [3,9,8,6], [11,5,12,11], [7,10,8,11],
          [9,1,5,10], [8,11,12,9], [2,10,4,7], [3,4,12,4], [7,12,2,5], [0,0,0,0], [0,0,0,0]]
default_cap = 4
# all_act = 1.select solution, 2.all posible, 3.pallet
all_acts = []

def check(pallet):
    answer = True
    for jar in pallet:
        for color in jar:
            if color != jar[0]:
                answer = False
    return answer

def capacity(jar):
    cap = 0
    for cell in jar:
        if cell == 0:
            cap += 1
    return cap

def last_color(jar):
    lc = 0
    for color in jar:
        if color != 0:
            lc = color
    return lc

def all_posible(pallet):
    posibilities = []
    for jar2_no in range(len(pallet)):
        if capacity(pallet[jar2_no]) > 0:
            for jar1_no in range(len(pallet)):
                if pallet[jar1_no] != pallet[jar2_no]:
                    if last_color(pallet[jar1_no]) != 0:
                        if last_color(pallet[jar1_no]) == last_color(pallet[jar2_no]) or last_color(pallet[jar2_no]) == 0:
                            if forward_test(jar1_no,jar2_no) not in all_pallets():
                                posibilities.append([jar1_no, jar2_no])
    return posibilities

def first_empty(jar):
    result = 0
    for cell in jar:
        if cell != 0:
            result += 1
    return result

def road_record():
    all_acts.append([0,all_posible(Pallet),deepcopy(Pallet)])
    record_correction()

def forward_test(jar1_no:int, jar2_no:int):
    pall = deepcopy(Pallet)
    jar1_last_color = last_color(pall[jar1_no])
    jar1_lasted_used = first_empty(pall[jar1_no])-1
    jar2_first_empty = first_empty(pall[jar2_no])
    pall[jar2_no][jar2_first_empty] = jar1_last_color
    pall[jar1_no][jar1_lasted_used] = 0
    return pall


def record_correction():
    if len(all_acts) > 1:
        key = all_acts[-2][1][0]
        key_p = [key[1],key[0]]
        for i in range(len(all_acts[-1][1])):
            if all_acts[-1][1][i] == key_p:
                all_acts[-1][1].pop(i)
                break

def log(status:str):
    global S
    S += 1
    last_act = all_acts[-1]
    Log = ''
    Log += f'    <step{S}>\n'
    Log += f'        <act>{status}</act>\n'
    Log += f'        <opt>{last_act[0]}</opt>\n'
    Log += f'        <alt>{last_act[1]}</alt>\n'
    Log += f'        <pal>{last_act[2]}</pal>\n'
    Log += f'    </step{S}>\n'
    with open('log.xml', 'a') as file:
        print(Log, file=file)

def log_start():
    Log = '<log>'
    with open('log.xml', 'w') as file:
        print(Log, file=file)   

def log_finish():
    Log = '</log>'
    with open('log.xml', 'a') as file:
        print(Log, file=file)      

def all_pallets():
    result = []
    for i in all_acts:
        result.append(deepcopy(i[2]))
    return result

def forward():
    act = all_acts[-1][1][all_acts[-1][0]]
    jar1_no = act[0]
    jar2_no = act[1]
    jar1_last_color = last_color(Pallet[jar1_no])
    jar1_lasted_used = first_empty(Pallet[jar1_no])-1
    jar2_first_empty = first_empty(Pallet[jar2_no])
    Pallet[jar2_no][jar2_first_empty] = jar1_last_color
    Pallet[jar1_no][jar1_lasted_used] = 0
    road_record()
    log('fore')

def backward():
    log('back')
    all_acts.pop(-1)
    Pallet = deepcopy(all_acts[-1][2])
    all_acts[-1][0] += 1

def backward_needed():
    if all_acts[-1][0] >= len(all_acts[-1][1]) or len(all_acts[-1][1]) == 0:
        return True
    else:
        return False

def Results():
    res = []
    for i in all_acts:
        res.append(i[1][0])
    return res


def run():
    road_record()
    while not check(Pallet):
        if backward_needed():
            backward()
        else:
            for j in all_acts:
                print(f'r_no:{j[0]}')
                print(f'pos:{j[1]}')
                print(f'pall:{j[2]}')
            forward()
            print('-----------------------------------------------')
    print(Results())
log_start()
run()
log_finish()