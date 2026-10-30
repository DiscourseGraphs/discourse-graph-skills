#!/usr/bin/env python3
"""Bundle the pinned starter and authored fragments into one offline HTML file."""
import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
RESERVED_IDS = {'main', 'overview', 'content', 'ui-status', 'theme-toggle', 'page-search',
                'search-controls', 'search-status', 'clear-search'}


def check_css(source):
    if re.search(r'@import\b|</style', source, re.I):
        raise ValueError('CSS imports and closing style tags are unsupported in offline output')
    for match in re.finditer(r'url\(\s*([\'"]?)(.*?)\1\s*\)', source, re.I | re.S):
        if not match[2].strip().startswith(('data:', '#')):
            raise ValueError('CSS resource URLs must be embedded data: URLs or local fragments')


class FragmentCheck(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set(RESERVED_IDS)
        self.levels = set()
        self.tab_targets = []
        self.in_style = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag in {'script', 'base', 'link', 'iframe', 'object', 'embed'}:
            raise ValueError(f'Unsupported runtime dependency tag: {tag}')
        if any(name.lower().startswith('on') for name in attrs):
            raise ValueError('Use the starter controllers; inline event handlers are unsupported')
        if 'srcset' in attrs or 'ping' in attrs:
            raise ValueError('srcset and link ping are unsupported; embed a single resource')
        for name in ('src', 'poster', 'background'):
            if name in attrs and not (attrs[name] or '').startswith('data:'):
                raise ValueError(f'{name} must be an embedded data: URL')
        for name in ('href', 'xlink:href'):
            if name not in attrs:
                continue
            value = attrs[name] or ''
            if tag == 'a':
                if not value.startswith(('#', 'https://', 'http://', 'mailto:')):
                    raise ValueError('Links must be local anchors or explicit reference URLs')
            elif not value.startswith(('#', 'data:')):
                raise ValueError('Non-link references must be embedded or local fragments')
        if 'action' in attrs or 'formaction' in attrs:
            raise ValueError('Offline forms must not submit; use labeled local inputs')
        if 'style' in attrs:
            check_css(attrs['style'] or '')
        if 'id' in attrs:
            identifier = attrs['id']
            if not identifier or identifier in self.ids:
                raise ValueError(f'Duplicate or reserved id: {identifier}')
            self.ids.add(identifier)
        if tag == 'details' and 'data-level' in attrs:
            if attrs['data-level'] not in ('group', 'card'):
                raise ValueError('Disclosure levels must be group or card')
            self.levels.add(attrs['data-level'])
        if attrs.get('role') == 'tab':
            self.tab_targets.append(attrs.get('aria-controls'))
        self.in_style = tag == 'style' or self.in_style

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            check_css(data)


def build(config_path):
    config_path = Path(config_path).resolve()
    config = json.loads(config_path.read_text(encoding='utf-8-sig'))
    allowed = {'title', 'subtitle', 'overview', 'content', 'nav', 'search', 'theme',
               'disclosure_controls', 'extra_css'}
    if not isinstance(config, dict) or set(config) - allowed:
        raise ValueError('Config must be an object containing only documented fields')
    for key in ('title', 'overview', 'content'):
        if not isinstance(config.get(key), str) or not config[key].strip():
            raise ValueError(f'{key} must be a nonempty string')
    if not isinstance(config.get('subtitle', ''), str):
        raise ValueError('subtitle must be text')
    for key in ('search', 'theme', 'disclosure_controls'):
        if key in config and not isinstance(config[key], bool):
            raise ValueError(f'{key} must be true or false')

    def fragment(key):
        return (config_path.parent / config[key]).read_text(encoding='utf-8-sig')

    overview, content = fragment('overview'), fragment('content')
    checked = FragmentCheck()
    checked.feed(overview)
    checked.feed(content)
    checked.close()
    if any(target not in checked.ids for target in checked.tab_targets):
        raise ValueError('Every tab must reference an existing panel id')
    nav = config.get('nav', [])
    if not isinstance(nav, list):
        raise ValueError('nav must be an array of label/target objects')
    nav_links = []
    for item in nav:
        if not isinstance(item, dict) or set(item) != {'label', 'target'}:
            raise ValueError('Each navigation item needs only label and target')
        if not isinstance(item['label'], str) or not item['label'].strip():
            raise ValueError('Navigation labels must be nonempty text')
        target = item['target']
        if not isinstance(target, str) or not re.fullmatch(r'#[A-Za-z][A-Za-z0-9_-]*', target) or target[1:] not in checked.ids:
            raise ValueError(f'Navigation target must name an existing local id: {target}')
        nav_links.append(f'<a href="{html.escape(target, quote=True)}">{html.escape(item["label"])}</a>')

    css = '\n'.join((ASSETS / name).read_text(encoding='utf-8') for name in ('primer-tokens.css', 'ui.css'))
    if config.get('extra_css'):
        if not isinstance(config['extra_css'], str):
            raise ValueError('extra_css must be a stylesheet path')
        css += '\n' + fragment('extra_css')
    check_css(css)
    license_text = (ASSETS / 'primer-LICENSE.txt').read_text(encoding='utf-8')
    css = f'/* Third-party license retained in this standalone file:\n{license_text}\n*/\n{css}'
    provenance = json.loads((ASSETS / 'provenance.json').read_text(encoding='utf-8'))
    search = '''<div id="search-controls" class="toolbar search-bar" hidden>
<label for="page-search">Search this page</label><input id="page-search" type="search" autocomplete="off" aria-describedby="search-status">
<button id="clear-search" type="button">Clear search</button><span id="search-status" class="search-status" role="status" aria-live="polite"></span></div>''' if config.get('search', False) else ''
    control_sets = []
    if config.get('disclosure_controls', True):
        for level, label in (('group', 'groups'), ('card', 'cards')):
            if level in checked.levels:
                control_sets.append(f'<div class="control-set" role="group" aria-label="{label.capitalize()}"><button type="button" data-disclose="{level}" data-open="true" hidden>Expand {label}</button><button type="button" data-disclose="{level}" data-open="false" hidden>Collapse {label}</button></div>')
    controls = '<div class="toolbar disclosure-controls" data-disclosure-controls hidden>' + ''.join(control_sets) + '</div>' if control_sets else ''
    replacements = {
        'TITLE': html.escape(config['title']),
        'SUBTITLE': '<p>' + html.escape(config['subtitle']) + '</p>' if config.get('subtitle') else '',
        'OVERVIEW': overview, 'CONTENT': content, 'CSS': css,
        'JS': (ASSETS / 'ui.js').read_text(encoding='utf-8'),
        'NAV': '<nav class="page-nav" aria-label="Page sections">' + ''.join(nav_links) + '</nav>' if nav_links else '',
        'SEARCH': search, 'CONTROLS': controls,
        'THEME_BUTTON': '<button id="theme-toggle" type="button" aria-pressed="false" hidden>Dark mode</button>' if config.get('theme', True) else '',
        'PROVENANCE': f'create-standalone-html starter {provenance["starter_version"]}; Primer {provenance["primer_primitives"]}',
    }
    shell = (ASSETS / 'shell.html').read_text(encoding='utf-8')
    # One substitution pass leaves similarly shaped text in user content untouched.
    return re.sub(r'\{\{([A-Z_]+)\}\}', lambda match: replacements[match[1]], shell)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--force', action='store_true', help='Replace the selected existing output')
    args = parser.parse_args()
    try:
        document = build(args.config)
        with args.output.open('w' if args.force else 'x', encoding='utf-8', newline='\n') as stream:
            stream.write(document)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f'Cannot bundle HTML: {error}\n')
    print(args.output.resolve())


if __name__ == '__main__':
    main()
