#!/usr/bin/env python3
"""Post a single Bluesky (AT Protocol) post with link facets.

Usage:
  python3 scripts/bsky_post.py --text "hello" [--env ../../bluesky-mcp/.env]
Reads BLUESKY_IDENTIFIER + BLUESKY_APP_PASSWORD from the env file or environment.
Prints the created post URI and a JSON receipt to stdout.

No third-party deps.
"""
from __future__ import annotations
import argparse, json, os, re, sys, time, urllib.request, urllib.error

API = "https://bsky.social/xrpc"
URL_RE = re.compile(r"https?://\S+|\b[a-z0-9.-]+\.(?:dev|com|social|org|art)(?:/\S*)?")


def load_env(path):
    if path and os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def post(path, data, token=None):
    req = urllib.request.Request(API + path, data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json", **({"Authorization": "Bearer " + token} if token else {})})
    try:
        return json.load(urllib.request.urlopen(req, timeout=30))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode()[:300]}")


def facets(text):
    out = []
    for m in URL_RE.finditer(text):
        frag = m.group(0)
        start = len(text[:m.start()].encode())
        b = frag.encode()
        uri = frag if frag.startswith("http") else "https://" + frag
        out.append({"index": {"byteStart": start, "byteEnd": start + len(b)},
                    "features": [{"$type": "app.bsky.richtext.facet#link", "uri": uri}]})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--env", default=os.path.expanduser("~/workspace/peterlodri-sec/bluesky-mcp/.env"))
    ap.add_argument("--lang", default="en")
    a = ap.parse_args()
    load_env(a.env)

    ident = os.environ.get("BLUESKY_IDENTIFIER")
    pw = os.environ.get("BLUESKY_APP_PASSWORD")
    if not (ident and pw):
        raise SystemExit("missing BLUESKY_IDENTIFIER / BLUESKY_APP_PASSWORD")

    sess = post("/com.atproto.server.createSession", {"identifier": ident, "password": pw})
    did, token = sess["did"], sess["accessJwt"]

    record = {"$type": "app.bsky.feed.post", "text": a.text,
              "langs": [a.lang],
              "createdAt": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())}
    f = facets(a.text)
    if f:
        record["facets"] = f

    res = post("/com.atproto.repo.createRecord",
               {"repo": did, "collection": "app.bsky.feed.post", "record": record}, token)
    handle = sess.get("handle", ident)
    rkey = res["uri"].rsplit("/", 1)[-1]
    receipt = {"handle": handle, "uri": res["uri"], "cid": res["cid"],
               "url": f"https://bsky.app/profile/{handle}/post/{rkey}",
               "postedAt": record["createdAt"], "facets": len(f)}
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
