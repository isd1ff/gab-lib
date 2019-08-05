

# API calls
You can find here all documentation: 

https://docs.joinmastodon.org/api/rest/

### Sending a new status in the client account:
```
gab.toot_send("hello world");
```
### Getting a status information:
```
gab.toot_get("123321");
```
### Getting a status context:
```
gab.toot_context("123321");
```
### Getting a status reposts:
```
gab.toot_reposts("123321");
```
### Getting a status favorite:
```
gab.toot_favorites("123321");
```
### Getting a status card:
```
gab.toot_card("123321");
```
### Share/Unshare a status:
```
gab.toot_share("123321");
gab.toot_unshare("123321");
```
### Pin/Unpin a status:
```
gab.toot_pin("123321");
gab.toot_unpin("123321");
```
### Like/Unlike (aka favourite in gab) a status:
```
gab.toot_like("123321");
gab.toot_unlike("123321");
```
### Search general stuff:
```
gab.search("human groups");
```
### Get client notifications:
```
gab.notifications();
```
### Clear all client notifications:
```
gab.notifications_clear();
```
### Remove single client notification:
```
gab.notification_remove("33333");
```
### Get account information:
```
gab.user("123344");
```
### Get accounts followed by single account:
```
gab.user_following("123344");
```
### Get followers from a single account:
```
gab.user_followers("123344");
```
### Get account statuses (limit:40 per pagination):
```
gab.user_toots("123344");
```
### Follow/Unfollow specific account:
```
gab.user_follow("123344");
gab.user_unfollow("123344");
```

## Pagination
Some api calls have a limit of 40 items per array.

So when you have a `link:` in the response headers, you
can get next/previous page using `pagination` routine.

Example:
```
following = gab.user_following("123344",{"limit":40})
if following.status_code==200:
  next_page = gab.paginate(following.headers,True)
  prev_page = gab.paginate(following.headers,False)
  ...
````

## Responses
All lib responses are native from `requests` library.