import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_performance_agent(query: str, batch_df):
    data_summary = batch_df.to_json(orient="records")
    
    system_prompt = f"""
    You are an intelligent Academic Performance Advisor for a college professor/mentor.
    You have the following student LeetCode performance data for this semester in JSON format:
    {data_summary}

    Answer the professor's questions accurately based on this data:
    - Identify top performers, struggling students, or inactive students.
    - Mention exact counts (Easy, Medium, Hard).
    - Give clear suggestions to improve batch performance.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content