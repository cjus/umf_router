# WebSocket Universal Message Router (POC)
umf_router is a Python/Flask server application which uses gevent and gevent-websocket to handle WebSocket messages which are formatted using a JSON message format called UMF.
This application is a proof-of-concept for bidirectional message passing via WebSockets.  To learn more about UMF see the [UMF Documentation](https://bringit.atlassian.net/wiki/display/PB/Universal+Messaging+Format)

This project also includes a single page application (SPA) tester written using AngularJS. The tester is called UMFTester and can be used to send/receive messages to/from Flask-based UMFRouter.

# Installation
See the requirements.txt file for the small list of package dependencies.

# UMFTester
![UMFTester screenshot](https://stash.bringit.com/users/cjus/repos/umf_router/browse/UMFTester.png?&raw "UMFTester screenshot")
## Using the UMFTester application
Run the UMF Router (backend) server using:

    $ ./runserver.py

Then go to your web browser and load:

    http://localhost:5000

You should see a page similar to the one shown in the screenshot above.

The page is divided into two panels, Test Options and Console

### Setting Test Options
UMFTester allows you to perform a number of different tests. Essentially you can specify the number of messages to send per second. Each second is considered a test iteration.
For each tests you can select the type of messages you'd like to send. If "random" is chosen then the test will randomly switch between message types.
You can also set the number of messages to send via each test iteration.
To can also set the number of iterations you'd like to run. Lastly you can specify an amount of bytes to add to each message's payload.

When you're ready you can press the Start button to begin a test. You can at anytime during a test press the Stop button to abort a test.

### Viewing Test Output
The Console will show the tests activity as test execute. Cool huh?

### Mobile / Tablet friendly
UMFTester is built with responsive design in mind and written using Bootstrap and AngularJS.

# Status of tests
## UMFRouter (Python/Flask Server)
The core test is for the actual UMF router located in /umf/umf_router_tests.py

## UMFTester (AngularJS SPA)
The SPA's tests are in /app/tests/spec.  Load the SpecRunner.html to see tests run.

# TODOs
This entire application is simple a WebSocket proof of concept, however there are still a lot of things that can be added to improve it.

* Improved documentation.
* More tests!
* More doc strings.

