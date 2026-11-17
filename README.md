# scanner-blocklist

Addresses and rules for blocking bots that hunt for secret files on websites: `.env`, `.git/config`, cloud keys, database dumps. Many of them pretend to be Googlebot or another well-known crawler.

Everything here was seen on sites we run. Nothing is copied from other lists. Maintained by [Nuvyr](https://nuvyr.com).

## Files

- `ips.txt`: addresses seen scanning, one per line. Lines starting with `#` are notes and give the date and what was seen.
- `cloudflare/fake-crawler.txt`: a Cloudflare custom rule expression. It matches a request that calls itself a known crawler (Googlebot, Bingbot, ClaudeBot, GPTBot and others) but that Cloudflare has not confirmed. Real crawlers are confirmed, so search indexing is not affected.
- `cloudflare/scanner-paths.txt`: a Cloudflare custom rule expression for paths that only scanners ask for. Check it against your own site first. It blocks every path that starts with `/.` (except `/.well-known/`) and every path ending in `.php`.

## Use with Cloudflare

Add each rule under Security → WAF → Custom rules with the action **Block**. Put them before any rule that allows or skips traffic.

To block the addresses, turn `ips.txt` into a rule expression:

```sh
curl -s https://raw.githubusercontent.com/pixexid/scanner-blocklist/main/ips.txt \
  | grep -v '^#' | paste -sd' ' - | sed 's/.*/ip.src in {&}/'
```

The list also works anywhere else that reads one address per line.

## Removal

Cloud servers change hands, so an address can end up with someone innocent. Addresses not seen scanning again within 90 days are removed. If you hold one of these addresses and want it off the list, open an issue.

## License

CC0. Use it however you like.
