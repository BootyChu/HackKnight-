from flask import Flask, render_template

app = Flask(__name__, static_folder="../static", template_folder="../templates")



@app.route('/')
def home():
    return render_template('index.html')

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


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

if __name__ == "__main__":
    app.run(debug=True)
