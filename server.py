from database.database import db, User
from server import app

if __name__ == "__main__":
    db.create_all()
    db.session.add()
    app.run(debug=True,port=8080)