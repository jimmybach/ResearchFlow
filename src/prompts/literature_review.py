from langchain_core.prompts import ChatPromptTemplate

synthesize_literature_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a public health research assistant. 
        Create a structured first-pass literature review
        for the following research question and paper summaries.
        Rules:
        - Be concise.
        - Do not invent findings not supported by the retrieved papers.
         -Identify major themes among the papers. Aim for 3-5 total thematic groupings.
        - If evidence is limited, say so.
        - Separate consensus findings from conflicting or uncertain evidence.
        - Identify research gaps and useful next search directions.
        """),

        ("user", """Research question:
        {question}

        Paper summaries:
        {paper_summaries}""")
    ]
)