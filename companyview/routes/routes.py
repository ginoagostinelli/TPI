from companyview.helpers import helper
from companyview.controller import companies_controller
from companyview.models.models import Company, User, Favorite
from companyview.controller import companies_controller
from flask import Blueprint, render_template, Response, request, redirect, url_for , g
from companyview.helpers.forms import SignupForm,LoginForm
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from werkzeug.urls import url_parse
from flask_login import LoginManager,current_user,login_user,logout_user
from companyview.database import user_db, favorite_db


global_scope = Blueprint("views", __name__)


# @global_scope.before_request
# def before_request():
#     g.company = request.args.get("ticker")


@global_scope.route("/", methods=["GET"])
def home():
    """Landing page route."""

    return render_template("home.html")


@global_scope.route("/company", methods=["GET"])
def company():

    ticker = request.args.get("ticker")
    helper.validate_ticker(ticker)

    company = companies_controller.get_company_data(Company(ticker=ticker))
    company_data = {
        "name": company.name,
        "country": company.country,
        "city": company.city,
        "industry": company.industry,
        "employees": company.employees,
        "business": company.business,
    }

    news = companies_controller.get_news(company)

    timeline_plot = companies_controller.get_timeline_plot(company)
    dividends_plot = companies_controller.get_dividends_plot(company)
    comparation_plot = companies_controller.get_comparation_plot(company)

    return render_template(
        "companyData.html",
        **company_data,
        **news,
        timeline=timeline_plot,
        dividends=dividends_plot,
        comparation=comparation_plot,
    )


@global_scope.route("/signUp", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese emai
        user = user_db.get_by_email(email)
        if user is not None:
            error = f"El email {email} ya está siendo utilizado por otro usuario"
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user_db.create(user)
            # user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get("next", None)
            print("--------------------------------", current_user)
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("views.home")
            return redirect(next_page)
    return render_template("signUp.html", form=form, error=error)


@global_scope.route('/logIn',methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = user_db.get_by_email(form.email.data)
        #user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('views.home')
            return redirect(next_page)
        else:
            next_page = url_for('views.home')
            return redirect(next_page)
    return render_template('login.html', form=form)





@global_scope.route('/logout',methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@global_scope.route("favorite", methods=['GET', 'POST'])
def add_fav():
    if request.method == 'POST':
        f=Favorite()
        f.id_user=request.form.get('id_user') 
        f.id_company= request.form.get('id_company') 
        favorite_db.create(f)
    elif request.method == 'GET':
        return redirect(url_for('views.home'))
    
    return  render_template("companyData.html")

@global_scope.route("del_favorite", methods=['GET', 'POST'])
def del_fav():
    if request.method == 'POST':
        f=Favorite()
        f.id_user=request.form.get('id_user') 
        f.id_company= request.form.get('id_company') 
        favorite_db.delete(f)
    elif request.method == 'GET':
        return redirect(url_for('views.home'))
    
    return  render_template("companyData.html")