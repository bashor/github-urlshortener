#github-urlshortener#

github-urlshortener is a extremely simple/hackish github static url shortener. It uses the permalink markup in Github Page' files to create url-friendly files which redirect to a desirable url.

##Usage##

1. Create a config.txt file containing the initial desirable start number (example: 10000)

2. Edit the shorturl.py BASE_URL constant:

     BASE_URL =  # your website base url

3. Set the origin git remote of the current repository to your github pages repository url:

     git remote set-url origin *remote-url*

     Make sure the repository has no git history.

4. Run the shorturl script passing the original url as parameter:

    $ python shorturl.py https://github.com/felipeborges/github-urlshortener

    $ http://feborg.es/q16
