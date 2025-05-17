from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def RetrievalQAChain(llm, prompt, db, text):
    vectorstore_retriever = db.as_retriever(
        search_kwargs={"k": 5}, search_type="similarity"
    )

    qa_chain = (
        {
            "context": vectorstore_retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return qa_chain
