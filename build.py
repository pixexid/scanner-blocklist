import argparse
import ipaddress
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def utc(value):
    if not isinstance(value, str) or not value.endswith('Z'):
        raise ValueError('timestamp must be ISO UTC ending in Z')
    return datetime.fromisoformat(value[:-1] + '+00:00')


def stamp(value):
    return value.isoformat(timespec='seconds').replace('+00:00', 'Z')


def build(sightings, now):
    groups = {}
    for row in sightings:
        ip = str(ipaddress.ip_address(row['ip']))
        first, last = utc(row['first_seen']), utc(row['last_seen'])
        if first > last or last > now or row['behaviour'] not in ('secret_files', 'webshell_probe'):
            raise ValueError('invalid sighting')
        if type(row['requests']) is not int or row['requests'] < 0:
            raise ValueError('invalid request count')
        group = groups.setdefault(ip, {'last': last, 'behaviours': set(), 'requests': 0})
        group['last'] = max(group['last'], last)
        group['behaviours'].add(row['behaviour'])
        group['requests'] += row['requests']
    entries = [dict(ip=ip, behaviours=sorted(group['behaviours']), last_seen=stamp(group['last']),
                    expires_at=stamp(group['last'] + timedelta(hours=48)), requests=group['requests'])
               for ip, group in sorted(groups.items()) if group['last'] + timedelta(hours=48) > now]
    return {'generated_at': stamp(now), 'ttl_hours': 48, 'entries': entries}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--now', help='UTC timestamp for reproducible builds')
    args = parser.parse_args()
    now = utc(args.now) if args.now else datetime.now(timezone.utc).replace(microsecond=0)
    feed = build(json.loads(Path('sightings.json').read_text()), now)
    Path('feed.json').write_text(json.dumps(feed, indent=2) + '\n')
    header = f"# generated_at: {feed['generated_at']}\n# consumers must reject this file if generated_at is older than 24 hours\n"
    Path('ips.txt').write_text(header + ''.join(entry['ip'] + '\n' for entry in feed['entries']))
    print(f"Built {len(feed['entries'])} entries at {feed['generated_at']}")


if __name__ == '__main__':
    main()
