from flask_app import create_app
from flask_app.config import DevelopmentConfig
app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run(debug=True)
