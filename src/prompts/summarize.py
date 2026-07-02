from langchain_core.prompts import ChatPromptTemplate

summarize_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a public health research assistant. 
        Create a structured first-pass literature synthesis 
        for the following research question and retrieved papers.
        Rules:
        - Be concise.
        - Do not invent findings not supported by the retrieved papers.
        - If evidence is limited, say so.
        - Separate consensus findings from conflicting or uncertain evidence.
        - Identify research gaps and useful next search directions.
        """),

        ("user", """Research question:
        {question}

        Retrieved papers:
        {papers}""")
    ]
)