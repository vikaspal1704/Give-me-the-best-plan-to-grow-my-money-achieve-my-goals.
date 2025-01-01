import openai
from database.quickstart_connect import connect_to_database
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_post_performance(collection, post_type):
    """
    Analyze average engagement metrics for a specific post type.

    Args:
        collection: The collection from Astra DB.
        post_type: The type of post to analyze (e.g., "carousel", "reels").

    Returns:
        A dictionary containing the average likes, shares, and comments.
    """
    print(f"\nAnalyzing performance for post type: {post_type}...")

    # Aggregate metrics for the given post type
    cursor = collection.find({"post_type": post_type})
    total_likes, total_shares, total_comments, count = 0, 0, 0, 0

    for document in cursor:
        total_likes += document.get("likes", 0)
        total_shares += document.get("shares", 0)
        total_comments += document.get("comments", 0)
        count += 1

    if count == 0:
        print(f"No data found for post type: {post_type}")
        return None

    average_metrics = {
        "post_type": post_type,
        "average_likes": total_likes / count,
        "average_shares": total_shares / count,
        "average_comments": total_comments / count,
    }

    print(f"Metrics for {post_type}: {average_metrics}")
    return average_metrics


def generate_insights(metrics):
    """
    Generate insights using GPT for the given metrics.

    Args:
        metrics: A dictionary of engagement metrics.

    Returns:
        A string containing the insights.
    """
    # Ensure the OpenAI API key is set
    client = OpenAI()
    if not openai.api_key:
        raise RuntimeError("OpenAI API key is not set. Please add it to the .env file.")

    messages=[
                {
                    "role": "system",
                    "content": "You are an assistant generating insights from social media performance metrics.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Analyze the following social media engagement metrics:\n"
                        f"Post Type: {metrics['post_type']}\n"
                        f"Average Likes: {metrics['average_likes']}\n"
                        f"Average Shares: {metrics['average_shares']}\n"
                        f"Average Comments: {metrics['average_comments']}\n"
                        f"Provide actionable insights based on the performance."
                    ),
                },
            ],
    # completion = client.chat.completions.create(
    #                     model="gpt-4o-mini",
    #                     messages=[
    #             {
    #                 "role": "system",
    #                 "content": "You are an assistant generating insights from social media performance metrics.",
    #             },
    #             {
    #                 "role": "user",
    #                 "content": (
    #                     f"Analyze the following social media engagement metrics:\n"
    #                     f"Post Type: {metrics['post_type']}\n"
    #                     f"Average Likes: {metrics['average_likes']}\n"
    #                     f"Average Shares: {metrics['average_shares']}\n"
    #                     f"Average Comments: {metrics['average_comments']}\n"
    #                     f"Provide actionable insights based on the performance."
    #                 ),
    #             },
    #         ],
    #                 )

        # Access the response using dot notation
    # insights = completion.choices[0].message
    print(f"Prompt:\n\n\n",messages)
    # print(f"\nGenerated Insights:\n{insights}")
    return messages



def main():
    """
    Main function to analyze post performance and generate insights.
    """
    # Connect to the database
    database = connect_to_database()

    # Access the collection
    collection = database.get_collection("social_media_engagement")

    # Input: Post type
    post_type = input("Enter post type (carousel, reels, static): ").strip().lower()

    # Validate post type
    if post_type not in {"carousel", "reels", "static"}:
        print("Invalid post type entered. Please choose from carousel, reels, or static.")
        return

    # Analyze post performance
    metrics = analyze_post_performance(collection, post_type)

    if metrics:
        # Generate insights using GPT
        generate_insights(metrics)


if __name__ == "__main__":
    main()
