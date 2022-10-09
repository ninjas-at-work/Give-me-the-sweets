from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Sweets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), unique = True, nullable = False)
    description = db.Column(db.String(120))

    def __repr__(self) -> str:
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
    return 'hello world'


@app.route('/sweets')
def get_sweets():
    sweets = Sweets.query.all()
    sweets_data=[]
    for sweet in sweets:
        sweet_info = {'name':sweet.name, 'description':sweet.description}
        sweets_data.append(sweet_info)
    return {"sweets":sweets_data}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/sweets/<id>')
def get_sweet(id):
    sweet = Sweets.query.get_or_404(id)

    return {"name":sweet.name, "description":sweet.description}



@app.route('/sweets', methods=['POST'])
def add_sweet():
    sweet = Sweets(name = request.json['name'], description=request.json['description'])
    db.session.add(sweet)
    db.session.commit()
    return {'id':sweet.id}


@app.route('/sweets/<id>', methods=['DELETE'])
def delete_sweet(id):
    sweet = Sweets.query.get(id)
    if sweet is None:
        return {"message":"sweet does not exist, are you sure?"}
    db.session.delete(sweet)
    db.session.commit()
    return {"message":"sweet deleted"}