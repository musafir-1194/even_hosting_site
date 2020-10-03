Installation:

Create a directory

>> mkdir even_hosting
>> cd even_hosting 

Extract the ZIP file

Create Virutal ENV
>> virtualenv --no-site-packages ./env

Activate
>> source ./env/bin/activate

Run requirements.txt
>> pip install -r requirements.txt

Run Migrations
>> flask db init
>> flask db migrate

Start Python interpreter from env
>>> from even_hosting import db
>>> db.create_all()

Run your application
export FLASK_APP="project/_init_.py"
export FLASK_DEBUG=1
flask run
