# Guest Agent [Alfred] – Modular Agent Framework Demo - HuggingFace Agents Course

A concise, production‑style reference implementation of a **tool‑calling conversational agent** built with [LangChain](https://python.langchain.com/) ≥ 0.1, [LangGraph](https://langchain-ai.github.io/langgraph/), and OpenAI’s chat completion API.  The codebase shows how to:

* Orchestrate a multi‑tool workflow through a state graph rather than a traditional sequential chain.
* Bind LangChain tools directly to an OpenAI model to exploit function‑calling semantics.
* Retrieve domain‑specific knowledge with a lightweight BM25 text index (no embeddings required).
* Cleanly separate concerns—data loading, retrieval, tool wrappers, and agent logic—in a way that scales.

## Features

| Capability                         | Implementation                                                                              | File(s)                               |
| ---------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------- |
| **Natural‑language orchestration** | `ChatOpenAI` bound to tool schema via `bind_tools`                                          | `agent.py`                            |
| **Graph‑based control flow**       | Two‑node [`StateGraph`](https://langgraph-ai.github.io/langgraph/) with conditional routing | `agent.py`                            |
| **Domain retrieval**               | BM25 index over invitee dataset                                                             | `data_loader.py`, `retriever_tool.py` |
| **External search**                | DuckDuckGo run wrapper                                                                      | `tools.py`                            |
| **Weather stub**                   | Deterministic "dummy" weather service (illustrative placeholder)                            | `tools.py`                            |
| **Model analytics**                | Hugging Face Hub query to surface download statistics                                       | `tools.py`                            |

## Repository Layout

```text
.
├── agent.py           # Graph definition and driver script
├── data_loader.py     # Downloads & normalises the invitee dataset
├── retriever_tool.py  # BM25 retriever + LangChain Tool wrapper
├── tools.py           # Additional tools: search, weather, HF Hub stats
├── data.txt           # Example invitee records (small, local subset)
└── README.md          # You are here
```

*No hidden magic: the entry point is `agent.py`; everything else is imported explicitly.*

## Quick Start

### Prerequisites

* Python 3.10 – 3.12
* An OpenAI account with an **API key** (`OPENAI_API_KEY`)

```bash
# Clone repository
$ git clone https://github.com/your‑org/alfred‑agent.git
$ cd alfred‑agent

# (Optional) create isolated environment
$ python -m venv .venv && source .venv/bin/activate

# Install runtime dependencies
$ pip install -r requirements.txt

# Run the demo conversation
$ export OPENAI_API_KEY="sk‑..."
$ python agent.py
```

The script spins up the graph, injects a few sample user queries, and prints the agent’s responses to stdout.

## Architecture

```
┌────────────┐   initial state   ┌────────────┐
│   START    │ ────────────────▶ │ Assistant  │
└────────────┘                   └────┬───────┘
                                      │ needs tool?
                         ┌────────────┴────────────┐
                         │           yes            │
                         ▼                         ▼
                    ┌────────┐               ┌────────┐
                    │  Tool  │──────────────▶│ Return │
                    │  Node  │◀──────────────┤  to    │
                    └────────┘               │Assistant│
                                             └────────┘
```

* **Assistant Node** – calls OpenAI with the full conversation context.  If the model proposes a function call, control flows to the Tool Node; otherwise the assistant responds directly.
* **Tool Node** – resolves the requested function, executes it, and appends the result to the message list.  Control then loops back to the assistant for final synthesis.

The pattern scales to arbitrarily many specialised nodes without entangling dialogue logic with tool execution details.

## Extending the Agent

1. **Add a new tool** – create a callable that follows the LangChain Tool protocol and append it to the `tools` list in `agent.py`.  The assistant will auto‑discover the schema on the next run.
2. **Swap the LLM** – change `model_name` (e.g. `gpt‑4o`) or point to an Azure deployment; the wrapper is already abstracted.
3. **Replace BM25 with embeddings** – substitute `BM25Retriever` with `VectorstoreRetriever` and drop in your favourite embedding model.
4. **Advance control flow** – LangGraph supports branching, retries, and timeouts; customise the `StateGraph` to match production needs.

## License

Distributed under the MIT license.  See `LICENSE` for details.
