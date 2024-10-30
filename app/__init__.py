from flask import Flask
from .config import Config
import asyncio
from .routes import UserRoutes
from .userSession import UserSystem
from .config import Config
from flask_session import Session



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Session(app)

    user_system = UserSystem()
    user_routes = UserRoutes(user_system)

    app.register_blueprint(user_routes.bp)

    # Use asyncio to run the init_data function
    async def init(file_path):
        await user_routes.init_data(file_path)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init(Config.DEFAULT_FILE_JSON))
    loop.close()

    return app

