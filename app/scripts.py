import re
from app import app, db
from app.models import Dictionary
from sqlalchemy import func, desc
import sqlalchemy as sa
import sqlalchemy.orm as so

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
    "aa": "ä",
    "ph": "f"
}
dia_c = {
    "ty": "c",
    "dy": "j",
    "aye": "ae",
    "uo": "ou"
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
    "ʔʷ": "w",
    "ʰ.": "."
}
ipa_c = {
    "n.k": "ŋ.k",
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
    "ʰɪ": "ʰɪ̥",
    "ʰʊ": "ʰɯ̥",
    "ʰi": "ʰi̥",
    "ʰu": "ʰɯ̥",
    "adz": "az",
    "ɕr": "ʂ",
    "ʑr": "ʐ",
    "ɕ.r": ".ʂ",
    "ʑ.r": ".ʐ",
    "ɕ.ˈr": ".ˈʂ",
    "ʑ.ˈr": ".ˈʐ"
}
ipa_c2 = {
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
    "ʑ": "ʒ",
    "dʃ": "tʃ",
    "ʲ": "j",
    "ʷ": "w",
    "au": "aʊ",
    "ai": "aɪ",
    "ei": "eɪ",
    "ɵ": "ɚ",
    "uɹ": "ɚ",
    "ʰ": "",
    "ʔ": "",
    "g.": "k.",
    "d.": "t.",
    "ɐ": "a",
    "x": "h",
    "p": "b",
}
stc_pair = {
    "t": "D",
    "k": "G",
    "T": "Z",
    "c": "Q",
    "ɕ": "C",
    "x": "H",
    "f": "V",
    "θ": "R",
    "d": "t",
    "g": "k",
    "z": "ts",
    "j": "c",
    "ʑ": "ɕ",
    "v": "f",
    "ɣ": "x",
    "ð": "th",
    "D": "d",
    "G": "g",
    "Z": "z",
    "Q": "j",
    "C": "zy",
    "H": "gh",
    "V": "v",
    "R": "dh"
}

dtitles = ["Ää","Ææ","Bb","Cc","Dd","DHdh","Ee","Ff","Gg","GHgh","Hh","Ii","Ïï","Jj","Kk","Ll","Mm","Nn","Oo","Öö","Qq","Rr","Ss","SYsy","Tt","THth","TSts","Uu","Vv","Ww","Xx","Yy","Zz","ZYzy","RHrh"]
inflist = ["syet", "sye", "sran", "sro", "da", "de", "ran", "ro", "den", "do", "sui", "kos", "syan", "sin", "git", "jai", "ja", "lï", "in","ket","kiec","lï", "un", "ki", "kei", "tua", "en", "yaz", "i", "n", "rande", "srande", "dende", "syetende", "syetenda", "nde", "nda"]
inf2list = ["ri", "fïn", "uaz", "yari", "yaki", "ru", "gan", "äri", "äki", "waz", "waki", "wari", "unaz"]
infilist = ["i", "wi", "u", "winu", "yá", "wayá", "e", "wiye", "im", "wim", "yu", "i", "ui", "yo", "ou", "yá", "uyá", "e", "ue", "im", "uim", "yu"]
infylist = ["ï", "iyï", "ir", "irhï", "á", "iyá", "e", "iye", "ïm", "iyïm", "yiyï","yï", "yiyï", "ï", "iyï", "yá", "iyá", "ye", "iye", "yïm", "iyïm", "yiyï"]
infyelist = ["yé", "yué", "eyó", "ueyó", "yaná", "yuená", "ya", "yua", "yém", "yuém", "yun"]
infelist = ["é", "ué", "ó", "uó", "ayá", "uwayá", "a", "ua", "e", "ue", "e"]

class definition:
    def __init__(self, word, ipa, ipa_c, ipa_e, defin, anim, pos, etym, root, inf, alt, neg, redup, ref):
        self.word = word
        self.ipa = ipa
        self.ipa_c = ipa_c
        self.ipa_e = ipa_e
        self.defin = defin
        self.anim = anim
        self.pos = pos
        self.etym = etym
        self.root = root
        self.inf = inf
        self.alt = alt
        self.neg = neg
        self.redup = redup
        self.ref = ref

    def __repr__(self):
        return '{} ({}) {} with definition {}'.format(self.pos, self.anim, self.word, self.defin)


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
        elif x[1] == "u" and (x[2] in vowels):
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
    if (x[len(x) - 3] == '.') and (x[len(x)-2] in cons_b):
        return x[:len(x)-3] + x[len(x)-2]
    else:
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

def genIPA(name):
    splitname = re.split(" ",name)
    res = ""
    i=0
    while i<len(splitname):
        res = res + ipa(splitname[i])
        i += 1
        if i<len(splitname):
            res = res + " "
    return res

def genIPA_collo(name):
    for st, co in ipa_c.items():
        name = name.replace(st, co)
    for st, co in ipa_c2.items():
        if name.endswith(st):
            name = name.replace(st,co)
    return name

def genIPA_eng(name):
    for st, co in ipa_e.items():
        name = name.replace(st, co)
    return name

def refreshDict():
    print("importing dictionary...")
    Dictionary.query.delete()
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
    with open("new.txt", "r", encoding='utf-8') as f:
        ndict = [line.strip() for line in f]
        for x in ndict:
            if x != "" and "inflections: " not in x:
                x = x.split(" // ")
                tx = x[0].split(" ")
                if(tx[len(tx)-1] == "i.") or (tx[len(tx)-1] == "ii.") or (tx[len(tx)-1] == "iii."):
                    word = tx[:len(tx)-2]
                    pos = tx[len(tx)-2]
                    anim = tx[len(tx)-1]
                    nw = ""
                    for j in word:
                        nw += j + " "
                        print(nw)
                        currentword = Dictionary(nw.strip(), x[1], anim, pos, "")
                else:
                    word = tx[:len(tx)-1]
                    pos = tx[len(tx)-1]
                    nw = ""
                    for j in word:
                        nw += j + " "
                        print(nw)
                        currentword = Dictionary(nw.strip(), x[1], "", pos, "")
                db.session.add(currentword)
        print("Dictionary imported successfully!")
        db.session.commit()

def posword(x):
    match x:
        case "n.":
            return "Noun"
        case "v.":
            return "Verb"
        case "stv.":
            return "Stative verb"
        case "intj.":
            return "Interjection"
        case "conj.":
            return "Conjunction"
        case "phr.":
            return "Phrase"
        case "aff.":
            return "Affix"
        case "part.":
            return "Particle"
        case _:
            return "Unimplemented"

def getInf(x):
    if x.pos == "n.":
        match x.anim:
            case "i.":
                if x.word[0] in vowels:
                    return ["in","ket","kiec","lï","s'"]
                else:
                    return ["in", "ket", "kiec", "lï", "sa "]
            case "ii.":
                return ["un", "ki", "kei", "tua", "sa "]
            case _:
                if x.word[0] in vowels:
                    if x.word[len(x.word) - 1] == "i":
                        return ["n", "ja", "jai", "ni", "s'"]
                    elif x.word[len(x.word) - 1] in vowels:
                        return ["n", "ja", "jai", "i", "s'"]
                    else:
                        return ["en", "ja", "jai", "i", "s'"]
                else:
                    if x.word[len(x.word)-1] == "i":
                        return ["n", "ja", "jai", "ni", "sa "]
                    elif x.word[len(x.word)-1] in vowels:
                        return ["n", "ja", "jai", "i", "sa "]
                    else:
                        return ["en", "ja", "jai", "i", "sa "]
    elif x.pos == "v." or "stv.":
        unsroot = x.word
        for uns, st in stv_pair.items():
            unsroot = unsroot.replace(uns,st)
        match x.word[len(x.word)-1]:
            case "i":
                if x.word[len(x.word) - 2] in vowels:
                    v = x.word[len(x.word)-2]
                    list = ["i", "wi", "u", "winu", "yá", "wayá", "e", "wiye", "im", "wim", "yu"]
                    list2 = ["uw"+v+"i","un"+v+"u","uw"+v+"yá","un"+v+"ye","uw"+v+"im"]
                    for i in range(len(list)):
                        if i == 4 or i == 5:
                            list[i] = unsroot[:len(unsroot) - 1] + list[i]
                            if i == 5:
                                list[i] = list[i] + "/" + unsroot[:len(unsroot) - 2] + list2[int(i / 2)]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                        else:
                            list[i] = x.word[:len(x.word) - 1] + list[i]
                            if i%2==1:
                                list[i] = list[i] + "/" + x.word[:len(x.word) - 2]+list2[int(i/2)]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                    list.append("ri")
                    list.append("fïn")
                    list.append("waz")
                    list.append("yari")
                    list.append("yaki")
                else:
                    list = ["i", "ui", "yo", "ou", "yá", "uyá", "e", "ue", "im", "uim", "yu"]
                    for i in range(len(list)):
                        if i == 4 or i == 5:
                            list[i] = unsroot[:len(unsroot) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                        else:
                            list[i] = x.word[:len(x.word) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                    list.append("ri")
                    list.append("fïn")
                    list.append("uaz")
                    list.append("yari")
                    list.append("yaki")
                return list
            case "ï":
                if x.word[len(x.word)-2] == "y":
                    list = ["yï", "yiyï", "ï", "iyï", "yá", "iyá", "ye", "iye", "yïm", "iyïm", "yiyï"]
                    for i in range(len(list)):
                        if i == 4 or i == 5:
                            list[i] = unsroot[:len(unsroot) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                        else:
                            list[i] = x.word[:len(x.word) - 2] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                    list.append("ri")
                    list.append("fïn")
                    list.append("uaz")
                    list.append("wari")
                    list.append("waki")
                    return list
                else:
                    list = ["ï", "iyï", "ir", "irhï", "á", "iyá", "e", "iye", "ïm", "iyïm", "yiyï"]
                    for i in range(len(list)):
                        if i == 4 or i == 5:
                            list[i] = unsroot[:len(unsroot) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                        else:
                            list[i] = x.word[:len(x.word) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                    list.append("ri")
                    list.append("fïn")
                    list.append("uaz")
                    list.append("wari")
                    list.append("waki")
                    return list
            case "é":
                if x.word[len(x.word) - 2] == "y":
                    list = ["yé", "yué", "eyó", "ueyó", "yaná", "yuená", "ya", "yua", "yém", "yuém", "yun"]
                    for i in range(len(list)):
                        if 4 <= i <= 5:
                            list[i] = unsroot[:len(unsroot) - 2] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                        else:
                            list[i] = x.word[:len(x.word) - 2] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                    list.append("ru")
                    list.append("gan")
                    list.append("unaz")
                    list.append("érhari")
                    list.append("érhaki")
                else:
                    list = ["é", "ué", "ó", "oú", "ayá", "uwayá", "a", "ua", "e", "ue", "un"]
                    for i in range(len(list)):
                        if i == 4 or i == 5:
                            list[i] = unsroot[:len(unsroot) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                        else:
                            list[i] = x.word[:len(x.word) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                    list.append("ru")
                    list.append("gan")
                    list.append("uaz")
                    list.append("érhari")
                    list.append("érhaki")
                return list
            case "a":
                if x.word[len(x.word) - 2] == "u":
                    list = ["a", "ya", "ó", "yó", "ayá", "yaná", "a", "ya", "am", "uyam", "yun"]
                    for i in range(len(list)):
                        if i == 4 or i == 5:
                            list[i] = unsroot[:len(unsroot) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                        else:
                            list[i] = x.word[:len(x.word) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                    list.append("ru")
                    list.append("gan")
                    list.append("naz")
                    list.append("äri")
                    list.append("äki")
                if x.word[len(x.word) - 2] == "y":
                    list = ["ya", "yua", "ayó", "uayó", "yaná", "yuaná", "ya", "yua", "yam", "yuam", "yun"]
                    for i in range(len(list)):
                        if 2 <= i <= 5:
                            list[i] = unsroot[:len(unsroot) - 2] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                        else:
                            list[i] = x.word[:len(x.word) - 2] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                    list.append("ru")
                    list.append("gan")
                    list.append("unaz")
                    list.append("äri")
                    list.append("äki")
                else:
                    list = ["a", "ua", "ó", "uó", "ayá", "uwayá", "a", "ua", "am", "uam", "aun"]
                    for i in range(len(list)):
                        if i == 4 or i == 5:
                            list[i] = unsroot[:len(unsroot) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                        else:
                            list[i] = x.word[:len(x.word) - 1] + list[i]
                            for j, k in dia_c.items():
                                list[i] = list[i].replace(j, k)
                    list.append("ru")
                    list.append("gan")
                    list.append("uaz")
                    list.append("äri")
                    list.append("äki")
                return list
            case _:
                unproot = x.word.replace("c","ty")
                unproot = unproot.replace("j","dy")
                list = ["", "u", "o", "ou", "á", "uá", "e", "ue", "em", "em", "ï"]
                for i in range(len(list)):
                    if i == 2 or i == 3:
                        list[i] = unproot[:len(unproot) - 1] + list[i]
                        for j, k in dia_c.items():
                            list[i] = list[i].replace(j, k)
                    elif i == 4 or i == 5:
                        list[i] = unsroot[:len(unsroot)] + list[i]
                        for j, k in dia_c.items():
                            list[i] = list[i].replace(j, k)
                    else:
                        list[i] = x.word[:len(x.word)] + list[i]
                        for j, k in dia_c.items():
                            list[i] = list[i].replace(j, k)
                list.append("ri")
                list.append("fïn")
                list.append("uaz")
                list.append("ari")
                list.append("aki")
                return list

def redup(x):
    word = x.word
    for dia, mon in dia_b.items():
        word = word.replace(dia, mon)
    if(word[0] in cons_b) and (word[1] not in son_b):
        syl = word[:2]
        for un, vo in stc_pair.items():
            syl = syl.replace(un, vo)
        init = word[:2]
        for dia, mon in dia_b.items():
            if dia != "ph":
                word = word.replace(mon, dia)
                init = init.replace(mon, dia)
        return word.replace(word[:2],init+syl,1)
    elif (word[0] in cons_b) and (word[1] in son_b):
        syl = word[:3]
        for un, vo in stc_pair.items():
            syl = syl.replace(un, vo)
        init = word[:3]
        for dia, mon in dia_b.items():
            init = init.replace(mon, dia)
        return word.replace(word[:3], init + syl, 1)
    else:
        return word[0] + "n" + word

def removeInf(x):
    if x.startswith("s'"):
        x = x.replace("s'","")
    if len(Dictionary.query.filter(Dictionary.word == deredup(x.strip())).all()) > 0:
        return deredup(x.strip())
    elif len(Dictionary.query.filter(Dictionary.defin.icontains("alt. " + x.strip())).all()) > 0:
        return Dictionary.query.filter(Dictionary.defin.icontains("alt. " + x.strip())).first().word
    x = deredup(x)
    for inf in inflist:
        if x.endswith(inf):
            y = ''.join(x.rsplit(inf,1))
            if len(Dictionary.query.filter(Dictionary.word == y.strip()).all()) > 0:
                return y
            else:
                z = removeVinf(y)
                if len(Dictionary.query.filter(Dictionary.word == z.strip()).all()) > 0:
                    return z
    z = removeVinf(x)
    if len(Dictionary.query.filter(Dictionary.word == z.strip()).all()) > 0:
        return z
    return x

def removeVinf(x):
    for inf in inf2list:
        if x.endswith(inf):
            x = ''.join(x.rsplit(inf,1))
            if len(Dictionary.query.filter(Dictionary.word == x.strip()).all()) > 0:
                return x
    for vinf in infilist:
        if x.endswith(vinf):
            z = ''.join(x.rsplit(vinf, 2))
            if len(Dictionary.query.filter(Dictionary.word == z.strip() + "i").all()) > 0:
                return z + "i"
    for vinf in infylist:
        if x.endswith(vinf):
            z = ''.join(x.rsplit(vinf, 2))
            if len(Dictionary.query.filter(Dictionary.word == z.strip() + "ï").all()) > 0:
                return z + "ï"
            elif len(Dictionary.query.filter(Dictionary.word == z.strip() + "yï").all()) > 0:
                return z + "yï"
    for vinf in infelist:
        if x.endswith(vinf):
            z = ''.join(x.rsplit(vinf, 2))
            if vinf == "ayá" or vinf == "uwayá":
                for st, un in stv_pair.items():
                    z2 = z.replace(st, un)
                    if len(Dictionary.query.filter(Dictionary.word == z2.strip() + "é").all()) > 0:
                        return z2 + "é"
            else:
                if len(Dictionary.query.filter(Dictionary.word == z.strip() + "é").all()) > 0:
                    return z + "é"
    return x

def decompound(x):
    words = Dictionary.query.order_by(desc(func.length(Dictionary.word))).all()
    sep = []
    for i in words:
        if i.word in x:
            sep.append(i)
            x = ''.join(x.rsplit(i.word,1))
    return sep

def deredup(x):
    ori = x
    if x[0] == x[2]:
        return x[2:]
    else:
        for dia, mon in dia_b.items():
            x = x.replace(dia, mon)
        seccos = x[2]
        if (x[0] in cons_b) and (x[1] not in son_b):
            for vo, un in stc_pair.items():
                seccos = seccos.replace(vo,un)
            for dia, mon in dia_b.items():
                seccos = seccos.replace(dia, mon)
            if(seccos == x[0]):
                for dia, mon in dia_b.items():
                    x = x.replace(mon, dia)
                if x[1] == "s":
                    return x[:3] + x[5:]
                elif x[1] == "h":
                    return x[:3] + x[6:]
                elif x[0] == "z":
                    return x[:2] + x[5:]
                else:
                    return x[:1] + x[3:]
    return ori

def reflex(x):
    refl = 'nsywr'
    y = x
    for dia, mon in dia_b.items():
        y.replace(dia, mon)
    if y[0] in refl:
        return "a" + x[0] + x
    elif x[0] == "ɕ":
        return "as" + x
    elif x[0] == "ʑ":
        return "az" + x
    elif x[0] == "ʕ":
        return "al'" + x
    elif x[0] == "h":
        return "all" + x
    return "al" + x
