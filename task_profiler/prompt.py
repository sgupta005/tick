QUESTION_PROMPT = """
You will receive a string in the following format:

"Task Name: ... Task Topic: ..."

Your job is to:

1. Use the **Task Name** to frame a **formal and direct question**.
2. Fix any grammatical errors in the **Task Topic**, but do not change its meaning.
3. Return a string with:
   - The (formatted) **Task Topic** on the first line.
   - The **formal question** you created on the second line.

Do not include any additional explanation or formatting. Only return the two lines as specified.
"""
