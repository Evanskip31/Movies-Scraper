# Movies-Scraper

You are probably tired of navigating through a movie website to get the right movie you'd want to watch during the weekend. There may even be no time to do that. With this code, you'll be getting newly uploaded movie links sent to your email (*still under progress)

This code scrapes movies from [this site](https://yts.mx). 

If you want this code available to you locally, you can clone it:
`git clone https://github.com/Evanskip31/Movies-Scraper.git`

The very first thing is to import all the necessary libraries for this task. These include:
```
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
```
If you get import errors, it means you've probably not installed the libraries.
To install, we'll use `pip`:
``` 
pip install beautifulsoup4
pip install requests
pip install collections
```
