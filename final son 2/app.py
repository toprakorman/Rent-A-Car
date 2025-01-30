from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.models import db, User, Car, Office
from helpers.auth_handler import hash_password, check_password, is_authenticated, get_current_user
from helpers.validators import validate_user_registration
from helpers.google_maps import get_office_locations
from config import Config
from languages import LANGUAGES

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.context_processor
def inject_is_authenticated():
    return dict(is_authenticated=is_authenticated)

def create_sample_data():
    if not Office.query.first():
        # Create offices
        offices_data = [
            {"name": "Izmir Office", "location": "Izmir", "address": "123 Izmir St.", "phone_no": "1234567890", "latitude": 38.4237, "longitude": 27.1428},
            {"name": "Istanbul Office", "location": "Istanbul", "address": "456 Istanbul St.", "phone_no": "0987654321", "latitude": 41.0082, "longitude": 28.9784},
            {"name": "Ankara Office", "location": "Ankara", "address": "789 Ankara St.", "phone_no": "1122334455", "latitude": 39.9334, "longitude": 32.8597},
        ]

        for office_data in offices_data:
            office = Office(**office_data)
            db.session.add(office)
        db.session.commit()

        offices = Office.query.all()
        car_data = [
            {"name": "Honda Civic", "transmission": "Automatic", "cost": 30000, "deposit": 5000, "mileage": 15000, "age": 3, "rental_cost": 100, "image": "images/civic.jpg"},
            {"name": "Toyota Corolla", "transmission": "Manual", "cost": 20000, "deposit": 4000, "mileage": 12000, "age": 2, "rental_cost": 80, "image": "images/corolla.jpg"},
            {"name": "Ford Mustang", "transmission": "Automatic", "cost": 35000, "deposit": 6000, "mileage": 8000, "age": 4, "rental_cost": 120, "image": "images/mustang.jpg"},
            {"name": "Chevrolet Malibu", "transmission": "Manual", "cost": 25000, "deposit": 4500, "mileage": 10000, "age": 3, "rental_cost": 90, "image": "images/malibu.jpg"},
            {"name": "Nissan Altima", "transmission": "Automatic", "cost": 28000, "deposit": 5500, "mileage": 7000, "age": 1, "rental_cost": 110, "image": "images/altima.jpg"},
            {"name": "Mazda 3", "transmission": "Manual", "cost": 22000, "deposit": 4700, "mileage": 15000, "age": 2, "rental_cost": 95, "image": "images/mazda3.jpg"},
            {"name": "Hyundai Sonata", "transmission": "Automatic", "cost": 27000, "deposit": 5200, "mileage": 9000, "age": 3, "rental_cost": 105, "image": "images/sonata.jpg"},
            {"name": "Volkswagen Jetta", "transmission": "Manual", "cost": 23000, "deposit": 4200, "mileage": 11000, "age": 2, "rental_cost": 85, "image": "images/jetta.jpg"},
            {"name": "Subaru Outback", "transmission": "Automatic", "cost": 32000, "deposit": 5800, "mileage": 6000, "age": 4, "rental_cost": 115, "image": "images/outback.jpg"},
            {"name": "Kia Forte", "transmission": "Manual", "cost": 19000, "deposit": 3500, "mileage": 14000, "age": 2, "rental_cost": 75, "image": "images/forte.jpg"},
            {"name": "Tesla Model 3", "transmission": "Automatic", "cost": 40000, "deposit": 7000, "mileage": 5000, "age": 1, "rental_cost": 130, "image": "images/model3.jpg"},
            {"name": "BMW 3 Series", "transmission": "Automatic", "cost": 45000, "deposit": 8000, "mileage": 7000, "age": 2, "rental_cost": 140, "image": "images/bmw3.jpg"},
            {"name": "Audi A4", "transmission": "Manual", "cost": 42000, "deposit": 7500, "mileage": 9000, "age": 3, "rental_cost": 135, "image": "images/audi_a4.jpg"},
            {"name": "Mercedes-Benz C-Class", "transmission": "Automatic", "cost": 47000, "deposit": 8500, "mileage": 8000, "age": 2, "rental_cost": 145, "image": "images/c_class.jpg"},
            {"name": "Porsche 911", "transmission": "Automatic", "cost": 90000, "deposit": 15000, "mileage": 4000, "age": 1, "rental_cost": 250, "image": "images/911.jpg"},
            {"name": "Jaguar XE", "transmission": "Manual", "cost": 48000, "deposit": 8700, "mileage": 8500, "age": 2, "rental_cost": 150, "image": "images/jaguar_xe.jpg"},
            {"name": "Lexus IS", "transmission": "Automatic", "cost": 46000, "deposit": 8200, "mileage": 7800, "age": 2, "rental_cost": 140, "image": "images/lexus_is.jpg"},
            {"name": "Dodge Charger", "transmission": "Manual", "cost": 39000, "deposit": 6900, "mileage": 11000, "age": 3, "rental_cost": 125, "image": "images/charger.jpg"},
            ]

        car_index = 0
        for office in offices:
            for _ in range(6):
                car = Car(**car_data[car_index], office_id=office.id)
                db.session.add(car)
                car_index += 1
        db.session.commit()

        print("Sample data created successfully.")

@app.before_request
def set_language():
    session.setdefault("language", "en")

@app.context_processor
def inject_language():
    lang = session.get("language", "en")
    return dict(language=lang, translations=LANGUAGES[lang])

@app.route("/set_language/<lang>")
def set_language_route(lang):
    if lang in LANGUAGES:
        session["language"] = lang
    return redirect(request.referrer or url_for("home"))

# Home page
@app.route('/')
def home():
    offices = Office.query.all()
    locations = [{"id": office.id, "lat": office.latitude, "lng": office.longitude, "name": office.name} for office in offices]
    
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        greeting = f"{LANGUAGES[session.get('language', 'en')]['login_success']}, {user.username}"
    else:
        greeting = f"{LANGUAGES[session.get('language', 'en')]['greet']}"
        
    return render_template('home.html', offices=offices, locations=locations, greeting=greeting)


@app.route('/search')
def search():
    pickup_office_id = request.args.get('pickup_office')
    transmission = request.args.get('transmission')
    sort_option = request.args.get('sort')

    query = Car.query
    if pickup_office_id:
        query = query.filter_by(office_id=pickup_office_id)

    if transmission:
        query = query.filter(Car.transmission == transmission)

    if sort_option:
        if sort_option == "cost_asc":
            query = query.order_by(Car.cost.asc())
        elif sort_option == "cost_desc":
            query = query.order_by(Car.cost.desc())
        elif sort_option == "mileage_asc":
            query = query.order_by(Car.mileage.asc())
        elif sort_option == "mileage_desc":
            query = query.order_by(Car.mileage.desc())

    cars = query.all()
    return render_template('search_results.html', cars=cars)

@app.route('/office/<int:office_id>')
def office_info(office_id):
    office = Office.query.get_or_404(office_id)
    return render_template('office_info.html', office=office)

@app.route('/office/<int:office_id>/cars')
def show_office_cars(office_id):
    office = Office.query.get_or_404(office_id)
    return render_template('search_results.html', cars=office.cars)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_detail.html', car=car)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password(user.password, password):
            session['user_id'] = user.id
            flash(f"{LANGUAGES[session.get('language', 'en')]['login_success']}, {user.username}!", "success")
            return redirect(url_for('home'))
        else:
            flash(f"{LANGUAGES[session.get('language', 'en')]['invalid_login']}", 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash(f"{LANGUAGES[session.get('language', 'en')]['logged_out']}", 'success')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        country = request.form.get('country')
        city = request.form.get('city')

        photo = request.files.get('photo')

        existing_user = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()
        if existing_user:
            flash(f"{LANGUAGES[session.get('language', 'en')]['invalid_regis']}", 'error')
            return redirect(url_for('register'))
        
        hashed_password = hash_password(password)

        new_user = User(
            email=email,
            username=username,
            password=hashed_password,
            country=country,
            city=city
        )

        db.session.add(new_user)
        db.session.commit()

        flash(f"{LANGUAGES[session.get('language', 'en')]['regis_success']}", 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    app.run(debug=True)
