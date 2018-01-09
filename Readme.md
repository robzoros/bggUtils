# Some Commands
```
wget "http://www.boardgamegeek.com/xmlapi2/collection?username=username&subtype=boardgame&own=1&excludesubtype=boardgameexpansion&brief=1" [-O collection.xml]

wget "http://www.boardgamegeek.com/xmlapi2/plays?username=username&mindate=2017-01-01&maxdate=2017-12-31&subtype=boardgame&page=1" [-O played.xml]

wget "http://www.boardgamegeek.com/xmlapi2/thing?id=826"

xsltproc [-o collectionID.txt] BGG_id.xsl collection.xml

python bgg_thing.py [-f collectionID.txt] [-o collection.csv]

xsltproc [-o played.json] BGG-plays2.xsl [played.xml]

spark-submit \
  --class BGGPlaysStats \
  --master spark://master.spark.tfm:7077 \
  [directory jar]/sparkbgg_2.11-1.0.jar \
  file:[played.json]
```


