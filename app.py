from flask import Flask, render_template
from contentful import Client

client = Client(
    'r0iojhtvlgr2',
    'RaUhiKQRQMFANqWuoS4DTiVZXUPpNiBtFhiEv_7o1iw',
    environment='master'  # Optional - it defaults to 'master'.
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route("/quem-somos")
def about():
    members = client.entries({"content_type": "member"})
    past_members = client.entries({"content_type": "pastMember"})
    return render_template('pages/about.html', 
                           title="Quem Somos",
                           members=members,
                           past_members=past_members)

@app.route("/linhas-de-pesquisa")
def reasearch():
    reasearch = client.entries({"content_type": "researchArea"})
    return render_template('pages/research.html', 
                           title="Linhas de Pesquisa",
                           reasearch=reasearch)

@app.route("/infraestrutura")
def infra():
    equipments = client.entries({"content_type": "equipment"})
    return render_template('pages/infra.html', 
                           title="Infraestrutura",
                           equipments=equipments)

@app.route("/produtos-desenvolvidos")
def products():
    # equipaments = client.entries({"content_type": "equipaments"})
    return render_template('pages/products.html', 
                           title="Produtos Desenvolvidos")

@app.route("/producao-cientifica")
def production():
    production = client.entries({"content_type": "academicProduction"})
    articles = client.entries({"content_type": "article"})
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
    app.run(debug=False, host="0.0.0.0")