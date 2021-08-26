# activity-schedule
API REST como Prueba técnica para TrueHome

## Project Link
[Live API](http://ec2-18-191-2-61.us-east-2.compute.amazonaws.com/)

## Run locally

To run the project locally docker-compose must be installed.
Once it's installed and set properly, run the following command.

`docker-compose up -d --build`

If you want dummy data loaded into the DB, run:

`docker-compose exec web python manage.py loaddata dummy_data`

### Tests

To run the project's tests run:

`docker-compose exec web python manage.py test`
