#### **References**
- [https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [https://www.youtube.com/watch?v=C3tlMqaNSaI](https://www.youtube.com/watch?v=C3tlMqaNSaI)
- [https://viblo.asia/p/elasticsearch-la-gi-1Je5E8RmlnL](https://viblo.asia/p/elasticsearch-la-gi-1Je5E8RmlnL)
- [https://viblo.asia/p/elasticsearch-distributed-search-ZnbRlr6lG2Xo#replica-shard-6](https://viblo.asia/p/elasticsearch-distributed-search-ZnbRlr6lG2Xo#replica-shard-6)
#### **Local setup**
Open `wsl`, run these command to run the `elasticsearch`
`docker network create elastic`
`docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2`
`docker run --name es01 --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -t docker.elastic.co/elasticsearch/elasticsearch:8.12.2`

Config
`export ELASTIC_PASSWORD="your_password"`
`docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .`
`curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200`

Run kibana
`docker pull docker.elastic.co/kibana/kibana:8.12.2`
`docker run --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.12.2`

Endpoint: 
`http://localhost:5601/?code=751482`



