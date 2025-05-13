from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from config import RAG_MODEL
from utils.state import State

RAG_PROMPT = """\
You are a helpful assistant specializing in AI evaluation and research papers analysis. Your task is to answer questions based ONLY on the provided context. If the context doesn't contain the information needed, acknowledge that limitation rather than making up information.

### Question
{question}

### Context
{context}

Based on the above context only, provide a comprehensive answer. Include specific details from the research papers when relevant. If the question cannot be answered from the context, clearly state that the information is not available in the provided documents.
"""

def create_rag_graph(retriever):
    """Create a RAG graph that uses a retriever to answer questions."""
    rag_prompt = ChatPromptTemplate.from_template(RAG_PROMPT)
    llm = ChatOpenAI(model=RAG_MODEL)
    
    def retrieve(state):
        retrieved_docs = retriever.invoke(state["question"])
        return {"context": retrieved_docs}
    
    def generate(state):
        # Extract document content and include document identifiers
        doc_contents = []
        for i, doc in enumerate(state["context"]):
            # Include document identifier in the content for reference
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            doc_id = metadata.get('id', f'doc_{i}')
            doc_contents.append(f"Document {doc_id}:\n{doc.page_content}")
            
        # Join all document contents with clear separation
        docs_content = "\n\n" + "\n\n---\n\n".join(doc_contents)
        
        # Format messages with question and context
        messages = rag_prompt.format_messages(question=state["question"], context=docs_content)
        response = llm.invoke(messages)
        return {"response": response.content}
    
    # Create graph with individual nodes and edges instead of using add_sequence
    graph_builder = StateGraph(State)
    
    # Add nodes individually
    graph_builder.add_node("retrieve", retrieve)
    graph_builder.add_node("generate", generate)
    
    # Add edges individually
    graph_builder.add_edge(START, "retrieve")
    graph_builder.add_edge("retrieve", "generate")
    graph_builder.add_edge("generate", END)
    
    return graph_builder.compile()