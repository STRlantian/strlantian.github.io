import json as js
'''
我宣布个事
这函数我写的
woooooo
'''

def reconvert(path: str, name: str) -> str:
    '''
    取一个比赛用的文本文件
    然后改造成适合模型读的json
    改不了题就改代码.jpg
    *文件名不要带后缀
    '''
    with open(path + name + ".txt", 'r', encoding="utf8") as file:
        raw = []
        text = []
        labels = {}
        current = ""
        state = "O"
        keyword = ""
        stateB = 0
        stateE = 0
        line = file.readline()
        while line:
            print(line)
            if not line == '\n':
                se = line.split()
                if len(se) == 1:
                    se.append(se[0])
                    se[0] = "_"
                current += se[0]
                if not se[1] == 'O':
                    state = se[1].split('-')[1]
                    state = state.lower()
                    if state == "org":
                        state == "organization"
                    elif state == "loc":
                        state == "address"
                    elif state == "per":
                        state == "name"
                    keyword += se[0]
                    stateE = len(current) - 1
                else:
                    if not state == 'O':
                        stateB = stateE - len(keyword) + 1
                        try:
                            pos = labels[state][keyword]
                            pos.append([stateB, stateE])
                        except:
                            try:
                                sl = labels[state]
                                sl.update({ keyword: [[stateB, stateE]]})
                            except:
                                labels.update({ state: { keyword: [[stateB, stateE]]}})
                        keyword = ""
                        state = 'O'
            else:
                text.append(current)
                raw.append({ "text": current, "label": labels })
                current = ""
                labels = {}
                stateB = stateE = 0
                keyword = ""
                state = 'O'
            line = file.readline()
        text.append(current)
        raw.append({ "text": current, "label": labels })
        out = ""
        for s in raw:
            out += js.dumps(s, ensure_ascii=False) + '\n'
        # return out
        try:
            with open(path + name + ".json", 'x', encoding="utf8") as file:
                for s in raw:
                    file.write(js.dumps(s, ensure_ascii=False) + '\n')
        except:
            with open(path + name + ".json", 'w', encoding="utf8") as file:
                for s in raw:
                    file.write(js.dumps(s, ensure_ascii=False) + '\n')

def recover(jsontext: list, outpath: str, outname: str) -> list:
    '''
    jsontext是json.dumps(...)之后的结果
    或者可以直接读取json文件
    返回转化后的结果
    '''
    raw = []
    out = []
    for t in jsontext:
        tc = js.loads(t)
        raw.append(tc)
    # print(raw)
    for ele in raw:
        text = ele["text"]
        tags = []
        for i in range(0, len(text)):
            tags.append('O')
        labels = ele["label"]
        labelist = ["organization", "address", "name"]
        for lb in labelist:
            try:
                groups = labels[lb]
                for locs in dict(groups).values():
                    for loc in locs:
                        for i in range(loc[0], loc[1] + 1):
                            tags[i] = "I-" + lb
                        tags[loc[0]] = "B-" + lb
            except:
                continue
        for i in range(0, len(text)):
            if text[i] == '_':
                text[i] == ' '
            out.append(text[i] + " " + tags[i] + '\n')
        out.append('\n')
    # print(out)
    '''
    try:
        with open(outpath + outname + "_rec.txt", 'x', encoding="utf8") as file:
            file.writelines(out)
    except:
        with open(outpath + outname + "_rec.txt", 'w', encoding="utf8") as file:
            file.writelines(out)
    '''
    return out

# PATH = "./out/"
# NAME = "final3"
# reconvert(PATH, NAME)
# with open(PATH + NAME + ".json", 'r', encoding="utf8") as file:
#    recover(file.readlines(), PATH, NAME)
reconvert("data/clue/", "train")
reconvert("data/clue/", "test")