QUESTION_PROMPT = """
You will be provided with a sentence.

Your task is to:

Analyze the sentence and convert it into a formal, precise, and concise question, ensuring:

- The question is grammatically correct and uses formal language.
- It accurately reflects the meaning of the original sentence.
- It is focused and avoids unnecessary words or ambiguity.
- No additional information or assumptions are added.

Return a single string as output, which:

- Contains only the formal question you constructed.
- Does not include quotes, user IDs, or any additional characters.
- Contains no extra formatting, commentary, or line breaks—just the question in one continuous string.

Output Format Example:
Input: I need help understanding how to install the software  
Output: How can I install the software?

Important Constraints:

- Only return the question string.
- Do not include explanations, formatting, or identifiers.
- Do not return a list or JSON structure.
"""
