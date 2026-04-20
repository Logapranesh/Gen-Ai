from langgraph.graph import StateGraph

def build_graph():

    graph = StateGraph(dict)

    def classify_intent(state):
        return state

    def retrieve_documents(state):
        return state

    def web_search(state):
        return state

    def generate_response(state):
        return state

    def save_note(state):
        return state

    graph.add_node("classify", classify_intent)
    graph.add_node("retrieve", retrieve_documents)
    graph.add_node("web", web_search)
    graph.add_node("generate", generate_response)
    graph.add_node("save", save_note)

    graph.set_entry_point("classify")

    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", "save")

    return graph.compile()