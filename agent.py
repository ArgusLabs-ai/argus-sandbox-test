"""A tiny customer-support agent, used to try the Argus check on a pull request.

No LLM and no API key: each step is plain Python, so the result is the same on every run.

    retrieve  looks up help-center articles for the question
    answer    writes the reply from those articles

To see Argus catch a silent failure, set BROKEN = True below and open a pull request.
`retrieve` then returns no articles, `answer` still replies, every test still passes,
and the Argus check names `retrieve` as the step that broke.
"""

from typing import TypedDict

from langgraph.graph import END, StateGraph

BROKEN = False

ARTICLES = {
    "refund": "Refunds reach your card within 5 business days.",
    "shipping": "Orders ship within 2 days; tracking is emailed.",
    "password": "Reset your password from Settings > Security.",
}


class State(TypedDict, total=False):
    question: str
    documents: list
    answer: str
    sources: list


def retrieve(state: State) -> dict:
    if BROKEN:
        return {"documents": []}  # the search index came back empty, and nothing raised
    words = state["question"].lower()
    return {"documents": [text for topic, text in ARTICLES.items() if topic in words]}


def answer(state: State) -> dict:
    docs = state.get("documents") or []
    if not docs:
        return {"answer": "Thanks for reaching out! Our team will get back to you soon."}
    return {"answer": " ".join(docs), "sources": docs}


def build():
    graph = StateGraph(State)
    graph.add_node("retrieve", retrieve)
    graph.add_node("answer", answer)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)
    return graph.compile(name="support-agent")


app = build()
