from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class AstraDB:
    def __init__(self, secure_connect_path):
        self.auth_provider = PlainTextAuthProvider()
        self.cluster = Cluster(cloud={"secure_connect_bundle": secure_connect_path}, auth_provider=self.auth_provider)
        self.session = self.cluster.connect()
        self.session.set_keyspace("social_media")

    def create_table(self):
        self.session.execute("""
        CREATE TABLE IF NOT EXISTS engagement_data (
            post_id int PRIMARY KEY,
            post_type text,
            likes int,
            shares int,
            comments int
        )
        """)

    def insert_data(self, data):
        for record in data:
            self.session.execute("""
            INSERT INTO engagement_data (post_id, post_type, likes, shares, comments)
            VALUES (%s, %s, %s, %s, %s)
            """, record)

    def query_data(self, post_type):
        result = self.session.execute(f"""
        SELECT AVG(likes) AS avg_likes, AVG(shares) AS avg_shares, AVG(comments) AS avg_comments
        FROM engagement_data
        WHERE post_type = '{post_type}'
        """)
        return result.one()
