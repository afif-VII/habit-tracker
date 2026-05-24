import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv(".env")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "time": self.time,
            "completed": self.completed
        }

@app.route("/")
def home():
    return {
        "message": "Habit Tracker API is running"
    }

@app.route("/habits", methods=["GET"])
def get_habits():
    habits = Habit.query.all()
    
    return {
        "habits": [habit.to_dict() for habit in habits]
    }

@app.route("/habits", methods=["POST"])
def create_habit():
    data = request.get_json()

    new_habit = Habit(
        name=data["name"],
        time=data["time"]
    )

    db.session.add(new_habit)
    db.session.commit()

    return new_habit.to_dict(), 201

@app.route("/habits/<int:habit_id>", methods=["DELETE"])
def delete_habit(habit_id):

    habit = Habit.query.get(habit_id)

    if not habit:
        return {
            "error": "Habit not found"
        }, 404

    db.session.delete(habit)
    db.session.commit()

    return {
        "message": "Habit deleted",
        "habit": habit.to_dict()
    }

@app.route("/habits/<int:habit_id>", methods=["PUT"])
def update_habit(habit_id):
    data = request.get_json()

    habit = Habit.query.get(habit_id)

    if not habit:
        return {
            "error": "Habit not found"
        }, 404
    
    habit.name = data.get("name", habit.name)
    habit.time = data.get("time", habit.time)
    habit.completed = data.get("completed", habit.completed)

    db.session.commit()

    return {
        "message": "Habit updated",
        "habit": habit.to_dict()
    }

if __name__ == "__main__":
    app.run(debug=True)