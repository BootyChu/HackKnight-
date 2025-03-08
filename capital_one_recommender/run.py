import logging
from app import create_app

#Create Flask app
app = create_app()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)  #Runs with debugging enabled