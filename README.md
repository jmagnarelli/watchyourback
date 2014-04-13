# TweetPD

----

[TweetPD](http://www.tweetpd.com) is an alert service for local emergencies. It
listens in on municipal fire, police, and 911 dispatch Twitter accounts, and can
let you know if something's wrong in your area. TweetPD currently supports the
following alert methods:

* SMS text message 
* US Mail

That's right! Postal mail. If there's a fire down the street from you, we can
*immediately* dispatch a postard to your residence, and in just a few short
business days, you'll know all about the emergency. The future is now!


----
## Technologies used
1. Flask server
2. [Lob](https://www.lob.com) API, for sending postcards
3. [Twilio](https://www.twilio.com) API, for sending SMS
4. [Tweepy](https://github.com/tweepy/tweepy), for listening in on the po-po
5. [Twitter Bootstrap](http://http://getbootstrap.com)

Note: If you were thinking of actually relying on this for emergency
notifications, don't. It's a pet project, and it's not even guaranteed to be
running at any particular time.

[Photo Credit](https://flic.kr/p/7KADUp) for the original background image. Yes,
changes were made.
