# Running the server

import dotenv, os
dotenv.load_dotenv()  # load FLASK_RUN_PORT

from flaskApp import app
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("FLASK_RUN_PORT"), host='0.0.0.0')


    