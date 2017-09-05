from google.cloud import spanner

instance_id = "test-instance"
database_id = "example-db"
table_name = "Singers"

client = spanner.Client()
instance = client.instance(instance_id)
database = instance.database(database_id)

with database.batch() as batch:
        batch.insert(
            table=table_name,
            columns=('SingerId', 'FirstName', 'LastName',),
            values=[
                (1, u'Marc', u'Richards'),
                (2, u'Catalina', u'Smith'),
                (3, u'Alice', u'Trentor'),
                (4, u'Lea', u'Martin'),
                (5, u'David', u'Lomond')])
