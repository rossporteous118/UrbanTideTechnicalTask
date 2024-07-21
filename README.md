# UrbanTide Technical Task

### Overview 
This project ingests data in the form of two small CSV files from an API. It uses the Pandera Python library to apply some simple constraints and ensure that the datatypes are correct. The program then performs some basic outlier detection using the interquartile range method before finally inserting the data into a PostgreSQL database provided no outliers are present in the dataset. 

The application is Dockerised using Docker Compose to simplify the setup and deployment.


### Build and run the container

1. Clone the git repository:
   
     git clone https://github.com/rossporteous118/UrbanTideTechnicalTask.git

2. Naviagte to the correct directory.

3. Build and run the container:
   
     docker-compose up --build
  

### Check data with PostgreSQL

1. Connect to the PostgreSQL container. 'postgres-container-id' can be found at the top left of Docker desktop under the container name.

      docker exec -it <postgres-container-id> psql -U postgres -d technical_test

3. Select data using SQL.

      SELECT * FROM output_table;

4. The output table should now be displayed in the terminal.



