from flask import Flask, render_template, request
from engine.search_engine import SearchEngine

from benchmark.benchmark import (
    benchmark_search_algorithms,
    benchmark_retrieval_algorithms,
    benchmark_ranking_algorithms
)

app = Flask(__name__)

# -----------------------------
# Initialize Search Engine
# -----------------------------

DATA_PATH = "data/documents.json"
search_engine = SearchEngine(DATA_PATH)

# -----------------------------
# Run benchmarks once at startup
# -----------------------------

bench_search = benchmark_search_algorithms()
bench_retrieval = benchmark_retrieval_algorithms()
bench_ranking = benchmark_ranking_algorithms()

# -----------------------------
# Home / Search Route
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    trace = []
    ranking_analysis = {}
    query = ""
    ranking = "minheap"
    top_k = 5

    if request.method == "POST":

        # Get the user's search query
        query = request.form.get("query", "").strip()

        # Get ranking algorithm selected by the user
        ranking = request.form.get("ranking", "minheap")

        # Get Top-K selected by the user
        try:
            top_k = int(request.form.get("top_k", 5))
        except ValueError:
            top_k = 5

        if query:

            # Convert frontend value to backend ranking name
            if ranking == "minheap":
                ranking_method = "heap"

            elif ranking == "merge":
                ranking_method = "merge"

            elif ranking == "quick":
                ranking_method = "quick"

            else:
                ranking_method = "heap"

            # Run search and receive results + algorithm trace
            results, trace = search_engine.search(
                query,
                ranking_method=ranking_method,
                top_k=top_k
            )

            ranking_analysis = search_engine.explain_ranking(
                query,
                results,
                ranking_method,
                top_k
            )

    return render_template(
        "index.html",
        query=query,
        results=results,
        documents=search_engine.document_map,
        ranking=ranking,
        top_k=top_k,
        ranking_analysis=ranking_analysis,

        # Benchmark data
        bench_search=bench_search,
        bench_retrieval=bench_retrieval,
        bench_ranking=bench_ranking,

        # Live algorithm trace
        trace=trace
    )


# -----------------------------
# Run Application
# -----------------------------

@app.route("/document/<int:doc_id>")
def document(doc_id):

    document = search_engine.document_map.get(doc_id)

    if document is None:
        return "Document not found", 404

    return render_template(
        "document.html",
        document=document,
        documents = search_engine.document_map
    )


if __name__ == "__main__":
    app.run(debug=True)