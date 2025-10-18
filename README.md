[LeetQuiz (Kodland)](https://raininmyhead.pythonanywhere.com/)
==================
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<img width="1351" height="638" alt="image" src="https://github.com/user-attachments/assets/80194a5c-09ce-4acb-9199-dae8149548d0" />


Lightweight Flask quiz application with user authentication, a simple leaderboard, and a 3-day weather forecast using the Open-Meteo API.

------------------------------------------------------------
FEATURES
------------------------------------------------------------
- User registration and login (Flask-WTF)
- Per-user score tracking persisted in SQLite (SQLAlchemy)
- Quiz engine with shuffled options (questions in quiz_data.py)
- Leaderboard showing top users
- Home page with 3-day day/night weather summary via Open-Meteo
- Small JSON API endpoint for the logged-in user (/api/me)

------------------------------------------------------------
REQUIREMENTS
------------------------------------------------------------
- Python 3.8+
- Internet access for Open-Meteo geocoding / forecast requests
- requirements.txt file (included in this repository)

------------------------------------------------------------
QUICK SETUP (WINDOWS)
------------------------------------------------------------

1. Create and activate a virtual environment

Powershell:
```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
```

CMD:
```
    python -m venv venv
    venv\Scripts\activate
```

2. Install dependencies
```
    pip install -r requirements.txt
```

3. (Optional) Set a secure secret key for production
```
    setx LEETQUIZ_SECRET "replace-with-a-secure-random-value"
```

5. Run the app
```
    python app.py
```

NOTE:
The app defaults to a development secret if the environment variable is not set.
Replace it before production and disable debug mode.

------------------------------------------------------------
ROUTES / USAGE
------------------------------------------------------------
```
/ (GET)               - Home page (optional query param: city to fetch weather)
/register (GET, POST) - Register a new user
/login (GET, POST)    - Login
/logout (GET)         - Logout
/quiz (GET, POST)     - Take quiz (POST submits answer)
/leaderboard (GET)    - View leaderboard
/api/me (GET)         - JSON with logged-in user info
```

------------------------------------------------------------
PROJECT LAYOUT
------------------------------------------------------------
```
app.py           - Main Flask application and routes
models.py        - SQLAlchemy models (User)
forms.py         - Flask-WTF forms
quiz_data.py     - Question bank and helpers (get_random_question, total_questions)
static/          - CSS and assets (e.g., static/css/style.css)
templates/       - Jinja2 templates (base.html, home.html, quiz.html, etc.)
leetquiz.db      - SQLite database contains users table/schema created after running created after running
```

------------------------------------------------------------
EXTENDING THE QUIZ
------------------------------------------------------------
Edit quiz_data.py to add or modify questions.
Each question must include:
- text: question string
- options: list of strings
- answer: the correct option string

Options are shuffled at runtime, and the correct index is computed dynamically.

------------------------------------------------------------
NOTES & RECOMMENDATIONS
------------------------------------------------------------
- Replace the default SECRET_KEY with a strong random value for production.
- Disable debug mode before deploying and use a WSGI server.
- Open-Meteo calls require network access; handle errors and rate limits if needed.
- The question ID returned from get_random_question() is ephemeral (random int) and not persistent.

------------------------------------------------------------
Website Link
------------------------------------------------------------
https://raininmyhead.pythonanywhere.com/


------------------------------------------------------------
UI Template Reources
------------------------------------------------------------
- [Weather Widget Template](https://codesandbox.io/p/sandbox/weather-app-html-css-n0zy9f?file=%2Findex.html%3A17%2C7)
- [Quiz Box](https://bootstrapexamples.com/@ross-wille/interactive-quiz-application)
- [OpenWeatherMap Icons for weather icons](https://openweathermap.org/weather-conditions)
------------------------------------------------------------
Connect With Me:
------------------------------------------------------------
<a href="https://www.linkedin.com/in/salsabilasyahirah/" target="_blank">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" alt="website icon" width="30"/>
</a>
<a href="https://medium.com/@salsabilasyahirah" target="_blank">
  <img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/medium.svg" alt="website icon" width="30"/>
</a>
<a href="https://www.kaggle.com/sasyablossom" target="_blank">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kaggle/kaggle-original.svg" alt="website icon" width="30"/>
</a>
