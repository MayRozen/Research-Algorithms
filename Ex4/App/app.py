import dotenv, os
dotenv.load_dotenv()  # load FLASK_RUN_PORT

from App.flaskApp import app
app.run(debug=True, port=os.getenv("FLASK_RUN_PORT", 5000))

# SEE https://csariel.xyz/how-to/service

