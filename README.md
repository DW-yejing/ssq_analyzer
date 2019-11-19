# ssq_analyzer

![code size](https://img.shields.io/github/languages/code-size/DW-yejing/ssq_analyzer) ![license](https://img.shields.io/github/license/DW-yejing/ssq_analyzer) ![issues](https://img.shields.io/github/issues/DW-yejing/ssq_analyzer) ![stars](https://img.shields.io/github/stars/DW-yejing/ssq_analyzer?style=social)

ssq_analyzer is a set of The double chromosphere prediction tools. It consists mainly of two parts:

>first part  
Crawl the required historical data from the [official website](http://www.cwl.gov.cn/), then stored in excel format.  

> second part  
generate a bulk json file(to put those data into our elasticsearch cluster ) by parsing the stored file.

finnaly, we need up and running our es cluster, index the historical data, and get the prediction by aggregations.

## Elasticsearch reference

>index mapping

``` json
PUT /kjxx
{
  "mappings": {
    "properties": {
      "code": { "type": "long" },  
      "red":  { "type": "integer"  },
      "blue": { "type": "integer"  }
    }
  }
}
```

> index data

``` curl
curl -H "Content-Type: application/json" -XPOST "localhost:9200/kjxx/_bulk?pretty&refresh" --data-binary "@xxx.json"
```

> aggregations

``` json
POST kjxx/_search?size=0
{
    "aggs":{
        "blues":{
            "terms":{
                "field": "blue"
            }
        }
    }
}
```

## LICENSE

[MIT](LICENSE)
