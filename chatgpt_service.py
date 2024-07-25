from openai import OpenAI

api_key = 'sk-proj-TOy9JHjRP0PV8e30WHCfT3BlbkFJD7UnqPMZj3q3KURZHvjq'


client = OpenAI(api_key=api_key)


def get_chatgpt_response(prompt):
    try:
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].text
    except Exception as e:
        return f"Error: {e}"
