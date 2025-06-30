# dou-scraper
Non-official dou.ua companies list scraper

# How to run
1. Go to https://jobs.dou.ua/companies/
2. Open Dev tools -> Network tab -> Fetch/XHR
3. Click on button on the website to load more companies
4. Go to Network -> click on the request -> take these fields:
   - User-Agent
   - csrftoken
   - _ga
   - _gcl_au
   - __gsas
   - _ga_N62L6SV4PV
5. Then go to payload -> copy csrfmiddlewaretoken
6. You are ready to go! Paste all these values to `main.py` and run it!
