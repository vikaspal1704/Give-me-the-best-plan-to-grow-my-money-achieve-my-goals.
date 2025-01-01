from quickstart_connect import connect_to_database
from astrapy import Database, Collection
from astrapy.constants import VectorMetric
from astrapy.info import CollectionVectorServiceOptions
import json


def create_collection(database: Database, collection_name: str) -> Collection:
    """
    Creates a collection in the specified database with vectorization enabled.
    The collection will use Nvidia's NV-Embed-QA embedding model
    to generate vector embeddings for data in the collection.

    Args:
        database (Database): The instantiated object that represents the database where the collection will be created.
        collection_name (str): The name of the collection to create.

    Returns:
        Collection: The created collection.
    """
    try:
        collection = database.create_collection(
            collection_name,
            metric=VectorMetric.COSINE,
            service=CollectionVectorServiceOptions(
                provider="nvidia",
                model_name="NV-Embed-QA",
            ),
        )
        print(f"Created collection: {collection.full_name}")
        return collection
    except Exception as e:
        print(f"Error creating collection: {e}")
        raise


def upload_json_data(
    collection: Collection,
    data_file_path: str,
    embedding_string_creator: callable,
) -> None:
    """
    Uploads data from a file containing a JSON array to the specified collection.
    For each piece of data, a $vectorize field is added. The $vectorize value is
    a string from which vector embeddings will be generated.

    Args:
        collection (Collection): The instantiated object that represents the collection to upload data to.
        data_file_path (str): The path to a JSON file containing a JSON array.
        embedding_string_creator (callable): A function to create the string for which vector embeddings will be generated.
    """
    try:
        # Read the JSON file and parse it into a JSON array.
        with open(data_file_path, "r", encoding="utf8") as file:
            json_data = json.load(file)

        # Add a $vectorize field to each piece of data.
        documents = [
            {
                **data,
                "$vectorize": embedding_string_creator(data),
            }
            for data in json_data
        ]

        # Upload the data.
        inserted = collection.insert_many(documents)
        print(f"Inserted {len(inserted.inserted_ids)} items.")
    except Exception as e:
        print(f"Error uploading data: {e}")
        raise


def main():
    """
    Main function to execute the database connection, collection creation, and JSON data upload.
    """
    try:
        # Connect to the database
        database = connect_to_database()

        # Create a collection
        collection = create_collection(database, "social_media_engagement")

        # Upload data from the JSON file
        upload_json_data(
            collection,
            "./engagement_data.json",
            lambda data: (
                f"post_type: {data['post_type']}, likes: {data['likes']}, "
                f"shares: {data['shares']}, comments: {data['comments']}"
            ),
        )
    except Exception as e:
        print(f"An error occurred in main: {e}")


if __name__ == "__main__":
    main()
