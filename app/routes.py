from app import app, db
from flask import render_template, request, jsonify, flash,\
    redirect, url_for
from flask_login import current_user, login_required, login_user, \
    logout_user
import stripe
from app.models import User
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegisterForm, ResetPasswordForm,\
    ResetPasswordRequestForm
import africastalking

def send_airtime():
    username = "sandbox"
    api_key = app.config['AFRICASTALKING_API_KEY']

    africastalking.initialize(username, api_key)

    airtime = africastalking.Airtime

    phone_number = current_user.phone
    currency_code = "KES" #Change this to your country's code
    amount = 5

    try:
        response = airtime.send(
            phone_number=phone_number, amount=amount, currency_code=currency_code)
        print(response)
    except Exception as e:
        print(f"Encountered an error while sending airtime. More error details below\n {e}")

# User Authentication

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html',
                           title='Login',
                           form=form
                           )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! Login to continue.')
        return redirect(url_for('login'))
    return render_template('auth/register.html',
                           title='Register',
                           form=form
                           )


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/product-detail')
@login_required
def product_detail():
    return render_template('product_detail.html')

@app.route('/config')
def get_publishable_key():
    stripe_config = {
        'publicKey': app.config['STRIPE_PUBLISHABLE_KEY']
    }
    return jsonify(stripe_config)


@app.route('/create-checkout-session')
def create_checkout_session():
    domain_url = 'http://127.0.0.1:5000/'
    stripe.api_key = app.config['STRIPE_SECRET_KEY']
    try:
        checkout_session = stripe.checkout.Session.create(
            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have
            # the session ID set as a query param
            # success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}'
            success_url=domain_url + 'success',
            cancel_url=domain_url + 'cancelled',
            payment_method_types=['card'],
            billing_address_collection='required',
            mode='payment',
            line_items=[
                {
                    'quantity': 1,
                    'price': 'price_1MSFYUFWpU2KHaPL6UDMKPoi',
                }
            ]
        )
        return jsonify({'sessionId': checkout_session['id']})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/success')
@login_required
def success():
    send_airtime()
    flash('Enjoy your free airtime')
    return render_template('success.html', title='Success')


@app.route('/cancelled')
def cancel():
    return render_template('cancel.html', title='Cancel')


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, app.config["STRIPE_ENDPOINT_SECRET"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        flash("Payment was successful.")

    return "Success", 200
