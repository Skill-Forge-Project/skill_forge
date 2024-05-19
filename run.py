import os
from dotenv import load_dotenv
from app import create_app


load_dotenv

app = create_app()

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    debug_port = os.getenv("DEBUG_PORT", 5000)  # Set default port to 5000 if DEBUG_PORT is not set
    app.run(debug=True, host='0.0.0.0', port=int(debug_port))