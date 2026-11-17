import copy
import unittest
from datetime import timedelta

from build import build, utc


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.now = utc('2026-11-17T12:00:00Z')
        self.row = dict(ip='192.0.2.1', behaviour='secret_files',
                        first_seen='2026-11-15T12:00:00Z', last_seen='2026-11-15T12:00:00Z', requests=3)

    def test_expiry_boundary(self):
        self.assertEqual(build([self.row], self.now)['entries'], [])
        self.assertEqual(len(build([self.row], self.now - timedelta(seconds=1))['entries']), 1)

    def test_only_new_sighting_renews(self):
        newer = dict(self.row, first_seen='2026-11-16T12:00:00Z', last_seen='2026-11-16T12:00:00Z')
        self.assertEqual(build([self.row, self.row], self.now)['entries'], [])
        entry = build([self.row, newer], self.now)['entries'][0]
        self.assertEqual(entry['expires_at'], '2026-11-18T12:00:00Z')
        self.assertEqual(entry['requests'], 6)

    def test_invalid_input(self):
        for changes in (dict(ip='bad'), dict(behaviour='other'), dict(first_seen='2026-11-18T00:00:00Z'),
                        dict(last_seen='2026-11-18T00:00:00Z'), dict(last_seen='2026-11-15T12:00:00+00:00'),
                        dict(requests=-1)):
            with self.subTest(changes=changes), self.assertRaises((ValueError, KeyError)):
                build([dict(self.row, **changes)], self.now)

    def test_ipv6_and_determinism(self):
        rows = [dict(self.row, ip='2001:db8::1', last_seen='2026-11-16T12:00:00Z'),
                dict(self.row, last_seen='2026-11-16T12:00:00Z', behaviour='webshell_probe')]
        result = build(rows, self.now)
        self.assertEqual(result, build(list(reversed(copy.deepcopy(rows))), self.now))
        self.assertEqual([e['ip'] for e in result['entries']], ['192.0.2.1', '2001:db8::1'])


if __name__ == '__main__':
    unittest.main()
