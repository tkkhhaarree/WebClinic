- open project folder in pycharm.
- find the file data_dummy.json given with this project, rename it to 'data.json' and place it in prefered location. 
- go to line 95, 134, 136, 143, 145, 199, 208, 220 and change the path of data.json in each line according to
   the location you put the file in previous step (remember to use full path eg: C:\\Users\\ABC\\Desktop\\data.json
   and use double slashes \\ for escape characters).
- open mysql and type command: drop database ehrserver; 
   then again type: create database ehrserver; as we need to start with fresh database.
- again open cmd and run ehrserver by changing location to ehrserver folder using cd command, then type: grails run-app
- now make sure django, requests etc libraries are installed. then run django project using command:
     python manage.py runserver
- goto server_address_displayed/ehrs (eg: 127.0.0.1:8000/ehrs). login using: admin, admin, 123456.
- note: dont use template 'cancer signs' as of now as I didn't code it due to lack of dataset.