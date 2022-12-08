import os, hashlib
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/perfil')
def perfil():
    #Con esta condicional validamos que esta autenticado para recien mostrarle el template
    if current_user.is_authenticated:
        return render_template("perfil.html", status=current_user.is_authenticated)
    else:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    import models.users
    if request.method == "POST":
        from models.users import Users

        correoE = request.form.get("correoR")
        contrasenaE = request.form.get("contrasenaR")

        if request.form.get(("rememberR")):
            rememberE = True
        else:
            rememberE = False
        user = Users.query.filter_by(correo=correoE).first()

        if user is None:
            flash("correo o contraseña incorrecta")
            return redirect(url_for('login'))
        elif user.check_password(contrasenaE):
            login_user(user, remember=rememberE)
            return redirect(url_for('perfil'))
        else:
            flash("correo o contraseña incorrecta")
            return redirect(url_for('login'))

    return render_template("index.html")


@app.route('/logout')
def logout():
    logout_user()
    return render_template("index.html")

@app.route('/registro', methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuarioE = request.form.get("usuarioR")
        emailE = request.form.get("emailR")
        passwordE = request.form.get("passwordR")

        from models.users import Users
        newuser = Users(usuario=usuarioE, correo=emailE)
        newuser.set_password(passwordE)

        db.session.add(newuser)
        db.session.commit()

        nombreE = request.form.get("nombreR")
        locacionE = request.form.get("locacionR")
        informacionE = request.form.get("informacionR")
        fecha_creacionE = datetime.utcnow()
        avatarE = gravatar(emailE)

        #Query para traer datos de la tabla en la bd filtrando por correo
        user = Users.query.filter_by(correo=newuser.correo).first()

        from models.profiles import Profile
        newprofile = Profile(user_id=user.id, nombre=nombreE, locacion=locacionE, informacion=informacionE, fecha_creacion=fecha_creacionE, avatar=avatarE)
        print(nombreE, locacionE, informacionE,fecha_creacionE, avatarE)
        
        db.session.add(newprofile)
        db.session.commit()

    return render_template("registro.html")


@app.route('/actualizar', methods=["GET", "POST"])
@login_required
def actualizar():
    from models.users import Users
    lsUsers = Users.query.all()

    if request.method == "POST":
        oldemail = request.form.get("oldcorreoR")
        email = request.form.get("correoR")

        from models.users import Users
        user = Users.query.filter_by(correo=oldemail).first()

        user.correo = email
        db.session.commit()

    return render_template("actualizar.html", users=lsUsers)


@app.route('/eliminar', methods=["GET", "POST"])
@login_required
def eliminar():
    from models.users import Users
    lsUsers = Users.query.all()

    if request.method == "POST":
        email = request.form.get("correoR")

        from models.users import Users
        user = Users.query.filter_by(correo=email).first()

        db.session.delete(user)
        db.session.commit()

    return render_template("eliminar.html", users=lsUsers)

#Creamos la funcion para gravatar
def gravatar(emailE, sizeE=256,defaultE="identicon", ratingE="g"):
    urlE = "https://secure.gravatar.com/avatar"
    hashE = hashlib.md5(emailE.encode("utf-8")).hexdigest()
    return "{url}/{hash}?s={size}&d={default}&r={rating}".format(
        url=urlE, hash=hashE, size=sizeE, default=defaultE, rating=ratingE)

if __name__ == '__main__':
    app.run()
