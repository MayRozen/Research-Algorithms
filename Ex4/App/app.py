import dotenv, os
dotenv.load_dotenv()  # load FLASK_RUN_PORT

from flaskApp import app
app.run(debug=True, port=os.getenv("FLASK_RUN_PORT"))
