# gab-lib
Simple gab library for API, from a python beginner.

## Require
Python 3+

## Usage
You can find CLIENT_TOKEN in Gab Preferences > Developer > New Application

Some commands may not work if there's no permission in the application.
```
import gab

BASE_URL="https://api.gab.com/"
CLIENT_TOKEN = "AAAAA-AAAA-AAAA"

auth = lib.AuthAPI(BASE_URL,CLIENT_TOKEN)
gab = lib.GabAPI(auth)

gab.toot("hello world");
```
