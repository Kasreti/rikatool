from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app.forms import searchWord
import app.scripts as cs
from app.models import Dictionary
from sqlalchemy.sql import collate

@app.route("/")
def hello_world():
    return "<p>y u here mf</p>"

@app.route("/f5")
def refresh_dict():
    cs.refreshDict()
    return redirect(url_for('show_definition', word="aici"))

@app.route("/search/")
@app.route("/search/<term>?st=word", methods=['GET', 'POST'])
def wresults(term):
    form = searchWord()
    if form.validate_on_submit():
        located = Dictionary.query.filter(Dictionary.word == form.word.data.strip()).all()
        located2 = Dictionary.query.filter(Dictionary.word == cs.removeInf(form.word.data.strip())).all()
        if form.refresh.data:
            return redirect(url_for('refresh_dict'))
        elif len(located) == 0 and len(located2) > 0:
            return redirect(url_for('show_definition', word=cs.removeInf(form.word.data.strip())))
        elif len(located) == 0 and len(located2) == 0:
            if form.defsubmit.data:
                return redirect(url_for('dresults', term=form.word.data.strip()))
            else:
                return redirect(url_for('wresults', term=form.word.data.strip()))
        else:
            return redirect(url_for('show_definition', word=form.word.data.strip()))
    matches = Dictionary.query.filter(Dictionary.word.icontains(term)).order_by(collate(Dictionary.word, 'NOCASE')).all()
    return render_template('results.html', term=term, matches=matches, form=form)
@app.route("/search/<term>?st=def", methods=['GET', 'POST'])
def dresults(term):
    form = searchWord()
    if form.validate_on_submit():
        located = Dictionary.query.filter(Dictionary.word == form.word.data.strip()).all()
        located2 = Dictionary.query.filter(Dictionary.word == cs.removeInf(form.word.data.strip())).all()
        if form.refresh.data:
            return redirect(url_for('refresh_dict'))
        elif len(located) == 0 and len(located2) > 0:
            return redirect(url_for('show_definition', word=cs.removeInf(form.word.data.strip())))
        elif len(located) == 0 and len(located2) == 0:
            if form.defsubmit.data:
                return redirect(url_for('dresults', term=form.word.data.strip()))
            else:
                return redirect(url_for('wresults', term=form.word.data.strip()))
        else:
            return redirect(url_for('show_definition', word=form.word.data.strip()))
    matches = Dictionary.query.filter(Dictionary.defin.icontains(term)).order_by(collate(Dictionary.word, 'NOCASE')).all()
    return render_template('results.html', term=term, matches=matches, form=form)

@app.route("/wiki/")
@app.route("/wiki/<word>", methods=['GET', 'POST'])
def show_definition(word):
    form = searchWord()
    located = Dictionary.query.filter(Dictionary.word == word.strip()).all()
    retword = []
    if form.validate_on_submit():
        located = Dictionary.query.filter(Dictionary.word == form.word.data.strip()).all()
        located2 = Dictionary.query.filter(Dictionary.word == cs.removeInf(form.word.data.strip())).all()
        if form.refresh.data:
            return redirect(url_for('refresh_dict'))
        elif len(located) == 0 and len(located2) > 0:
            return redirect(url_for('show_definition', word=cs.removeInf(form.word.data.strip())))
        elif len(located) == 0 and len(located2) == 0:
            if form.defsubmit.data:
                return redirect(url_for('dresults', term=form.word.data.strip()))
            else:
                return redirect(url_for('wresults', term=form.word.data.strip()))
        else:
            return redirect(url_for('show_definition', word=form.word.data.strip()))
    for x in located:
        defin = x.defin.split("; ")
        root = ""
        anim = ""
        neg = ""
        if x.anim:
            match x.anim:
                case "i.":
                    anim = "class i. human"
                case "ii.":
                    anim = "class ii. deitic"
                case "iii.":
                    anim = "class iii. inanimate and non-human animate"
        elif x.pos == "v." or "stv.":
            match x.word[len(x.word)-1]:
                case "i":
                    anim = "i-type"
                    root = x.word[:len(x.word) - 1]
                    neg = root + "u"
                case "ï":
                    anim = "ï-type"
                    root = x.word[:len(x.word) - 2]
                    neg = root + "iy"
                case "é":
                    anim = "é-type"
                    root = x.word[:len(x.word) - 1]
                    neg = root + "u"
                case "a":
                    anim = "é-type"
                    root = x.word[:len(x.word) - 1]
                    neg = root + "u"
                case "y":
                    anim = "i-type"
                    root = x.word
                    neg = root + "u"
        match neg[len(neg)-2:]:
            case "uu":
                neg = neg[:len(neg)-1] + "y"
            case "au":
                neg = neg[:len(neg) - 1] + "w/" + neg[:len(neg) - 2] + "uw" + neg[len(neg)-2]
        if "alt." in defin[0]:
            adef = defin[0].split(")")
            defin[0] = adef[1]
            alt = adef[0] + ")"
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
        retword.append(cs.definition(x.word.strip(),cs.genIPA(word),cs.genIPA_collo(cs.genIPA(word)),cs.genIPA_eng(cs.genIPA(word)),defin,anim,cs.posword(x.pos),etym,root,cs.getInf(x), alt, neg, cs.redup(x)))
    return render_template('word.html', retword=retword, form=form)