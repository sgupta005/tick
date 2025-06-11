from openai import OpenAI
from task_profiler.prompt import QUESTION_PROMPT
from django.conf import settings

def get_question_from_openai(task):
    message = f"Task Name: {task.name} \nTask Topic: {task.topic.name}"
    client = OpenAI(
    api_key=settings.OPENAI_API_KEY
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "system", "content": QUESTION_PROMPT},
        {"role": "user", "content": message}
    ]
    )

    output = completion.choices[0].message.content
    return {"output":output, "openai_response":completion}