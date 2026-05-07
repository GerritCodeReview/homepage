Homepage for [Gerrit Code Review][home].

[home]: https://www.gerritcodereview.com/

Instructions how to publish the Gerrit documentation can be found at:
https://www.gerritcodereview.com/publishing.html

docker build -t gerritcodereview/homepage .
docker run -p 4000:4000 -v $(pwd):/site gerritcodereview/homepage