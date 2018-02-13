FROM docker.elastic.co/elasticsearch/elasticsearch:6.0.1

ENV cluster.name=docker-cluster \
    ES_JAVA_OPTS="-Xms1024m -Xmx1024m" \
    xpack.security.enabled=false

RUN elasticsearch-plugin install analysis-kuromoji
RUN elasticsearch-plugin install analysis-icu
