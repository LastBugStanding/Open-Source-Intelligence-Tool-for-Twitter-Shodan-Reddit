# Open Source Intelligence Tool for Twitter, Shodan, Reddit
This is my graduation project which i made using python as data collecting and ELK Stack (ElasticSearch, Logstash, Kibana) to visualize and show information about collected data such as Time-Date, Location on world map, sentiment analysis by keywords as well as  good and bad words dictionary filtering. 

To use the files you need to setup ELK stack and have necessary API provided by the data sources.

allScarper.py => Gathers data, formats it using regex library and creates a csv which Logstash pipelines that data from csv to ElasticSearch. Finally I using Kibana to visualize the data gathered in the process.

logstash_allScraper.config => Pipelines the data from csv to ElasticSearch with the given config. You need to change the file path, index name and server ip (if you are using an server other than localhost (127.0.0.1))
