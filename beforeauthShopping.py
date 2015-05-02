
from flask import Flask ,redirect ,url_for,render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField, SelectField


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'please, tell nobody'


#Database Section

class Shopping(db.Model):
    """A single lunch"""
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(63))
    category = db.Column(db.String(255))


#Form Section

class ShoppingForm(Form):
    food = StringField(u'Item needed:')
    category = StringField(u'Category:')
    submit = SubmitField(u'Add')

@app.route("/")
def root():
    dairy  = Shopping.query.filter(Shopping.food.any and Shopping.category == 'dairy')
    hygiene = Shopping.query.filter(Shopping.food.any and Shopping.category == 'hygiene')
    kids = Shopping.query.filter(Shopping.food.any and Shopping.category == 'kids')
    form = ShoppingForm()
    return render_template('index.html', form=form,dairy=dairy,hygiene=hygiene,kids=kids)


@app.route('/new', methods=['POST'])
def newshopping():
    form = ShoppingForm()
    if form.validate_on_submit():
        shopping = Shopping()
        form.populate_obj(shopping)
        db.session.add(shopping)
        db.session.commit()
    return redirect(url_for('root'))

if __name__ == "__main__":
    db.create_all()  # make our sqlalchemy tables
    app.run(debug=True,host='0.0.0.0')

