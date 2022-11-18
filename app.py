import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/landing')
def landing():
    if current_user.is_authenticated:
        return render_template("landing.html", status=current_user.is_authenticated)
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
            flash("Correo invalido o contrasena")
            return redirect(url_for('login'))
        elif user.check_password(contrasenaE):
            login_user(user, remember=rememberE)
            return redirect(url_for('landing'))
        else:
            flash("Correo invalido o contrasena")
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
        emailE = request.form.get("correoR")
        passwordE = request.form.get("passR")

        from models.users import Users
        newuser = Users(usuario=usuarioE, correo=emailE)
        newuser.set_password(passwordE)

        db.session.add(newuser)
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


if __name__ == '__main__':
    app.run()
