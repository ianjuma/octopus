## octopus - AfricasTalking API demo app

#### A simple demo app on USSD, messaging (shortcode), mobile payments (mpesa), airtime and Voice API's.

- Register through ShortCode/ USSD
- Call number
- Push USSD - M-pesa payment
- Call number - to thank subscribers
- Message the number


#### Why Redis?

- A temporary in memory database is great to 'persist' variables. And also avoid unbounded growth of 
    queues and variables. Its easy to reason about persistence in Redis, its a data structure server. And 
      we love data structures! :D

- RQ. We use RQ as an ORM to redis, nothing fancy here.
- Twisted/ gevent/ gunicorn. Well, it's voice. Why not make the req/ rep cycle more concurrent? Greenlets rock!


#### Why WIT

- Lets not write a boring SMS based app. Lets write some AI, an Uber/ Waze on SMS maybe :)


#### API endpoints

- /api/shortcode/callback/
- /api/ussd/callback/
- /api/voice/callback/
- /api/messaging/dlr/callback/


### Flask and REST anti-patterns?

- I don't care much!
- Don't use flask globals (avoid binding g to the req context)
- It's not RESTful but it works :P
- way too many if's
- MV* - Man, I got tired! Open to pull requests
- Patterns, patters, patterns. It works.
