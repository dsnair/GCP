#!/bin/bash

# Set-up project
echo -e "Setting-up your project\n"
gcloud init

# --------------------------------------------
# instance ID = test-instance
# instance name (for display) = Test instance
# database name = example-db
# table name = Singers
# --------------------------------------------

# Create Spanner instance
echo -e "Creating Spanner instance\n"
#gcloud spanner instances create --help

gcloud spanner instances create test-instance \
--config=regional-us-west1 \
--nodes=1 \
--async \
--description="Test instance"

# View instance status
gcloud spanner instances list

# View list of regional locations
#gcloud spanner instance-configs list

# Create database and set table schema
echo -e "Creating database and setting table schema\n"
#gcloud spanner databases create --help

gcloud spanner databases create example-db \
--instance=test-instance \
--ddl='CREATE TABLE Singers (SingerId INT64 NOT NULL, FirstName STRING(1024), LastName STRING(1024), SingerInfo BYTES(MAX)) PRIMARY KEY (SingerId)' \
--async

# View database status
gcloud spanner databases list --instance=test-instance
