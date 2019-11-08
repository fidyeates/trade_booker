## Trade Booker

This trade booker web-application lets you list historic trades
listed by order date, and book new ones.

### Setup

Run:

```
sudo -H setup.sh
python3 bin/app.py
```

### Improvements and considerations

- ID generation is currently not very good, but that's a factor of using
sqlite as the backend. 
- Implementation of pagination into the list view would be useful for a production
ready application as historic trades could get very long.
- Ability to sort trades by date or filter
- Formatting, such as decimals for buy amount, fixed to 2 decimals currently 
but would need to understand the requirements for displaying the value further.
- Passing data from the frontend to the backend is not what you'd want to do, you'd perform the currency
lookups internally on the webserver and propagate that information back to the client. 
- There's not a lot here code wise to really unittest, as we're quickly into integration test 
and system test domains. 
- Platform independent setup (ubuntu/mac) etc, at the moment expects python3 and pip3 to be installed.
The gotchas of a distribution independent setup script I believe is somewhat out of scope of this 
exercise.
