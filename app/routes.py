from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app.forms import searchWord
import app.scripts as cs
from app.models import Dictionary


@app.route("/")
def hello_world():
    return "<p>Dictionary refreshed!</p>"

@app.route("/f5")
def refresh_dict():
    cs.refreshDict()
    return redirect(url_for('show_definition', word="aici"))

@app.route("/wiki/")
@app.route("/wiki/<word>", methods=['GET', 'POST'])
def show_definition(word):
    form = searchWord()
    if form.validate_on_submit():
        return redirect(url_for('show_definition', word=form.word.data))
    located = Dictionary.query.filter(Dictionary.word==word.strip()).first()
    if located is None:
        flash('No matching word found!')
        located = Dictionary.query.filter(Dictionary.word=='deva').first()
        word = "deva"
    word = word.strip()
    ipa = cs.genIPA(word)
    ipa_c = cs.genIPA_collo(ipa)
    ipa_e = cs.genIPA_eng(ipa)
    defin = located.defin.split("; ")
    pos = cs.posword(located.pos)
    root = ""
    anim = ""
    neg = ""
    if located.anim:
        match located.anim:
            case "i.":
                anim = "class i. human"
            case "ii.":
                anim = "class ii. deitic"
            case "iii.":
                anim = "class iii. inanimate and non-human animate"
    elif located.pos == "v.":
        match located.word[len(located.word)-1]:
            case "i":
                anim = "i-type"
                root = located.word[:len(located.word) - 1]
                neg = root + "u"
            case "ï":
                anim = "ï-type"
                root = located.word[:len(located.word) - 2]
                neg = root + "iy"
            case "é":
                anim = "é-type"
                root = located.word[:len(located.word) - 1]
                neg = root + "u"
            case "a":
                anim = "é-type"
                root = located.word[:len(located.word) - 1]
                neg = root + "u"
            case "y":
                anim = "i-type"
                root = located.word
                neg = root + "u"
        match neg[len(neg)-2:]:
            case "uu":
                neg = neg[:len(neg)-1] + "y"
            case "au":
                neg = neg[:len(neg) - 1] + "w/" + neg[:len(neg) - 2] + "uw" + neg[len(neg)-2]
    if "alt." in defin[0]:
        adef = defin[0].split(")") + ")"
        defin[0] = adef[1]
        alt = adef[0]
    else:
        alt = ""
    if ", from" in defin[len(defin)-1]:
        etym = "Derived from " + defin[len(defin)-1].split(", from")[len(defin)]
        defin = defin[len(defin)-1].split(", from")[:len(defin)]
    elif ", lit." in defin[len(defin)-1]:
        etym = "Derived from " + defin[len(defin) - 1].split(", lit.")[len(defin)]
        defin = defin[len(defin) - 1].split(", lit.")[:len(defin)]
    elif ", borrowed from" in defin[len(defin)-1]:
        etym = "Borrowed from " + defin[len(defin)-1].split(", borrowed from")[len(defin)]
        defin = defin[len(defin)-1].split(", borrowed from")[:len(defin)]
    else:
        etym = ""
    inf = cs.getInf(located)
    return render_template('word.html', word=word, ipa=ipa, ipa_c=ipa_c, ipa_e=ipa_e, form=form, defin=defin, pos=pos, anim=anim, alt=alt, root=root, neg=neg, etym=etym, inf=inf)