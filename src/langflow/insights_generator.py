import openai

openai.api_key = "your-openai-api-key"

class InsightsGenerator:
    @staticmethod
    def generate_insight(metrics):
        prompt = f"""
        Based on the following engagement metrics:
        - Average Likes: {metrics.avg_likes}
        - Average Shares: {metrics.avg_shares}
        - Average Comments: {metrics.avg_comments}

        Provide actionable insights on post performance.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
