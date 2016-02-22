# Wox Youtube Plugin
A Plugin for Wox to search and display youtube results. It allows you to search the top n youtube videos results via the wox searchbox and open the one you're interested in.

The following syntax is used:
yt [query [order by {date|rating|relevance|title|videoCount|viewCount}]] | --config].
The []-brackets symbolize that this is optional, the pipe (a|b) means use either a or b for your query.

To learn more about WOX visit http://www.getwox.com/.

To have a youtube logo displayed while searching, add one to the wox_youtube Plugin folder and rename it to icon.png.

![alt tag](https://raw.githubusercontent.com/username/projectname/branch/path/to/img.png)

Before being able to use the plugin you have to create an API key for Youtube. After creating it, you can parse it into the config.json file or use "yt --config api *Your key here*".

To change the language use "yt --language *your 2 char language code" and to change the maximum number of results displayed to e.g. 0 use "yt --config maxResults 10".
