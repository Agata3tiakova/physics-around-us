import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ContentTests(unittest.TestCase):
    def test_levels_have_valid_assets_and_answer_references(self):
        levels = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in (ROOT / "content" / "levels").glob("*.json")
        ]
        formulas = json.loads((ROOT / "content" / "formulas.json").read_text(encoding="utf-8"))
        formula_ids = {item["id"] for item in formulas}
        self.assertEqual(len(formula_ids), len(formulas))
        level_ids = {level["id"] for level in levels}
        used_formulas = set()
        for level in levels:
            with self.subTest(level=level["id"]):
                self.assertTrue((ROOT / "components" / "scene" / level["background"]).is_file())
                available = set(level["formula_ids"])
                self.assertLessEqual(available, formula_ids)
                used_formulas.update(available)
                processes = {item["id"] for item in level["processes"]}
                objects = {item["id"] for item in level["objects"]}
                self.assertEqual(len(objects), len(level["objects"]))
                self.assertLessEqual(set(level.get("animated_object_ids", [])), objects)
                for direction in ("next_level", "previous_level"):
                    if level.get(direction):
                        self.assertIn(level[direction], level_ids)
                for item in level["objects"]:
                    self.assertLessEqual(set(item["formula_ids"]), available)
                    self.assertLessEqual(set(item["processes"]), processes)
        self.assertEqual(used_formulas, formula_ids)


if __name__ == "__main__":
    unittest.main()
