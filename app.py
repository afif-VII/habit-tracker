from flask import Flask

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

@app.route("/habits")
def get_habits():
    return {
        "habits": habits
    }

if __name__ == "__main__":
    app.run(debug=True)