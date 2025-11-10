import pytest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ACEest_Fitness import FitnessTrackerApp

def test_add_workout():
    # Mock Tk and the Entry widgets
    mock_root = MagicMock()
    mock_workout_entry = MagicMock()
    mock_duration_entry = MagicMock()

    app = FitnessTrackerApp(mock_root)
    app.workout_entry = mock_workout_entry
    app.duration_entry = mock_duration_entry

    mock_workout_entry.get.return_value = "Push Ups"
    mock_duration_entry.get.return_value = "20"

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        app.add_workout()
        mock_showinfo.assert_called_once_with("Success", "'Push Ups' added successfully!")

    workouts = app.get_workouts()
    assert len(workouts) == 1
    assert workouts[0]["workout"] == "Push Ups"
    assert workouts[0]["duration"] == 20
