# KSQL

## Setup
```bash
bin/ksql
```

## L7.9 - Practice: Creating a Stream
Là file `Exercise7.1.ipynb`
1. Xem các topics
    
    ```sql
    SHOW TOPICS;
    ```
    
2. Tạo một stream
    
    ```sql
    CREATE STREAM clickevents
      (email VARCHAR,
       timestamp VARCHAR,
       uri VARCHAR,
       number INTEGER)
      WITH (KAFKA_TOPIC='com.udacity.streams.clickevents',
            VALUE_FORMAT='JSON');
    ```
    
3. Xem các streams
    
    ```sql
    SHOW STREAMS;
    ```
    
4. Tạo một stream từ query
    
    ```sql
    CREATE STREAM popular_uris AS
      SELECT * FROM clickevents
      WHERE number >= 100;
    ```
    
5. Xóa một stream
    
    ```sql
    DROP STREAM popular_uris;
    ```
    
## L7.10 - Practice: Creating a Table
Là file `Exercise7.2.ipynb`
1. Giống Kafka Consumers, KSQL mặc định bắt đầu consumption tại **latest offset**. Ta sẽ tạo một pages table, nhưng ta muốn tất cả data là available trong table này, nghĩa là ta muốn KSQL bắt đầu từ **earliest offset**.
    ```sql
    SET 'auto.offset.reset' = 'earliest';
    UNSET 'auto.offset.reset';
    ```
    
2. Tạo một table
    ```sql
    CREATE TABLE pages
      (uri VARCHAR PRIMARY KEY,
       description VARCHAR,
       created VARCHAR)
      WITH (KAFKA_TOPIC='com.udacity.streams.pages',
            VALUE_FORMAT='JSON');
    ```
    
    PRIMARY KEY là string mà uniquely identifies records. Với KSQL TABLEs, ta sẽ theo dõi latest value cho một given key, ko phải tất cả values ta đã từng thấy cho một key.
    
3. Tạo một table từ query
    ```sql
    CREATE TABLE a_pages AS
      SELECT * FROM pages WHERE uri LIKE 'http://www.a%';
    ```
    
4. Describe table
    ```sql
    DESCRIBE pages;
    ```
    
5. Xóa một table
    ```sql
    DROP TABLE A_PAGES;
    ```
    

## L7.12 - Querying
Là file `Exercise7.3.ipynb`
1. Basic filtering
    ```sql
    SELECT uri, number
      FROM clickevents
      WHERE number > 100
        AND uri LIKE 'http://www.k%';
    ```
    
2. Scalar function
    ```sql
    SELECT UCASE(SUBSTRING(uri, 12))
      FROM clickevents
      WHERE number > 100
        AND uri LIKE 'http://www.k%';
    ```
    

`SELECT` queries ko phải là persistent. Ngay khi ấn CTRL+C, query sẽ kết thúc. Nếu muốn chạy lại query, KSQL phải recreate query. Nếu muốn KQ của query là persistent, ta phải tạo một Table hoặc một Stream.

## L7.13, 7.14 - Hopping, Tumbling, Session Windowing
Là file `Exercise7.4.ipynb`
1. Tumbling windows
    
    ```sql
    CREATE STREAM clickevents_tumbling AS
      SELECT * FROM clickevents
      WINDOW TUMBLING (SIZE 30 SECONDS);
    ```
    
2. Hopping windows
    ```sql
    CREATE TABLE clickevents_hopping AS
      SELECT uri FROM clickevents
      WINDOW HOPPING (SIZE 30 SECONDS, ADVANCE BY 5 SECONDS)
      WHERE uri LIKE 'http://www.b%'
      GROUP BY uri;
    ```
    
3. Session windows
    ```sql
    CREATE TABLE clickevents_session AS
      SELECT uri FROM clickevents
      WINDOW SESSION (5 MINUTES)
      WHERE uri LIKE 'http://www.b%'
      GROUP BY uri;
    ```
Các queryies trên đang có lỗi chưa đc sửa.

## L7.17 - Practice: Aggregating Data
Là file `Exercise7.5.ipynb`
1. SUM
    
    ```sql
    SELECT uri, SUM(number)
    FROM clickevents
    GROUP BY uri
    EMIT CHANGES;
    ```
    
2. HISTOGRAM
    ```sql
    SELECT uri,
      SUM(number) AS total_number,
      HISTOGRAM(uri) AS num_uri
    FROM clickevents
    GROUP BY uri
    EMIT CHANGES;
    ```
    
3. TOPK
    ```sql
    SELECT uri , TOPK(number, 5)
    FROM clickevents
    WINDOW TUMBLING (SIZE 30 SECONDS)
    GROUP BY uri
    EMIT CHANGES;
    ```
    

## L7.18 - Practice: Joins
Là file `Exercise7.6.ipynb`
1. LEFT OUTER JOIN (mặc định của JOIN)
    ```sql
    CREATE STREAM clickevent_pages AS
      SELECT ce.uri, ce.email, ce.timestamp, ce.number, p.description, p.created
      FROM clickevents ce
      JOIN pages p on ce.uri = p.uri;
    ```
    
2. INNER JOIN
    ```sql
    CREATE STREAM clickevent_pages_inner AS
      SELECT ce.uri, ce.email, ce.timestamp, ce.number, p.description, p.created
      FROM clickevents ce
      INNER JOIN pages p on ce.uri = p.uri;
    ```
    
3. FULL OUTER JOIN
    ```sql
    CREATE STREAM clickevent_pages_outer AS
      SELECT ce.uri, ce.email, ce.timestamp, ce.number, p.description, p.created
      FROM clickevents ce
      FULL OUTER JOIN pages p on ce.uri = p.uri;
    ```
    Query này sẽ ko chạy đc. KSQL chỉ hỗ trợ`FULL OUTER JOIN khi join một Table với một Table hoặc một Stream với một Stream.
    

## L7.20 - Practice: Putting it all together
Là file `Exercise7.7.ipynb`
1. Tạo một table of user data và purchases, và một stream of click events. Trong table này, ta cho user information đi kèm với total amount of their purchases.
    ```sql
    CREATE TABLE users
    (username VARCHAR PRIMARY KEY,
    email VARCHAR,
    phone_number VARCHAR,
    address VARCHAR)
    WITH (KAFKA_TOPIC='com.udacity.streams.users',
      VALUE_FORMAT='JSON');
    CREATE STREAM clickevents
    (username VARCHAR KEY,
    email VARCHAR,
    timestamp VARCHAR,
    uri VARCHAR,
    number INTEGER)
    WITH (KAFKA_TOPIC='com.udacity.streams.clickevents',
      VALUE_FORMAT='JSON');
    CREATE TABLE purchases
    (username VARCHAR PRIMARY KEY,
    currency VARCHAR,
    amount INTEGER)
    WITH (KAFKA_TOPIC='com.udacity.streams.purchases',
      VALUE_FORMAT='JSON');
    ```
    
2. Tạo một join table của user purchases và user data
    ```sql
    CREATE TABLE user_purchases WITH (PARTITIONS=10) AS 
    SELECT 
    u.username AS username, 
    p.amount AS purchase_amount,
    u.email AS email,
    u.phone_number AS phone_number,
    u.address AS address
    FROM purchases p
    JOIN users u ON u.username = p.username;
    ```
    
3. Tạo một stream join user purchases và user clicks
    ```sql
    CREATE STREAM user_purchases_clicks WITH (PARTITIONS=10) AS 
    SELECT 
     up.username AS username, 
     up.purchase_amount AS purchase_amount,
     c.number AS num_clicks,
     up.email AS email,
     up.phone_number AS phone_number,
     up.address AS address
    FROM clickevents c
    JOIN user_purchases up ON up.email= c.email;
    ```
    
4. Tạo aggregated output
    ```sql
    CREATE TABLE user_activity AS
    SELECT 
     upc.username,
     upc.email,
     upc.phone_number,
     upc.address,
     SUM(upc.purchase_amount) AS total_purchase_value,
     SUM(num_clicks) AS total_clicks
    FROM user_purchases_clicks upc
    GROUP BY upc.username, upc.email, upc.phone_number, upc.address;
    ```
Query 3 và 4 có lỗi.