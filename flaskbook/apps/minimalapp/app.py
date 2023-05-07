from email_validator import validate_email, EmailNotValidError
from flask import (
    Flask,
    abort,
    current_app,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    make_response,
    session,
    url_for,
)
import logging
from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

# logging
app.logger.setLevel(logging.DEBUG)
app.logger.debug("A debug message")
app.logger.info("An info message")
app.logger.warning("A warning message")
app.logger.error("An error message")
app.logger.critical("A critical message")

# debug toolbar
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)

# mail
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def index() -> str:
    return "Hello Flaskbook!"

@app.get("/hello/<name>")
def hello(name:str) -> tuple[str, int] | str:
    if name == "brian":
        return "Hello, " + name, 200
    return "Hello " + name

@app.get("/add/<int:num1>/<int:num2>")
def add(num1:int, num2:int) -> str:
    return str(num1 + num2)

# show_name endpoint
@app.get("/name/<name>")
def show_name(name:str) -> render_template:
    return render_template("index.html", name=name)

with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello", name="brian"))
    print(url_for("show_name", name="Brian"))

# application context
# push to stack to use current_app
# current_context = app.test_request_context()
# current_context.push()

# print(current_app.name)

# g.connection = "test connection"
# print(g.connection)

# request context
# with app.test_request_context("/users?update=true", method="GET"):
#     print(request.path)
#     print(request.args)
#     print(request.args.get("update"))
#     print(request.method)
#     print(request.blueprint)

# contact form
@app.route("/contact")
def contact() -> render_template:
    response = make_response(render_template("contact.html"))
    response.set_cookie("flask key", "flask value")
    session["username"] = "john"
    return response

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete() -> render_template:
    if request.method == "POST":
        # get form data
        username = request.form.get("username")
        email = request.form.get("email")
        description = request.form.get("description")
        # validate email
        is_valid = True
        if not username:
            is_valid = False
            flash("Username is required.")
        if not email:
            is_valid = False
            flash("Email is required.")

        try:
            validate_email(email)
        except EmailNotValidError as e:
            is_valid = False
            flash(str(e))

        if not description:
            is_valid = False
            flash("Description is required.")

        # if not valid, return to form
        if not is_valid:
            return render_template(
                "contact.html",
                username=username,
                email=email,
                description=description,
            )

        # send email
        send_mail(
            email,
            "お問い合わせありがとうございました。",
            "contact_mail",
            username=username,
            description=description,
        )
        flash("Thanks, we have received your message.")
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")

def send_mail(to:str, subject:str, template:str, **kwargs:str) -> None:
    msg = Message(subject, recipients=[to])
    msg.body = render_template(f"{template}.txt", **kwargs)
    msg.html = render_template(f"{template}.html", **kwargs)
    mail.send(msg)
