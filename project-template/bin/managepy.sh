docker-compose up -d app db
docker-compose exec app sh -c "cd src && python manage.py $1 $2 $3 $4"