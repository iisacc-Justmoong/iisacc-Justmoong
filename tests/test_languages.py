import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

SPEC = importlib.util.spec_from_file_location(
    "update_languages", Path(__file__).resolve().parents[1] / "scripts/update_languages.py")
chart = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(chart)


def repo(number=1, name="example", **changes):
    data = {"id": number, "full_name": f"{chart.OWNER}/{name}",
            "owner": {"login": chart.OWNER}, "private": False,
            "fork": False, "archived": False, "default_branch": "main"}
    data.update(changes)
    return data


class LanguageChartTests(unittest.TestCase):
    def setUp(self):
        self.records = [{"id": 1, "name": f"{chart.OWNER}/example",
                         "archived": True, "default_branch": "main",
                         "languages": {"C++": 800, "Python": 200}}]
        self.data = chart.snapshot(self.records)
        self.data["updated_at"] = "2026-11-09T00:00:00+00:00"

    def test_filter_private_forks_profile_and_other_owners(self):
        repositories = [repo(), repo(2, private=True), repo(3, fork=True),
                        repo(4, chart.OWNER), repo(5, owner={"login": "someone-else"})]
        self.assertEqual([r["id"] for r in chart.eligible(repositories)], [1])

    def test_archives_included_and_duplicate_ids_counted_once(self):
        self.assertEqual(len(chart.eligible([repo(archived=True), repo(archived=True)])), 1)
        self.assertTrue(chart.eligible([repo(archived=True)])[0]["archived"])

    def test_byte_weighting_not_repository_average(self):
        records = self.records + [{**self.records[0], "id": 2, "languages": {"Python": 1000}}]
        result = chart.snapshot(records)
        self.assertEqual(result["total_bytes"], 2000)
        self.assertEqual(result["languages"], {"Python": 1200, "C++": 800})

    def test_empty_total_fails(self):
        with self.assertRaises(ValueError):
            chart.snapshot([])

    def test_other_preserves_all_bytes(self):
        totals = {f"Language {i}": i + 1 for i in range(24)}
        entries = chart.chart_entries(totals)
        self.assertEqual(len(entries), 8)
        self.assertEqual(entries[-1][0], "Other")
        self.assertEqual(sum(size for _, size in entries), sum(totals.values()))

    def test_small_language_set_has_no_other(self):
        self.assertEqual(chart.chart_entries({"C++": 2, "Python": 1}), [("C++", 2), ("Python", 1)])

    def test_svg_xml_themes_percentages_and_exact_bar_width(self):
        ns = {"s": "http://www.w3.org/2000/svg"}
        for dark in (False, True):
            svg = chart.render_svg(self.data, dark)
            tree = ET.fromstring(svg)
            self.assertIn("C++ 80.0%", svg)
            self.assertIn("Python 20.0%", svg)
            self.assertIn("#0d1117" if dark else "#ffffff", svg)
            bars = tree.findall('.//s:g[@clip-path="url(#bar)"]/s:rect', ns)
            self.assertAlmostEqual(sum(float(r.attrib["width"]) for r in bars), 584)

    def test_language_names_are_xml_escaped(self):
        self.data["languages"] = {"<Test & language>": 1000}
        ET.fromstring(chart.render_svg(self.data))
        self.assertIn("&lt;Test &amp; language&gt;", chart.render_svg(self.data))

    def test_unchanged_data_keeps_snapshot_date(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            data = chart.snapshot(self.records)
            chart.save(copy.deepcopy(data), target)
            before = (target / "languages.json").read_text()
            chart.save(copy.deepcopy(data), target)
            self.assertEqual(before, (target / "languages.json").read_text())

    def test_pagination_and_empty_repositories(self):
        page = [repo(i, f"repo-{i}") for i in range(100)]
        responses = [page, [repo(100, "last")]] + [{"C++": 1}] * 100 + [{}]
        with patch.object(chart, "api", side_effect=responses) as api:
            result = chart.collect(chart.OWNER)
        self.assertEqual(result["repository_count"], 101)
        self.assertEqual(result["repositories_with_code"], 100)
        self.assertEqual(result["total_bytes"], 100)
        self.assertIn("page=2", api.call_args_list[1].args[0])

    def test_invalid_language_payload_fails(self):
        with patch.object(chart, "api", side_effect=[[repo()], {"C++": "unknown"}]):
            with self.assertRaises(ValueError):
                chart.collect(chart.OWNER)

    def test_api_failure_does_not_publish_partial_result(self):
        with patch.object(chart, "api", side_effect=[[repo()], RuntimeError("API unavailable")]):
            with self.assertRaises(RuntimeError):
                chart.collect(chart.OWNER)


if __name__ == "__main__":
    unittest.main()
