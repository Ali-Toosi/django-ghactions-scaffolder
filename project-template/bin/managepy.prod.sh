docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec app sh -c "cd src && python manage.py $1 $2 $3 $4"