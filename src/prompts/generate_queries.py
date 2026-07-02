from langchain_core.prompts import ChatPromptTemplate

generate_queries_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert medical researcher and literature review assistant."),
        ("user", """Generate 5 diverse PubMed search queries for the following research question:
         \n\n{question}"""),

    ]
)