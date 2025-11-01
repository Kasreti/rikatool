import re

cons_b = 'mnbtdkgqTzcjsɕʑfvθðxɣhywʕlrʔɹʷʲ'
son_b = 'yu'
stv = 'áéíóúâôî'
vowels = 'aeiouæïöäyʷʲ' + stv
validph = vowels + cons_b + "." + stv
dia_b = {
        "ts": "T",
        "th": "θ",
        "dh": "ð",
        "sy": "ɕ",
        "zy": "ʑ",
        "gh": "ɣ",
        "rh": "ʕ",
        "ty": "c",
        "dy": "j",
        "kh": "x",
        "ae": "æ",
        "aa": "ä"
    }
stv_pair = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "â": "a",
    "ô": "ö",
    "î": "ï"
}
ipa_f = {
    "b": "p",
    "t": "tʰ",
    "T": "tsʰ",
    "c": "tɕʰ",
    "d": "t",
    "j": "dʑ",
    "z": "dz",
    "k": "kʰ",
    "y": "j",
    "xä": "χä",
    "xo": "χo",
    "ï": "y",
    "ie": "ʲɛ",
    "ia": "ʲa",
    "e": "ɛ",
    "ö": "ɵ",
    "o": "ɔ",
    "ä": "ɑ",
    "g": "k",
    "ʔʲ": "j",
    "ʔʷ": "w"
}
ipa_c = {
    "n.k": "ŋ.g",
    "ʷi": "ɨi",
    "ɛi": "eː",
    "ai": "eː",
    "ɔu": "oː",
    "an": "ɑ̃(n)",
    "eːn": "ẽ(n)",
    "ɔn": "ɔ̃(n)",
    "un": "ʊ̃(n)",
    "aŋ": "ɑ̃(ŋ)",
    "eːŋ": "ẽ(ŋ)",
    "ɔŋ": "ɔ̃(ŋ)",
    "uŋ": "ʊ̃(ŋ)",
    "au": "ʌw",
    "l.": "ɹ.",
    "kʰɪ.ˈ": "kʰɪ̥.ˈ",
    "kʰʊ̥.ˈ": "kʰɯ̥.ˈ",
    "adz": "az",
    "ar": "ɑː",
    "ær": "ɑː",
    "ɑr": "ɑː",
    "ir": "yː",
    "yr": "yː",
    "ur": "yː",
    "ɛr": "ɵː",
    "ɵr": "ɵː",
    "ɔr": "ɵː"
}
ipa_e = {
    "y": "u",
    "q": "k",
    "tsʰ": "s",
    "dz": "z",
    "ɵ": "ɚ",
    "æ": "ɛ",
    "r": "ɹ",
    "tʰ": "T",
    "kʰ": "K",
    "t": "d",
    "k": "g",
    "T": "t",
    "K": "k",
    "ɣ": "g",
    "ʕ": "h",
    "ɕ": "ʃ",
    "ʑ": "ʒ"
}


dtitles = ["Ää","Ææ","Bb","Cc","Dd","DHdh","Ee","Ff","Gg","GHgh","Hh","Ii","Ïï","Jj","Kk","Ll","Mm","Nn","Oo","Öö","Qq","Rr","Ss","SYsy","Tt","THth","TSts","Uu","Vv","Ww","Xx","Yy","Zz","ZYzy","RHrh"]

def ipa(x):
    x = x.lower()
    x = x.replace("-","")
    for dia, mon in dia_b.items():
        x = x.replace(dia, mon)
    if (x[0] in vowels) is True:
        x = "ʔ" + x
    x = sylla(x)
    x = stress(x)
    for pref, fin in ipa_f.items():
        x = x.replace(pref, fin)
    return x

def sylla(x):
    if (x[0] in cons_b) and (x[1] in son_b):
        if x[1] == "y":
            x = x[:1] + "ʲ" + x[2:]
        elif x[1] == "u":
            x = x[:1] + "ʷ" + x[2:]
    i = 1
    x = x + " "
    xlen = len(x)
    while i<=xlen-1:
        # print(i)
        # print (" checking " + x[i])
        if (x[i] in vowels) and (x[i+1] in cons_b):
             if (x[i+2] in cons_b) and ((x[i+2] in son_b) is False):
                 x = x[:i+2] + "." + x[i+2:]
                 i+=1
                 # print("1: " + x)
             elif (x[i+2] in cons_b) and (x[i+2] in son_b):
                 if x[i+2] == "y":
                     x = x[:i+2] + "ʲ" + x[i+3:]
                 elif x[i+2] == "u":
                     x = x[:i+2] + "ʷ" + x[i+3:]
                 x = x[:i+1] + "." + x[i+1:]
                 i+=1
                 # print("2: " + x)
             else:
                 x = x[:i+1] + "." + x[i+1:]
                 i+=1
                 # print("3: " + x)
        elif (x[i] in validph) is False:
            # print("bro ts invalid")
            break
        i += 1
        # print(i)
    return x[:-1]

def stress(x):
    sty = re.split("\\.", x)
    i = 0
    fin = 0
    dipt = -1
    found = ""
    while i<len(sty):
        dipcheck = sty[i]
        for cons in cons_b:
            dipcheck = dipcheck.replace(cons, '')
        if len(dipcheck) > 1:
                dipt = i
        for j in sty[i]:
            if (j in stv) is True:
                sty[i] = "ˈ" + sty[i]
                for stvo, ustv in stv_pair.items():
                    sty[i] = sty[i].replace(stvo, ustv)
                    if ustv in sty[i]:
                        found = ustv
                        fin = i
                break
        i += 1
    if found != "":
        copys = sty[fin-1]
        for cons in cons_b:
            copys = copys.replace(cons,'')
        # diphthong check
        if len(copys) > 1:
            return ".".join(sty)
        # monophthong check
        else:
            if copys == "e":
                if found in 'eiï':
                    sty[fin-1] = sty[fin-1].replace("e", "ɪ")
                else:
                    sty[fin-1] = sty[fin-1].replace("e", "ɐ")
            else:
                sty[fin-1] = sty[fin-1].replace("a", "ɐ")
                sty[fin-1] = sty[fin-1].replace("i", "ɪ")
                sty[fin-1] = sty[fin-1].replace("o", "ʊ")
                sty[fin-1] = sty[fin-1].replace("u", "ʊ")
            return ".".join(sty)
    else:
        if dipt != -1:
            # print("def: dipth")
            sty[dipt] = "ˈ" + sty[dipt]
            return ".".join(sty)
        else:
            # print("def: penul")
            sty[len(sty)-2] = "ˈ" + sty[len(sty)-2]
            return ".".join(sty)

# MAIN
# print ('yo welcome to rikatool v1')
# print ('paste a sentence or a word')
# name = input()

def genIPA(name):
    splitname = re.split(" ",name)
    res = ""
    i=0
    while i<len(splitname):
        res = res + ipa(splitname[i]) + " "
        i += 1
    return res

def genIPA_collo(name):
    for st, co in ipa_c.items():
        name = name.replace(st, co)
    return name

def genIPA_eng(name):
    for st, co in ipa_e.items():
        name = name.replace(st, co)
    return name

with open('dict.txt', 'r', encoding='utf-8') as f:
    dict = f.read()
with open("new.txt", "w", encoding='utf-8') as f:
    dict = dict.split("Inflections\n\nAppendix A")[0]
    dict = dict.split("Aa\n")[1]
    for i in dtitles:
        dict = dict.replace("\n" + i,"")
    dict = dict.strip()
    dict = dict.replace("\n\n","\n")
    f.write(dict)

