# UrbanTide Technical Task

### Overview 
This project ingests data in the form of two small CSV files from an API. It then uses the Pandera Python library to apply some simple constraints and ensure that the datatypes are correct. The program then performs some basic outlier detection using the interquartile range method before finally inserting the data into a PostgreSQL database provided no outliers are present in the dataset. 

The application is Dockerised using Docker Compose to simplify setup and deployment.

### Running the program


