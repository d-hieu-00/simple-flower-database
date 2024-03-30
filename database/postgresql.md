# For docker usage (fast and light)

docker run --name db-postgres -e POSTGRES_PASSWORD=a -e POSTGRES_HOST_AUTH_METHOD=md5 -p 5432:5432 --restart always -d postgres
docker run --name db-pgadmin4 -e PGADMIN_DEFAULT_EMAIL=era@local.com -e PGADMIN_DEFAULT_PASSWORD=a -p 5000:80 --restart always -d dpage/pgadmin4
