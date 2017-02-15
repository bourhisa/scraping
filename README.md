# Scraper and web parser

The final goal of this project was to build a list of e-commerce websites that were using schema.org to format their products.
It is divided into 2 parts.

- Scrapers :
	The folders "alexa/" and "thuiswinkel/" folders contain scrapers made to read the websites' pages and extract all the e-commerce URLs that appear in the HTML. The results are written to TXT and JSON files.
	A total of ~70000 URLs were collected and are included in this folder.

	- For Alexa (giant web index & property of AWS), a recursive function enables to retrace the website's page hierarchy and access all of the pages. It is adaptable for any resource available on Alexa.
	- For Thuiswinkel, it simply visits differents pages sorted by alphabetical orders and reads them.

- Web Parser: 
	The "schema_dot_org/" folder consists of a webscraper that visits each one of these URLs to look for the presence of a string (here: "schema.org/Product").
	From the landing page, it will list all the links to visit, roam randomly through the website and so on, until a breakpoint: either the result is null (the website never uses the string) or the string has been found in one of the pages.
	It will then write the results into a txt and JSON files.
	In the current version of the files, the execution isnt completely over, only 4000 URLs containing "schema.org/Product" are listed here.
	
