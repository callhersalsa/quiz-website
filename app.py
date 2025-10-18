"""
Main Flask application for LeetQuiz.
This module sets up the Flask app, configures the database, and defines routes for:
- Home page with weather forecast integration via Open-Meteo API.
- User registration and login using WTForms.
- Quiz functionality with question retrieval and score tracking.
- Leaderboard displaying top users by score.

All routes render appropriate templates and handle form submissions.

API integration with Open-Meteo includes geocoding and fetching 3-day weather forecasts with day/night splits.
Weather codes and icons are mapped using data from local modules. In data folder.
Weather icons are retrieved from data/weather_icons.py and openweather collections https://openweathermap.org/weather-conditions.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User
from forms import RegisterForm, LoginForm
from quiz_data import get_random_question, total_questions
from collections import Counter
from data.weather_codes import wc_map
from data.weather_icons import icon_for
from datetime import datetime

import requests
import os
import json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    # SECRET_KEY for WTForms CSRF and session security. Replace in production with a secure env var.
    app.config["SECRET_KEY"] = os.environ.get("LEETQUIZ_SECRET", "dev-secret-key-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "leetquiz.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # create DB & tables if they don't exist
    with app.app_context():
        db.create_all()

    # ---------- Helper: Open-Meteo integration ----------
    def fetch_open_meteo_forecast(city_name):
        """
        Returns Open Meteo forecast (3 days: today, tomorrow, day after tomorrow)
        with day/night split and additional weather stats.
        """
        # Geocoding location
        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
        gparams = {"name": city_name, "count": 1, "language": "en", "format": "json"}
        gresp = requests.get(geocode_url, params=gparams, timeout=10)
        if gresp.status_code != 200 or not gresp.json().get("results"):
            return None
        place = gresp.json()["results"][0]
        lat, lon = place["latitude"], place["longitude"]
        display_name = place.get("name") or city_name

        # Forecast (next 3 days)
        forecast_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,weathercode,relativehumidity_2m,precipitation,windspeed_10m",
            "timezone": "auto",
            "forecast_days": 3
        }
        fresp = requests.get(forecast_url, params=params, timeout=10)
        if fresp.status_code != 200:
            return None
        fjson = fresp.json()

        hourly = fjson["hourly"]
        times = hourly["time"]
        temps = hourly["temperature_2m"]
        codes = hourly["weathercode"]
        hums = hourly["relativehumidity_2m"]
        precs = hourly["precipitation"]
        winds = hourly["windspeed_10m"]
        
        # Compile day/night summaries for 3 days 
        days = []
        for date in sorted({t.split("T")[0] for t in times}):
            day_temps, night_temps, day_codes, night_codes = [], [], [], []
            day_hum, night_hum, day_prec, night_prec, day_wind, night_wind = [], [], [], [], [], []

            for i, t in enumerate(times):
                if not t.startswith(date):
                    continue
                hour = int(t.split("T")[1].split(":")[0])
                if 6 <= hour < 18:
                    day_temps.append(temps[i])
                    day_codes.append(codes[i])
                    day_hum.append(hums[i])
                    day_prec.append(precs[i])
                    day_wind.append(winds[i])
                else:
                    night_temps.append(temps[i])
                    night_codes.append(codes[i])
                    night_hum.append(hums[i])
                    night_prec.append(precs[i])
                    night_wind.append(winds[i])
                    
            # Helper to get summary description
            def summary(codes):
                return wc_map.get(Counter(codes).most_common(1)[0][0], "Weather") if codes else "Weather"
            
            # Compile day/night data
            days.append({
                "date": datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d %B %Y"),
                "day": {
                    "description": summary(day_codes),
                    "icon": icon_for(day_codes, is_day=True),
                    "temp_max": round(max(day_temps), 1) if day_temps else None,
                    "temp_min": round(min(day_temps), 1) if day_temps else None,
                    "humidity": round(sum(day_hum)/len(day_hum)) if day_hum else None,
                    "precipitation": round(sum(day_prec), 1) if day_prec else None,
                    "wind": round(sum(day_wind)/len(day_wind), 1) if day_wind else None
                },
                "night": {
                    "description": summary(night_codes),
                    "icon": icon_for(night_codes, is_day=False),
                    "temp_max": round(max(night_temps), 1) if night_temps else None,
                    "temp_min": round(min(night_temps), 1) if night_temps else None,
                    "humidity": round(sum(night_hum)/len(night_hum)) if night_hum else None,
                    "precipitation": round(sum(night_prec), 1) if night_prec else None,
                    "wind": round(sum(night_wind)/len(night_wind), 1) if night_wind else None
                }
            })

        return {"city": display_name, "latitude": lat, "longitude": lon, "days": days[:3]}

    # ---------- Routes ----------
    # Home page with weather forecast
    @app.route("/", methods=["GET"])
    def home():
        city = request.args.get("city", "").strip()
        weather = None
        if city:
            try:
                weather = fetch_open_meteo_forecast(city)
                if not weather:
                    flash(f"Could not find weather for '{city}'.", "warning")
            except Exception:
                flash("Failed to fetch weather data. Please try again.", "danger")
        return render_template("home.html",weather=weather, today=weather["days"][0] if weather else None)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data.strip().lower()
            existing = User.query.filter_by(username=username).first()

            if existing:
                form.username.errors.append("✖ Username already taken. Please choose another.")
                return render_template("register.html", form=form)

            user = User(name=form.name.data.strip(), username=username)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("✔ Account created! Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html", form=form)

    # User Login
    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data.strip().lower()
            user = User.query.filter_by(username=username).first()

            if not user:
                form.username.errors.append("✖ Username not found.")
            elif not user.check_password(form.password.data):
                form.password.errors.append("✖ Incorrect password.")

            if form.username.errors or form.password.errors:
                return render_template("login.html", form=form)

            # Successful login
            session.clear()
            session["username"] = user.username
            session["user_id"] = user.id
            session["answered_count"] = session.get("answered_count", 0)
            flash("✔ Logged in successfully.", "success")
            return redirect(url_for("home"))

        return render_template("login.html", form=form)

    # User Logout
    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out.", "info")
        return redirect(url_for("home"))

    # Quiz page
    @app.route("/quiz", methods=["GET", "POST"])
    def quiz():
        user = User.query.get(session["user_id"])
        if not user:
            flash("User account not found. Please log in again.", "danger")
            return redirect(url_for("login"))
        
        # Handle answer submission
        if request.method == "POST":
            # Get selected option index from form
            selected = request.form.get("selected")
            qdata = session.get("current_question")
            if not qdata:
                flash("No question in session. Please try again.", "warning")
                return redirect(url_for("quiz"))

            try:
                selected_idx = int(selected)
            except:
                selected_idx = None

            correct_idx = int(qdata.get("correct"))
            # Update score if correct
            if selected_idx is not None and selected_idx == correct_idx:
                user.score += 10

            db.session.commit()  # persist score immediately
            session["answered_count"] = session.get("answered_count", 0) + 1
            flash("Answer submitted — score updated!", "info")
            return redirect(url_for("quiz"))

        # GET: provide a new random question
        q = get_random_question()
        session["current_question"] = {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "correct": q["correct"]
        }
        
        # Calculate progress (not useed questions tracking for simplicity)
        answered = session.get("answered_count", 0)
        total_q = total_questions() or 1
        progress_percent = ((answered % total_q) / total_q) * 100

        return render_template(
            "quiz.html",
            question=q,
            score=user.score,
            progress=int(progress_percent),
            total_questions=total_q
        )
    
    # Leaderboard page
    @app.route("/leaderboard")
    def leaderboard():
        users = User.query.order_by(User.score.desc(), User.created_at.asc()).limit(100).all()
        return render_template("leaderboard.html", users=users)

    # small API to fetch current logged-in user info (useful for AJAX)
    @app.route("/api/me")
    def api_me():
        if not session.get("user_id"):
            return jsonify({"logged_in": False})
        user = User.query.get(session["user_id"])
        if not user:
            return jsonify({"logged_in": False})
        return jsonify({"logged_in": True, "username": user.username, "score": user.score})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

