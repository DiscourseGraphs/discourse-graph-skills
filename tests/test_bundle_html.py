"""Focused portability and caller-contract tests; synthetic fragments only."""
import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / 'plugins/discourse-graph/skills/create-standalone-html'
sys.path.insert(0, str(SKILL / 'scripts'))
from bundle_html import build


class DocumentInfo(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='html-bundle-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = {'title': 'A < B & C', 'overview': 'overview.html', 'content': 'content.html',
                       'nav': [{'label': 'How', 'target': '#how'}], 'search': True}
        (self.root / 'overview.html').write_text('<h2>Overview</h2><a href="https://example.test/source">Source</a>', encoding='utf-8')
        self.set_content('<details id="how" data-level="group"><summary>How</summary><details id="step" data-level="card" data-search-item><summary>Step</summary><p>A useful detail.</p></details></details>')

    def set_content(self, value):
        (self.root / 'content.html').write_text(value, encoding='utf-8')

    def config_path(self):
        target = self.root / 'page.json'
        target.write_text(json.dumps(self.config), encoding='utf-8')
        return target

    def test_single_document_embeds_assets_and_license_keeps_reference(self):
        document = build(self.config_path())
        info = DocumentInfo()
        info.feed(document)
        self.assertTrue(document.startswith('<!doctype html>'))
        self.assertIn('<title>A &lt; B &amp; C</title>', document)
        self.assertIn('The MIT License (MIT)', document)
        self.assertIn('@primer/primitives 11.10.0', document)
        self.assertIn('starter 1.0.0', document)
        self.assertTrue(any(tag == 'a' and attrs.get('href') == 'https://example.test/source' for tag, attrs in info.tags))
        self.assertTrue(any(tag == 'meta' and attrs.get('http-equiv') == 'Content-Security-Policy' and "connect-src 'none'" in attrs['content'] for tag, attrs in info.tags))
        self.assertFalse(any(tag in {'link', 'iframe'} or (tag == 'script' and 'src' in attrs) for tag, attrs in info.tags))
        self.assertFalse(any(tag == 'details' and 'open' in attrs for tag, attrs in info.tags))

    def test_remote_runtime_dependencies_are_rejected(self):
        for markup in ['<img src="https://example.test/x.png">', '<script src="https://example.test/x.js"></script>', '<svg><image href="https://example.test/x.svg"/></svg>', '<div style="background:url(https://example.test/x)"></div>', '<button onclick="fetch(\'https://example.test/x\')">Go</button>']:
            with self.subTest(markup=markup):
                self.set_content(markup)
                with self.assertRaises(ValueError):
                    build(self.config_path())

    def test_embedded_visual_and_local_svg_reference_are_accepted(self):
        self.config['nav'] = []
        self.set_content('<img alt="Dot" src="data:image/svg+xml,%3Csvg/%3E"><svg><defs><path id="arrow" d="M0 0"/></defs><use href="#arrow"/></svg>')
        self.assertIn('data:image/svg+xml', build(self.config_path()))

    def test_extra_css_offline_and_import_rejected(self):
        self.config['extra_css'] = 'page.css'
        stylesheet = self.root / 'page.css'
        stylesheet.write_text('.flow { gap: 20px; }', encoding='utf-8')
        self.assertIn('.flow { gap: 20px; }', build(self.config_path()))
        stylesheet.write_text('@import "https://example.test/styles.css";', encoding='utf-8')
        with self.assertRaises(ValueError):
            build(self.config_path())

    def test_duplicate_ids_and_missing_navigation_fail(self):
        self.set_content('<div id="how"></div><div id="how"></div>')
        with self.assertRaises(ValueError):
            build(self.config_path())
        self.set_content('<div id="other"></div>')
        with self.assertRaises(ValueError):
            build(self.config_path())

    def test_options_do_not_insert_unrequested_ui(self):
        self.config.update(search=False, theme=False, disclosure_controls=False)
        document = build(self.config_path())
        info = DocumentInfo()
        info.feed(document)
        self.assertFalse(any(attrs.get('id') in {'page-search', 'theme-toggle'} or 'data-disclose' in attrs for _, attrs in info.tags))

    def test_existing_output_requires_explicit_force(self):
        output = self.root / 'result.html'
        output.write_text('Keep me', encoding='utf-8')
        command = [sys.executable, '-B', str(SKILL / 'scripts' / 'bundle_html.py'), '--config', str(self.config_path()), '--output', str(output)]
        rejected = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertEqual(output.read_text(encoding='utf-8'), 'Keep me')
        accepted = subprocess.run(command + ['--force'], capture_output=True, text=True)
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        self.assertIn('<!doctype html>', output.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
