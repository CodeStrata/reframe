"""P1-06 (#235): the design site renderer for any canonical design, on three different synthetic samples. L1, L2.

FR-10 acceptance on every sample: every map is covered by a page, every
journey clicks through, and a batch-only function and a message exchange are
modelled without invented screens or REST endpoints.
"""

import copy
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

import reframe_v2.design_site as design_site
from reframe_v2.design_site import Feedback, RenderError, SiteInput, load_sample, render, slug

SAMPLES = Path(__file__).resolve().parents[1] / "examples" / "designs"
NAMES = ("online-preserve", "online-modernize", "batch-only", "message-exchange")


def sample(name, feedback=None):
    return load_sample(str(SAMPLES / f"{name}.json"), feedback)


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.anchors, self.tags = set(), [], set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if "data-reframe-id" in attrs:
            self.ids.add(attrs["data-reframe-id"])
        if "href" in attrs:
            self.hrefs.append(attrs["href"])
        if "id" in attrs:
            self.anchors.add(attrs["id"])


def parse(files):
    parsed = {}
    for name, data in files.items():
        collector = Collector()
        collector.feed(data.decode())
        parsed[name] = collector
    return parsed


class RenderEverySampleTests(unittest.TestCase):
    def test_every_behavioural_element_carries_its_id(self):
        for name in NAMES:
            with self.subTest(sample=name):
                site = sample(name)
                parsed = parse(render(site))
                ids = set().union(*(p.ids for p in parsed.values()))
                design = site.design
                expected = {p["id"] for p in design["pages"]} | {i["id"] for i in design["interactions"]}
                expected |= {f["id"] for p in design["pages"] for f in p["fields"]}
                expected |= {a["id"] for p in design["pages"] for a in p["actions"]}
                expected |= set(site.rules)
                self.assertEqual(expected - ids, set())

    def test_every_local_link_resolves(self):
        for name in NAMES:
            with self.subTest(sample=name):
                files = render(sample(name))
                parsed = parse(files)
                for page, collector in parsed.items():
                    for href in collector.hrefs:
                        if href.startswith("https://github.com/"):
                            continue
                        target, _, anchor = href.partition("#")
                        target = target or page
                        self.assertIn(target, files, f"{page} links to missing {href}")
                        if anchor:
                            self.assertIn(anchor, parsed[target].anchors, f"{page} links to missing anchor {href}")

    def test_no_scripts_or_external_resources(self):
        for name in NAMES:
            for text in (d.decode() for d in render(sample(name)).values()):
                self.assertNotIn("<script", text.lower())
                self.assertIsNone(re.search(r'(src|href)="(?!https://github\.com/)(https?:)?//', text))

    def test_rendering_is_deterministic(self):
        for name in NAMES:
            self.assertEqual(render(sample(name)), render(sample(name)))

    def test_input_text_is_escaped(self):
        site = sample("online-preserve")
        design = copy.deepcopy(site.design)
        design["pages"][0]["name"] = '<script>alert("x")</script>'
        out = render(SiteInput(design, site.rules, site.feedback, label='<img src=x onerror=alert(1)>'))
        text = b"".join(out.values()).decode()
        self.assertNotIn("<script>alert", text)
        self.assertNotIn("<img", text)


class GoalTests(unittest.TestCase):
    def test_preserve_has_one_page_per_map_with_its_keys(self):
        site = sample("online-preserve")
        files = render(site)
        maps = {m for p in site.design["pages"] for m in p["replaces_maps"]}
        self.assertEqual(len(site.design["pages"]), len(maps))
        page = files["page-page-poladr1.html"].decode()
        self.assertIn("3270 map: POLADR1", page)
        self.assertIn('<span class="key">PF3</span>', page)

    def test_modernize_lists_replaced_maps_and_loses_no_field_or_rule(self):
        preserve, modernize = sample("online-preserve"), sample("online-modernize")
        fields = lambda d: {f["id"] for p in d["pages"] for f in p["fields"]}
        rules = lambda d: {r for p in d["pages"] for r in p["rules_applied"] + [x for f in p["fields"] for x in f["rules"]]}
        self.assertEqual(fields(preserve.design), fields(modernize.design))
        self.assertEqual(rules(preserve.design), rules(modernize.design))
        page = render(modernize)["page-page-update-address.html"].decode()
        self.assertIn("Task page. Replaces maps: POLADR1, POLADR2", page)

    def test_every_map_is_covered_by_a_page(self):
        preserve, modernize = sample("online-preserve"), sample("online-modernize")
        maps = {m for p in preserve.design["pages"] for m in p["replaces_maps"]}
        self.assertEqual(maps, {m for p in modernize.design["pages"] for m in p["replaces_maps"]})

    def test_every_journey_clicks_through(self):
        site = sample("online-preserve")
        files = render(site)
        for journey in site.design["journeys"]:
            for page in journey["pages"]:
                self.assertIn(f"page-{slug(page)}.html", files)
        first = files["page-page-poladr1.html"].decode()
        self.assertIn('href="page-page-poladr2.html"', first)


class NoInventedScreensTests(unittest.TestCase):
    def test_batch_only_renders_no_pages_and_no_endpoints(self):
        files = render(sample("batch-only"))
        self.assertEqual(sorted(files), ["index.html", "interactions.html"])
        index = files["index.html"].decode()
        self.assertIn("no screens or endpoints are invented", index)
        self.assertNotIn("OpenAPI contract", files["interactions.html"].decode())

    def test_message_exchange_shows_its_queues_and_only_the_http_call_gets_a_contract(self):
        text = render(sample("message-exchange"))["interactions.html"].decode()
        self.assertIn("PAY.IN (MQ queue)", text)
        self.assertEqual(text.count("OpenAPI contract:"), 1)
        self.assertIn("No source found", text)


class RefusalTests(unittest.TestCase):
    def broken(self, change):
        site = sample("online-preserve")
        design = copy.deepcopy(site.design)
        change(design)
        return SiteInput(design, site.rules, site.feedback)

    def test_unknown_references_are_refused(self):
        changes = [
            lambda d: d["pages"][0]["actions"][0].update(navigates_to="page:missing"),
            lambda d: d["pages"][0]["actions"][0].update(interaction="int:missing"),
            lambda d: d["pages"][0]["rules_applied"].append("rule:missing"),
            lambda d: d["journeys"][0]["pages"].append("page:missing"),
        ]
        for change in changes:
            with self.assertRaises(RenderError):
                render(self.broken(change))

    def test_an_http_interaction_needs_its_contract(self):
        site = sample("message-exchange")
        design = copy.deepcopy(site.design)
        design["interactions"][1]["contract"] = None
        with self.assertRaises(RenderError):
            render(SiteInput(design, site.rules, site.feedback))


class FeedbackTests(unittest.TestCase):
    def test_local_feedback_shows_the_text_and_sends_nothing(self):
        page = render(sample("online-preserve"))["page-page-poladr1.html"].decode()
        self.assertIn("This is exactly what will be sent", page)
        self.assertIn("reframe context add", page)
        self.assertNotIn("github.com", page)

    def test_github_feedback_prefills_an_issue_the_person_submits(self):
        site = sample("online-preserve", Feedback("github", "sample-org/sample-repo"))
        page = render(site)["page-page-poladr1.html"].decode()
        self.assertIn("https://github.com/sample-org/sample-repo/issues/new?title=", page)
        self.assertIn("Nothing is sent until you submit it there", page)

    def test_github_feedback_needs_a_repository(self):
        with self.assertRaises(RenderError):
            render(sample("online-preserve", Feedback("github")))


class GenericCodeTests(unittest.TestCase):
    def test_the_renderer_names_nothing_from_any_application(self):
        source = Path(design_site.__file__).read_text().casefold()
        for word in ("poladr", "intacr", "policy", "payment", "carddemo", "cobil", "bill"):
            self.assertNotIn(word, source)


if __name__ == "__main__":
    unittest.main()
