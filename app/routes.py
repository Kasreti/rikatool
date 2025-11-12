from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app.forms import searchWord
import app.scripts as cs
from app.models import Dictionary
from sqlalchemy.sql import collate, func

@app.route("/")
def hello_world():
    return redirect(url_for('show_definition', word="aici"))

@app.errorhandler(404)
def page_not_found(e):
    flash("thats not a real page bro :skull:")
    return redirect(url_for('show_definition', word="aici"))

@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')

@app.errorhandler(500)
def internal_server_error(e):
    flash("uhh server messed up, dm kasreti about this")
    return redirect(url_for('show_definition', word="aici"))

@app.route("/search/")
@app.route("/search/<term>?st=word", methods=['GET', 'POST'])
def wresults(term):
    form = searchWord()
    if form.validate_on_submit():
        session['prev'] = form.word.data.strip().casefold()
        located = Dictionary.query.filter(Dictionary.word == form.word.data.strip().casefold()).all()
        located2 = []
        if form.refresh.data:
            cs.refreshDict()
            flash("dictionary refreshed!!")
        elif form.fuzsubmit.data:
            return redirect(url_for('wresults', term=form.word.data.strip().casefold()))
        elif form.genipa.data:
            flash("IPA for " + '"' + form.word.data.strip().casefold() + '"')
            flash("(Hayalese): /" + cs.genIPA(form.word.data.strip().casefold()) + "/")
            flash("(Distaye): /" + cs.genIPA_collo(cs.genIPA(form.word.data.strip().casefold())) + "/")
            flash("(Hasiph): /" + cs.genIPA_eng(cs.genIPA(form.word.data.strip().casefold()),form.word.data.strip().casefold()) + "/")
        elif form.random.data:
            gen = Dictionary.query.order_by(func.random()).first()
            return redirect(url_for('show_definition', word=gen.word))
        elif form.defsubmit.data:
            return redirect(url_for('dresults', term=form.word.data.strip().casefold()))
        if len(located) == 0:
            located2 = Dictionary.query.filter(Dictionary.word == cs.removeInf(form.word.data.strip().casefold())).all()
            print(cs.removeInf(form.word.data.strip().casefold()))
            if len(located) == 0 and len(located2) > 0:
                return redirect(url_for('show_definition', word=cs.removeInf(form.word.data.strip().casefold())))
            elif len(located) == 0 and len(located2) == 0:
                return redirect(url_for('wresults', term=form.word.data.strip().casefold()))
        else:
            return redirect(url_for('show_definition', word=form.word.data.strip().casefold()))
    matches = Dictionary.query.filter(Dictionary.word.icontains(term)).order_by(collate(Dictionary.word, 'NOCASE')).all()
    form.word.data = session['prev']
    if len(matches) == 0:
        matches = cs.decompound(term)
    return render_template('results.html', term=term, matches=matches, form=form)
@app.route("/search/<term>?st=def", methods=['GET', 'POST'])
def dresults(term):
    form = searchWord()
    if form.validate_on_submit():
        session['prev'] = form.word.data.strip().casefold()
        located = Dictionary.query.filter(Dictionary.word == form.word.data.strip().casefold()).all()
        located2 = []
        if form.refresh.data:
            cs.refreshDict()
            flash("dictionary refreshed!!")
        elif form.fuzsubmit.data:
            return redirect(url_for('wresults', term=form.word.data.strip().casefold()))
        elif form.genipa.data:
            flash("IPA for " + '"' + form.word.data.strip().casefold() + '"')
            flash("(Hayalese): /" + cs.genIPA(form.word.data.strip().casefold()) + "/")
            flash("(Distaye): /" + cs.genIPA_collo(cs.genIPA(form.word.data.strip().casefold())) + "/")
            flash("(Hasiph): /" + cs.genIPA_eng(cs.genIPA(form.word.data.strip().casefold()),form.word.data.strip().casefold()) + "/")
        elif form.random.data:
            gen = Dictionary.query.order_by(func.random()).first()
            return redirect(url_for('show_definition', word=gen.word))
        elif form.defsubmit.data:
            return redirect(url_for('dresults', term=form.word.data.strip().casefold()))
        if len(located) == 0:
            located2 = Dictionary.query.filter(Dictionary.word == cs.removeInf(form.word.data.strip().casefold())).all()
            print(cs.removeInf(form.word.data.strip().casefold()))
            if len(located) == 0 and len(located2) > 0:
                return redirect(url_for('show_definition', word=cs.removeInf(form.word.data.strip().casefold())))
            elif len(located) == 0 and len(located2) == 0:
                return redirect(url_for('wresults', term=form.word.data.strip().casefold()))
        else:
            return redirect(url_for('show_definition', word=form.word.data.strip().casefold()))
    matches = Dictionary.query.filter(Dictionary.defin.icontains(term)).order_by(collate(Dictionary.word, 'NOCASE')).all()
    form.word.data = session['prev']
    return render_template('results.html', term=term, matches=matches, form=form)

@app.route("/wiki/")
@app.route("/wiki/<word>", methods=['GET', 'POST'])
def show_definition(word):
    form = searchWord()
    located = Dictionary.query.filter(Dictionary.word == word.strip().casefold()).all()
    retword = []
    if form.validate_on_submit():
        session['prev'] = form.word.data.strip().casefold()
        located = Dictionary.query.filter(Dictionary.word == form.word.data.strip().casefold()).all()
        located2 = []
        if form.refresh.data:
            cs.refreshDict()
            flash("dictionary refreshed!!")
            return redirect(url_for('show_definition', word=word))
        elif form.markentry.data:
            cs.markEntry(word)
            flash("entry marked!!")
            return redirect(url_for('show_definition', word=word))
        elif form.genipa.data:
            flash("IPA for " + '"' + form.word.data.strip().casefold() + '"')
            flash("(Hayalese): /" + cs.genIPA(form.word.data.strip().casefold()) + "/")
            flash("(Distaye): /" + cs.genIPA_collo(cs.genIPA(form.word.data.strip().casefold())) + "/")
            flash("(Hasiph): /" + cs.genIPA_eng(cs.genIPA(form.word.data.strip().casefold()),form.word.data.strip().casefold()) + "/")
            return redirect(url_for('show_definition', word=word))
        elif form.fuzsubmit.data:
            return redirect(url_for('wresults', term=form.word.data.strip().casefold()))
        elif form.random.data:
            gen = Dictionary.query.order_by(func.random()).first()
            return redirect(url_for('show_definition', word=gen.word))
        elif form.defsubmit.data:
            return redirect(url_for('dresults', term=form.word.data.strip().casefold()))
        if len(located) == 0:
            located2 = Dictionary.query.filter(Dictionary.word == cs.removeInf(form.word.data.strip().casefold())).all()
            print(cs.removeInf(form.word.data.strip().casefold()))
            if len(located) == 0 and len(located2) > 0:
                return redirect(url_for('show_definition', word=cs.removeInf(form.word.data.strip().casefold())))
            elif len(located) == 0 and len(located2) == 0:
                return redirect(url_for('wresults', term=form.word.data.strip().casefold()))
        else:
            return redirect(url_for('show_definition', word=form.word.data.strip().casefold()))
    for x in located:
        defin = x.defin.split("; ")
        print(defin)
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
        elif x.pos == "v." or x.pos == "stv.":
            if x.word[len(x.word)-1] == "m":
                endvowel = x.word[len(x.word)-2]
            else:
                endvowel = x.word[len(x.word)-1]
            match endvowel:
                case "i":
                    anim = "i-type"
                    root = x.word[:len(x.word) - 1]
                    neg = root + "u"
                case "ï":
                    anim = "yï-type"
                    if x.word[:len(x.word)-2] == "y":
                        root = x.word[:len(x.word) - 2]
                    else:
                        root = x.word[:len(x.word) - 2] + "ï"
                    neg = root + "iy"
                case "é":
                    anim = "é-type"
                    root = x.word[:len(x.word) - 1]
                    neg = root + "u"
                case "e":
                    anim = "é-type (caus.)"
                    root = x.word
                    neg = root + "u"
                case "a":
                    anim = "é-type"
                    root = x.word[:len(x.word) - 1]
                    neg = root + "u"
                case "á":
                    anim = "é-type (passive)"
                    root = x.word[:len(x.word) - 1]
                    neg = root + "u"
                case "y":
                    anim = "i-type (palatal.)"
                    root = x.word
                    neg = root + "u"
                case _:
                    anim = "i-type (cons.)"
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
            etym = "Derived from " + defin[len(defin)-1].split(", from")[len(defin[len(defin)-1].split(", from"))-1]
            defin[len(defin)-1] = defin[len(defin)-1].split(", from")[0] + "."
        elif ", lit." in defin[len(defin)-1]:
            etym = "Derived from " + defin[len(defin) - 1].split(", lit.")[len(defin[len(defin)-1].split(", lit."))-1]
            defin[len(defin)-1] = defin[len(defin)-1].split(", lit.")[0] + "."
        elif ", borrowed from" in defin[len(defin)-1]:
            etym = "Borrowed from " + defin[len(defin)-1].split(", borrowed from")[len(defin[len(defin)-1].split(", borrowed from"))-1]
            defin[len(defin)-1] = defin[len(defin)-1].split(", borrowed from")[0] + "."
        elif ", root noun" in defin[len(defin)-1]:
            etym = "Derivation of root noun " + defin[len(defin)-1].split(", root noun")[len(defin[len(defin)-1].split(", root noun"))-1]
            defin[len(defin)-1] = defin[len(defin)-1].split(", root noun")[0] + "."
        elif ", contraction of" in defin[len(defin)-1]:
            etym = "Derivation from a contraction of " + defin[len(defin)-1].split(", contraction of")[len(defin[len(defin)-1].split(", contraction of"))-1]
            defin[len(defin)-1] = defin[len(defin)-1].split(", contraction of")[0] + "."
        else:
            etym = ""
        retword.append(cs.definition(x.word.strip().casefold(),cs.genIPA(word),cs.genIPA_collo(cs.genIPA(word)),cs.genIPA_eng(cs.genIPA(word),word),defin,anim,cs.posword(x.pos),etym,root,cs.getInf(x),cs.getAspInf(x),alt, neg, cs.redup(x), cs.reflex(x.word)))
    if session.get('prev'):
        if session['prev']:
            form.word.data = session['prev']
    else:
        form.word.data = ""
    related = Dictionary.query.filter(Dictionary.word.icontains(word.strip().casefold()),Dictionary.word != word.strip().casefold()).order_by(collate(Dictionary.word, 'NOCASE')).all()
    return render_template('word.html', retword=retword, related=related, form=form)