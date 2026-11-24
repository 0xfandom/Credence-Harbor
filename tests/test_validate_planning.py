import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_planning import validate_repository  # noqa: E402


class PlanningValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "planning").mkdir()
        (self.root / "docs").mkdir()
        (self.root / "docs" / "overview.md").write_text("Overview\n", encoding="utf-8")
        (self.root / "README.md").write_text(
            "[Overview](docs/overview.md) [Section](#section)\n", encoding="utf-8"
        )
        gates = ["G0", "G1", "G2", "G3", "G4a", "G4b", "G4", "POST_G4", "G5", "NEW_GATES"]
        self.milestones = [
            {
                "id": f"M{number}",
                "start_week": str(number + 1),
                "end_week": str(number + 2),
                "title": f"Milestone {number}",
                "gate": gates[number],
                "owner": "Team",
                "exit_criterion": "Documented",
            }
            for number in range(10)
        ]
        self.backlog = [
            {
                "id": "TASK-001",
                "milestone": "M0",
                "discipline": "Docs",
                "title": "First task",
                "depends_on": "",
                "gate": "G0",
                "definition_of_done": "Complete",
            },
            {
                "id": "TASK-002",
                "milestone": "M1",
                "discipline": "Docs",
                "title": "Second task",
                "depends_on": "TASK-001",
                "gate": "G1",
                "definition_of_done": "Complete",
            },
        ]
        self._write_csv("planning/milestones_506c.csv", self.milestones)
        self._write_csv("planning/backlog_506c.csv", self.backlog)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_csv(self, relative_path, rows):
        path = self.root / relative_path
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    def _errors(self):
        errors, _ = validate_repository(self.root)
        return "\n".join(errors)

    def test_valid_planning_files_pass(self):
        errors, summary = validate_repository(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(summary["milestones"], 10)
        self.assertEqual(summary["backlog_items"], 2)
        self.assertEqual(summary["readme_relative_links"], 1)

    def test_milestones_must_follow_m0_to_m9_order(self):
        self.milestones[0], self.milestones[1] = self.milestones[1], self.milestones[0]
        self._write_csv("planning/milestones_506c.csv", self.milestones)
        self.assertIn("expected row order M0-M9", self._errors())

    def test_unknown_milestone_gate_fails(self):
        self.milestones[0]["gate"] = "G6"
        self._write_csv("planning/milestones_506c.csv", self.milestones)
        self.assertIn("unknown gate 'G6'", self._errors())

    def test_unknown_backlog_gate_fails(self):
        self.backlog[0]["gate"] = "G6"
        self._write_csv("planning/backlog_506c.csv", self.backlog)
        self.assertIn("unknown gate 'G6'", self._errors())

    def test_backlog_gate_must_match_milestone(self):
        self.backlog[0]["gate"] = "G1"
        self._write_csv("planning/backlog_506c.csv", self.backlog)
        self.assertIn("does not match milestone 'M0' gate 'G0'", self._errors())

    def test_duplicate_backlog_id_fails(self):
        self.backlog[1]["id"] = self.backlog[0]["id"]
        self._write_csv("planning/backlog_506c.csv", self.backlog)
        self.assertIn("duplicate id", self._errors())

    def test_unknown_dependency_fails(self):
        self.backlog[1]["depends_on"] = "MISSING"
        self._write_csv("planning/backlog_506c.csv", self.backlog)
        self.assertIn("unknown dependency", self._errors())

    def test_dependency_cycle_fails(self):
        self.backlog[0]["depends_on"] = "TASK-002"
        self._write_csv("planning/backlog_506c.csv", self.backlog)
        self.assertIn("dependency cycle", self._errors())

    def test_broken_readme_link_fails(self):
        (self.root / "README.md").write_text("[Missing](docs/missing.md)\n", encoding="utf-8")
        self.assertIn("relative link target does not exist", self._errors())

    def test_invalid_milestone_week_range_fails(self):
        self.milestones[0]["end_week"] = "0"
        self._write_csv("planning/milestones_506c.csv", self.milestones)
        self.assertIn("positive week range", self._errors())


if __name__ == "__main__":
    unittest.main()
