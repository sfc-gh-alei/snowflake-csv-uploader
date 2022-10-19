# snowflake-csv-uploader
 Snowflake CSV file uploader

## Running in Docker

Simply build & run the image with the following:

```
docker build -t snowflake-csv-uploader .

# Run
docker run -it \
    -p 8501:8501 \
    -v "$PWD":/app \
    -w /app \
    snowflake-csv-uploader
```