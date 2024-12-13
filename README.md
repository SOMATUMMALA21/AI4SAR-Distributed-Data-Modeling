# AI4SAR-Distributed-Data-Modeling

## Requirements
1. Ensure Docker and Docker Compose are installed.
2. Verify that your system meets Docker's resource requirements.

## Steps
1. **Run Database Migrations and Initialize the User Account:**  
   ```bash
   docker compose up airflow-init
   ```
2. **Start All Services:**  
   ```bash
   docker compose up
   ```

## View
1. Open your web browser and go to: [http://localhost:8080](http://localhost:8080)
2. Use the following credentials to log in:
   - **Username:** airflow
   - **Password:** airflow

## Important Notes
The Docker Compose environment provided is a "quick-start" setup, intended for local development only. It is **not** suitable for production use due to several limitations.

### Recovery from Problems
If issues occur, the best recovery method is to clean up the environment and restart from scratch:

1. **Stop and Remove All Containers, Volumes, and Orphan Containers:**
   ```bash
   docker compose down --volumes --remove-orphans
   ```
2. **Delete the Directory with Docker Compose Files:**
   ```bash
   rm -rf '<DIRECTORY>'
   ```
3. **Restart the Setup:**  
   Follow the steps from the beginning, starting with re-downloading the `docker-compose.yaml` file.

### Cleanup Command
To stop and delete containers, remove volumes with database data, and delete downloaded images, run:
```bash
docker compose down --volumes --rmi all
```

### Additional Resources
For detailed usage and additional configurations, consult the official Apache Airflow Docker Compose guide:
[Airflow Docker Compose Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

## Hugging Face Integration
1. **Sign Into Hugging Face:**
   - Ensure your DAG is deployed in the service container.
   - Create a repository on Hugging Face for your model.
   - Generate an access token.
   - Use the Hugging Face CLI inside the container to log in and enable model updates.

### Note on Model Upload
- You must create your own Hugging Face repository before uploading your model.
- Replace `REPLACE_ME` in `upload_model.py` with your repository details to enable successful uploads.

## Images
1. **Apache Airflow at localhost:8080**
    - ![Airflow](https://i.imgur.com/OoehmM1.png)

2. **Successful Workflow in Apache Airflow**
    - ![Workflow](https://i.imgur.com/LGyW5VG.png)

3. **Hugging Face Model Repository**
    - ![Hugging Face](https://i.imgur.com/wozoGtU.png)

## To Be Done for Productionizing
1. Currently, models and data are stored locally, so it would be better to store them in a cloud storage service such as AWS S3.
2. Another step may need to be added to publish the model to another source so that it can be accessed via a restful API rather than having to pull the model from Hugging Face each time.
3. When retrieving data, please enfure that you create a new API token when getting NY missing cases from skops. Make sure to address the REPLACE_ME in data_retrieval.py.