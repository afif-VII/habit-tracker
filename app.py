from flask import Flask, request

app = Flask(__name__)

habits = [
            {
                "id": 1,
                "name": "Reading",
                "time": "1 hour a day",
            },
            {
                "id": 2,
                "name": "Gym",
                "time": "1 hour a day",
            }
        ]

@app.route("/")
def home():
    return {
        "message": "Habit Tracker API is running"
    }

@app.route("/habits", methods=["GET"])
def get_habits():
    return {
        "habits": habits
    }

@app.route("/habits", methods=["POST"])
def create_habits():
    data = request.get_json()

    new_habit = {
        "id": len(habits) + 1,
        "name": data["name"],
        "time": data["time"]
    }

    habits.append(new_habit)
    return new_habit, 201

if __name__ == "__main__":
    app.run(debug=True)