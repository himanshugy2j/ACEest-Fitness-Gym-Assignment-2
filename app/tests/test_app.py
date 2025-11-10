import tkinter as tk
from ACEest_Fitness import FitnessTrackerApp

def test_add_workout():
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    app.workout_entry.insert(0, "Push Ups")
    app.duration_entry.insert(0, "20")
    app.add_workout()
    workouts = app.get_workouts()
    assert len(workouts) == 1
    assert workouts[0]["workout"] == "Push Ups"
    assert workouts[0]["duration"] == 20
    root.destroy()
