#!/usr/bin/env python3
"""Dependency-free checks for the homepage iPhone demo and its release config.

Run normally before release. --allow-local-preview permits an untracked MP4 only
while preparing the site before the production media host has been configured.
"""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.scripts = []
        self.json_script = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.nodes.append((tag, attrs))
        if tag == 'script':
            self.json_script = attrs.get('type') == 'application/ld+json'

    def handle_endtag(self, tag):
        if tag == 'script':
            self.json_script = False

    def handle_data(self, data):
        if self.json_script and data.strip():
            self.scripts.append(json.loads(data))

    def select(self, tag, **attrs):
        return [a for t, a in self.nodes if t == tag and all(a.get(k) == v for k, v in attrs.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-local-preview', action='store_true')
    args = parser.parse_args()
    home = ROOT / 'index.html'
    page = Page(home)
    source = home.read_text()
    ids = [a['id'] for _, a in page.nodes if 'id' in a]
    assert len(ids) == len(set(ids)), 'Duplicate homepage IDs'
    videos = page.select('video')
    assert len(videos) == 1, 'Exactly one demo player is expected'
    video = videos[0]
    assert all(key in video for key in ('controls', 'playsinline'))
    assert not any(key in video for key in ('autoplay', 'loop'))
    assert video['preload'] == 'none'
    assert (video['width'], video['height']) == ('1920', '1080')
    assert video.get('aria-label') and video.get('aria-describedby')
    assert all(ref in ids for ref in video['aria-describedby'].split())
    assert source.count('class="home-section app-section"') == 1
    sections = page.select('section')
    commission = next(i for i, a in enumerate(sections) if a.get('id') == 'commission')
    assert sections[commission + 1].get('id') == 'iphone-demo'
    assert sections[commission + 2].get('class') == 'home-band'
    assert page.select('a', href='#iphone-demo', **{'class': 'home-btn text'})
    assert page.select('a', href='/tools/pay-plan-comparison-calculator/', **{'class': 'home-btn secondary'})
    assert page.select('a', href='/tools/car-salesman-commission-calculator/', **{'class': 'home-btn primary'})
    assert page.select('a', href='/tracker/', **{'class': 'home-btn secondary'})
    assert page.select('a', href='https://apps.apple.com/us/app/carsales-tracker-pro/id6756135308', **{'class': 'home-btn primary'})
    assert 'Commission and spiffs require Advanced or Elite.' in source
    assert 'Sample data; app screenshots and recordings; sequences shortened.' in source
    assert 'not a notification arriving' in source
    poster = ROOT / video['poster'].lstrip('/')
    assert poster.is_file() and poster.stat().st_size < 250_000
    assert poster.read_bytes()[:3] == b'\xff\xd8\xff'
    track, = page.select('track')
    assert track['kind'] == 'captions' and track['srclang'] == 'en'
    captions = (ROOT / track['src'].lstrip('/')).read_text()
    assert captions.startswith('WEBVTT\n')
    cues = re.findall(r'(\d\d):(\d\d)\.(\d{3}) --> (\d\d):(\d\d)\.(\d{3})', captions)
    assert len(cues) == 7
    previous = 0
    for sm, ss, sms, em, es, ems in cues:
        start = int(sm) * 60 + int(ss) + int(sms) / 1000
        end = int(em) * 60 + int(es) + int(ems) / 1000
        assert abs(start - previous) < .001 and start < end <= 37.5
        previous = end
    assert previous == 37.5
    for article in ('tools/car-salesman-commission-calculator/index.html', 'blog/front-end-vs-back-end-gross/index.html'):
        linked_page = Page(ROOT / article)
        assert linked_page.select('a', href='/#iphone-demo'), article
    media, = page.select('source')
    assert media['type'] == 'video/mp4'
    url = urlsplit(media['src'])
    if args.allow_local_preview and media['src'].startswith('/'):
        assert (ROOT / media['src'].lstrip('/')).is_file()
        print('Preview-only media URL: production URL is still required before release.')
    else:
        assert url.scheme == 'https' and url.netloc and url.path.endswith('.mp4'), 'Set the verified HTTPS production MP4 URL before release'
        assert not any(word in media['src'].lower() for word in ('placeholder', 'example.com', 'localhost'))
    tracked_mp4s = subprocess.check_output(['git', 'ls-files', '--', 'assets/demos/*.mp4'], cwd=ROOT, text=True).strip()
    assert not tracked_mp4s, 'Do not commit video binaries to the website repository'
    print('PASS: player, placement, CTAs, plan disclosures, captions, poster, article links, JSON-LD, and media configuration.')


if __name__ == '__main__':
    main()
