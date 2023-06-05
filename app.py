from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, gettext
from contentful import Client

# Contentful API connection
client = Client(
    'r0iojhtvlgr2',
    'RaUhiKQRQMFANqWuoS4DTiVZXUPpNiBtFhiEv_7o1iw',
    environment='master'  # Optional - it defaults to 'master'.
)

def get_locale():
    if request.args.get('language'):
        session['language'] = request.args.get('language')
    return session.get('language', 'pt')


# Init app, session and babel
app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
babel = Babel(app, locale_selector=get_locale)

app.config['languages'] =  {
    'pt': 'PT',
    'en': 'EN'
}
app.secret_key = "super secret key"

@app.context_processor
def inject_conf_var():
    return dict(AVAILABLE_LANGUAGES=app.config['languages'], 
                CURRENT_LANGUAGE=session.get('language', 
                                 request.accept_languages.best_match(app.config['languages'].keys())))

# language route
@app.route('/language=<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(url_for('index'))

# Routes
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/quem-somos")
def about():
    phd = client.entries({"content_type": "member", "fields.role": "Doutorado"})
    msc = client.entries({"content_type": "member", "fields.role": "Mestrado"})
    ic = client.entries({"content_type": "member", "fields.role": "Iniciação Científica"})
    tcc = client.entries({"content_type": "member", "fields.role": "Trabalho de Conclusão de Curso"})
    rsc = client.entries({"content_type": "member", "fields.role": "Pesquisador"})
    phd2 = client.entries({"content_type": "pastMember", "fields.type": "Doutorado", 'order': '-fields.year'})
    msc2 = client.entries({"content_type": "pastMember", "fields.type": "Mestrado", 'order': '-fields.year'})
    ic2 = client.entries({"content_type": "pastMember", "fields.type": "Iniciação Científica", 'order': '-fields.year'})
    tcc2 = client.entries({"content_type": "pastMember", "fields.type": "Trabalho de Conclusão de Curso", 'order': '-fields.year'})
    rsc2 = client.entries({"content_type": "pastMember", "fields.type": "Pesquisador", 'order': '-fields.year'})
 
    return render_template('pages/about.html',
                           title="Quem Somos",
                           members={"phd": phd,
                                    "msc": msc,
                                    "ic": ic,
                                    "tcc": tcc,
                                    "rsc": rsc},
                           past_members={"phd": phd2,
                                    "msc": msc2,
                                    "ic": ic2,
                                    "tcc": tcc2,
                                    "rsc": rsc2})

@app.route("/linhas-de-pesquisa")
def reasearch():
    reasearch = client.entries({"content_type": "researchArea"})
    return render_template('pages/research.html', 
                           title="Linhas de Pesquisa",
                           reasearch=reasearch)

@app.route("/infraestrutura")
def infra():
    equipments = client.entries({"content_type": "equipment"})
    environments = client.entries({"content_type": "environment"})
    return render_template('pages/infra.html', 
                           title="Infraestrutura",
                           equipments=equipments,
                           environments=environments)

@app.route("/produtos-desenvolvidos")
def products():
    # equipaments = client.entries({"content_type": "equipaments"})
    return render_template('pages/products.html', 
                           title="Produtos Desenvolvidos")

@app.route("/producao-cientifica")
def production():
    production = client.entries({"content_type": "academicProduction", 'order': '-fields.year'})
    articles = client.entries({"content_type": "article", 'order': '-fields.year'})
    books = client.entries({"content_type": "book"})
    patents = client.entries({"content_type": "patent"})
    prizes = client.entries({"content_type": "prize"})
    return render_template('pages/production.html', 
                           title="Produção Científica",
                           production=production,
                           articles=articles,
                           books=books,
                           patents=patents,
                           prizes=prizes)

@app.route("/parceiros")
def partners():
    partners = client.entries({"content_type": "partners"})
    research_groups = client.entries({"content_type": "researchGroup"})
    agencies = client.entries({"content_type": "agency"})
    return render_template('pages/partners.html', 
                           title="Parceiros",
                           partners=partners,
                           research_groups=research_groups,
                           agencies=agencies)

@app.route("/links")
def links():
    links = client.entries({"content_type": "link"})
    return render_template('pages/links.html', 
                           title="Links",
                           links=links)

@app.route("/contato")
def contact():
    return render_template('pages/contact.html', 
                           title="Contato")

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")