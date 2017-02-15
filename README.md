# Scraper and web parser

The final goal of this project was to build a list of e-commerce websites that were using schema.org to format their products.
It is divided into 2 parts.

- Scrapers :
	The folders alexa/ and thuiswinkel/ contain scrapers to read their pages and extract all the e-commerce URLs, and writes it to txt and/or JSON files.
	A total of ~70000 URLs were collected and are included in this folder.

	- For Alexa (giant web index & property of AWS), a recursive function enables to retrace the website's page hierarchy and access all of the pages.
	It is adaptable for any resource available on Alexa.
	- For Thuiswinkel, it simply visits differents pages sorted by alphabetical orders and reads them.


- Web Parsers
	The schema_dot_org folder consists of a webscraper that visits each one of these URLs to look for the presence of a the string "schema.org/Product".
	From the landing page, it will visit roam randomly through the website and check if the string appears.
	It will then write the results into a txt and JSON files.
	In the current version of the files, the execution isnt completely over, only 4000 URLs containing "schema.org/Product" are listed here.
	
