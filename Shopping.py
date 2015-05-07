from functools import wraps
from flask import Flask, redirect, render_template, flash, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'please, tell nobody'
# Session key for sesion Function
app.secret_key = "myballsareunreal!@#$%^&*(IUYTRES "

##   AUTH SECTION ###

#login required decorator

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login !')
            return redirect(url_for('login'))

    return wrap


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Creds Dude , give it another go'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout.html', methods=['GET', 'POST'])
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


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
@login_required
def index():
    return render_template('index.html')


@app.route("/shopping")
@login_required
def root():
    form = ShoppingForm()
    dairy = Shopping.query.filter(Shopping.food.any and Shopping.category == 'dairy')
    hygiene = Shopping.query.filter(Shopping.food.any and Shopping.category == 'hygiene')
    kids = Shopping.query.filter(Shopping.food.any and Shopping.category == 'kids')
    return render_template('shopping.html', form=form, dairy=dairy, hygiene=hygiene, kids=kids)


@app.route('/new', methods=['GET', 'POST'])
def newshopping():
    form = ShoppingForm()
    if form.validate_on_submit():
        shopping = Shopping()
        form.populate_obj(shopping)
        db.session.add(shopping)
        db.session.commit()
    return redirect(url_for('root'))

@app.route('/deleteitem', methods=['POST' , 'GET'])
def deleteitem():
    #item = ShoppingForm()
    #db.session.delete('from Shopping where food = ?', [request.form['item_to_delete']])
    #db.session.commit()
    return "when I figure out the deletes !"

if __name__ == "__main__":
    db.create_all()  # make our sqlalchemy tables
    app.run(debug=True, host='0.0.0.0')


# TODO INPUT VALIDATION
# TODO CENTER LOGIN PAGE
# TODO MONGOLAB
# TODO LOGOUT PAGE
# TODO INPUT VALIDATION FOR LOGINS
# TODO DEPLOY TO HEROKU
