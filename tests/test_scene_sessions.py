import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

from game.level_loader import load_level
from game.validators import validate_answer


APP = Path(__file__).resolve().parents[1] / "app.py"


class SceneSessionTests(unittest.TestCase):
    def test_results_keep_answers_in_complete_explanation(self):
        level = load_level("kitchen_01")
        target = level["objects"][0]
        for correct in (False, True):
            with self.subTest(correct=correct):
                app = AppTest.from_file(str(APP), default_timeout=30)
                app.session_state.last_result = validate_answer(
                    level, target["id"],
                    target["processes"] if correct else [],
                    target["formula_ids"] if correct else [],
                    attempts=1, hint_used=False,
                )
                app.switch_page("pages/results.py").run()
                self.assertEqual(len(app.exception), 0)
                explanation = next(
                    item for item in app.expander if item.label == "Show complete explanation"
                )
                for answer in ("Correct formulas:", 'class="formula-note-grid"', target["explanation"]):
                    self.assertEqual(sum(answer in item.value for item in app.markdown), 1)
                    self.assertTrue(any(answer in item.value for item in explanation.markdown))

    def test_levels_register_scene_in_each_runtime(self):
        for level_id in ("kitchen_01", "study_room_01"):
            with self.subTest(level=level_id):
                app = AppTest.from_file(str(APP), default_timeout=30)
                app.query_params = {"view": "level", "level": level_id}
                app.run()
                self.assertEqual(len(app.exception), 0)
                app.run()
                self.assertEqual(len(app.exception), 0)

    def test_removed_level_link_falls_back_to_kitchen(self):
        app = AppTest.from_file(str(APP), default_timeout=30)
        app.query_params = {"view": "level", "level": "water_garden_01"}
        app.run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state.current_level, "kitchen_01")
        self.assertFalse(any("Water Garden" in button.label for button in app.sidebar.button))

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
