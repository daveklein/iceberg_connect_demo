# iceberg_connect_demo

This demonstration will send data into an Apache Kafka topic which will be picked up by the Iceberg Connector for Kafka Connect and written to an Iceberg table.

## Technologies involved
- Apache Iceberg
- Apache Spark / PySpark
- MinIo
- Apache Kafka
- Kafka Connect
- Python

## Steps to run demo
1. Launch server applications
    `docker compose up -d`
2. Create Kafka topic
    `docker exec -t broker kafka-topics --create --topic completed-pizzas --partitions 6 --bootstrap-server broker:9092`
3. Launch the Iceberg connector (installed via docker compose)
    `curl -X PUT http://localhost:8083/connectors/pizzas-on-ice/config \
     -i -H "Content-Type: application/json" -d @pizzas_on_ice.json`
4. Check status of connector
    `curl http://localhost:8083/connectors/pizzas-on-ice/status |jq`
5. Install `confluent-kafka` package
    `pip install confluent-kafka`
6. Run pizza loader script
    `python pizza_loader.py`
7. Launch PySpark
    `docker exec -it spark-iceberg pyspark`
8. Explore Iceberg table
    `df = spark.table("demo.rpc.pizzas")`
    `df.count()`
    `df.show(5)`
    `df.groupBy("store_id").count().sort("count", ascending=False).show(5)`
