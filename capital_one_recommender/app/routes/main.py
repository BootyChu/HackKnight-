from flask import Flask, render_template, Blueprint
from app.utils.models import db
from app.utils.database import init_db
from app.routes.auth import auth

app = Flask(__name__, static_folder="../static", template_folder="../templates")

init_db(app) 

# Register Blueprints
app.register_blueprint(auth, url_prefix="/")  # Register 'auth' Blueprint


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/comparison')
def comparison():
    return render_template('comparison.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
