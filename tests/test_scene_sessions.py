import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "app.py"


class SceneSessionTests(unittest.TestCase):
    def test_levels_register_scene_in_each_runtime(self):
        for level_id in ("kitchen_01", "study_room_01", "water_garden_01"):
            with self.subTest(level=level_id):
                app = AppTest.from_file(str(APP), default_timeout=30)
                app.query_params = {"view": "level", "level": level_id}
                app.run()
                self.assertEqual(len(app.exception), 0)
                app.run()
                self.assertEqual(len(app.exception), 0)

    def test_kitchen_play_and_hint(self):
        app = AppTest.from_file(str(APP), default_timeout=30)
        app.query_params = {"view": "level", "level": "kitchen_01"}
        app.run()
        next(button for button in app.button if button.label == "Play scene").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn("jumping_cat", app.session_state.scene_finished_objects)
        self.assertIn("falling_box", app.session_state.scene_finished_objects)
        app.session_state.selected_object = "falling_box"
        app.run()
        next(button for button in app.button if button.label == "Replay animation").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state.scene_animation_target, "falling_box")
        self.assertIn("jumping_cat", app.session_state.scene_finished_objects)
        app.session_state.selected_object = "jumping_cat"
        app.run()
        next(button for button in app.button if button.label == "Hint").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state.hints_used, 1)


if __name__ == "__main__":
    unittest.main()
