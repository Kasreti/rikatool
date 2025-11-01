from flask import Flask, render_template
import app.scripts as cs

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/wiki/")
@app.route("/wiki/<word>")
def show_definition(word):
    ipa = cs.genIPA(word)
    ipa_c = cs.genIPA_collo(ipa)
    ipa_e = cs.genIPA_eng(ipa)
    return render_template('word.html', word=word, ipa=ipa, ipa_c=ipa_c, ipa_e=ipa_e)