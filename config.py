from dotenv import load_dotenv
import os

load_dotenv()  # this is a better practice, it takes environment variables from .env.


# Environment variables
class Config:  # BaseSettings reads variables itself without the need to use 'environ.get',
    # the name must match what it would look for. The second value in get() is the default if it's not in .env
    APP_NAME = os.environ.get("APP_NAME", "PyGame")
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 400
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "database.sqlite"
    )  # This creates a database locally in project files
