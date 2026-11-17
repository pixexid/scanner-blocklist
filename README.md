# scanner-blocklist

An advisory feed of reviewed first-party sightings from [Nuvyr](https://nuvyr.com). Only Nuvyr's own observations are published. An address expires 48 hours after its last verified attack; only fresh probing renews it. An address may have changed hands, so assess the impact before using the feed to block traffic.

Agents can fetch [feed.json](feed.json). It includes `generated_at`, `ttl_hours`, and each entry's `expires_at`. [ips.txt](ips.txt) contains the same addresses. Reject a feed more than 24 hours old, drop expired entries, and replace your list on every sync; never append to an old list. If updates stop, drop stale data rather than keeping it indefinitely.

`sightings.json` is the hand-maintained input. Run `python3 -m unittest -v` and `python3 build.py` to test and generate the feed. The scheduled build runs every six hours.

## Cloudflare examples

The expressions in `cloudflare/*.txt` are examples to adapt and test against your own traffic. The scanner-paths rule blocks every `.php` path and every `/wp-` path, which breaks WordPress and PHP sites. The fake-crawler rule can block useful unverified bots and may affect indexing. Choose actions appropriate for your site.

## Disputes

Open an issue to dispute an entry. Disputed entries are removed while reviewed.

## License

CC0. See [LICENSE](LICENSE).
