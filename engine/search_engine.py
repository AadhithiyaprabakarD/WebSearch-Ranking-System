import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import json

from algorithms.preprocessing import tokenize
from algorithms.inverted_index import InvertedIndex
from algorithms.retrieval import RetrievalAlgorithms
from algorithms.tfidf import TFIDFRanker
from algorithms.sorting import SortingAlgorithms
from algorithms.min_heap import MinHeapTopK


class SearchEngine:

    def __init__(self, data_path):
        # Load documents
        with open(data_path, "r", encoding="utf-8") as file:
            self.documents = json.load(file)

        # Build inverted index
        self.index = InvertedIndex()
        self.index.build(self.documents)

        # Create TF-IDF ranker
        self.ranker = TFIDFRanker(
            self.documents,
            self.index
        )

        # Store documents for quick access
        self.document_map = {
            document["id"]: document
            for document in self.documents
        }

    def retrieve_documents(self, query_terms):
        if not query_terms:
            return []

        # Build the posting list for the first query term
        matched_terms = self.index.search_prefix(query_terms[0])

        if not matched_terms:
            return []

        term_documents = set()

        for matched_term in matched_terms:
            posting_list = self.index.search_term(matched_term)

            for doc_id, tf in posting_list:
                term_documents.add(doc_id)

        # Convert document IDs into sorted posting-list format
        candidate_list = [
            (doc_id, 1)
            for doc_id in sorted(term_documents)
        ]

        # Intersect with remaining query terms using Two-Pointer
        for query_term in query_terms[1:]:

            matched_terms = self.index.search_prefix(query_term)

            if not matched_terms:
                return []

            term_documents = set()

            for matched_term in matched_terms:
                posting_list = self.index.search_term(matched_term)

                for doc_id, tf in posting_list:
                    term_documents.add(doc_id)

            current_list = [
                (doc_id, 1)
                for doc_id in sorted(term_documents)
            ]

            # Actual Two-Pointer Intersection
            intersection = RetrievalAlgorithms.two_pointer_intersection(
                candidate_list,
                current_list
            )

            # Keep only document IDs for the next iteration
            candidate_list = [
                (doc_id, 1)
                for doc_id, tf_a, tf_b in intersection
            ]

            if not candidate_list:
                return []

        return [doc_id for doc_id, tf in candidate_list]

    def search(self, query, ranking_method="merge", top_k=None):

        # -----------------------------
        # Algorithm Trace
        # -----------------------------
        trace = []
    
        # Step 1: preprocess query
        query_terms = tokenize(query)
    
        if not query_terms:
            return [], trace
    
        trace.append({
            "stage": "Query Preprocessing",
            "message": f"{len(query_terms)} query term(s) detected",
            "complexity": "O(Q)"
        })
    
        # Step 2: term lookup
        for term in query_terms:
            matched_terms = self.index.search_prefix(term)
    
            trace.append({
                "stage": "Term Lookup",
                "message": f'"{term}" → {len(matched_terms)} matching vocabulary term(s)',
                "complexity": "O(log V + M)"
            })
    
        # Step 3: retrieve candidate documents
        candidate_ids = self.retrieve_documents(query_terms)
    
        if not candidate_ids:
            trace.append({
                "stage": "Document Retrieval",
                "message": "No matching documents found",
                "complexity": "O(P)"
            })
            return [], trace
    
        trace.append({
            "stage": "Document Retrieval",
            "message": f"Two-Pointer Intersection → {len(candidate_ids)} candidate document(s)",
            "complexity": "O(P)"
        })
    
        # Step 4: calculate TF-IDF scores
        scored_results = []
    
        for doc_id in candidate_ids:
            score = self.ranker.calculate_score(
                query_terms,
                doc_id
            )
    
            scored_results.append(
                (doc_id, score)
            )
    
        trace.append({
            "stage": "TF-IDF Scoring",
            "message": f"Scored {len(scored_results)} candidate document(s)",
            "complexity": "O(P)"
        })
    
        # Step 5: rank results
        if ranking_method == "merge":
        
            ranked_results = SortingAlgorithms.merge_sort(
                scored_results
            )
    
            ranking_name = "Merge Sort"
            ranking_complexity = "O(R log R)"
    
        elif ranking_method == "quick":
        
            ranked_results = SortingAlgorithms.quick_sort(
                scored_results
            )
    
            ranking_name = "Quick Sort"
            ranking_complexity = "O(R log R) average"
    
        elif ranking_method == "heap":
        
            if top_k is None:
                top_k = 5
    
            heap = MinHeapTopK(top_k)
    
            for result in scored_results:
                heap.push(result)
    
            ranked_results = heap.get_top_k()
    
            ranking_name = "Min-Heap Top-K"
            ranking_complexity = "O(R log K)"
    
        else:
            raise ValueError(
                "Invalid ranking method. "
                "Use 'merge', 'quick', or 'heap'."
            )
    
        trace.append({
            "stage": "Ranking",
            "message": f"{ranking_name} selected",
            "complexity": ranking_complexity
        })
    
        # Step 6: apply top-k limit
        if top_k is not None:
            ranked_results = ranked_results[:top_k]
    
            trace.append({
                "stage": "Top-K Selection",
                "message": f"Returning top {top_k} result(s)",
                "complexity": "O(K)"
            })
    
        return ranked_results, trace

    def explain_ranking(self, query, ranked_results, ranking_method, top_k):
        query_terms = tokenize(query)
    
        analysis = {}
    
        for doc_id, final_score in ranked_results:
            contributions = []
            matched_terms = []
    
            for query_term in query_terms:
                matched_vocabulary_terms = self.index.search_prefix(query_term)
    
                for term in matched_vocabulary_terms:
                    tf = self.ranker.calculate_tf(term, doc_id)
    
                    if tf == 0:
                        continue
                    
                    idf = self.ranker.calculate_idf(term)
                    contribution = tf * idf
    
                    matched_terms.append(term)
    
                    contributions.append({
                        "term": term,
                        "tf": tf,
                        "idf": idf,
                        "contribution": contribution
                    })
    
            analysis[doc_id] = {
                "matched_terms": sorted(set(matched_terms)),
                "contributions": contributions,
                "final_score": final_score,
                "ranking_algorithm": {
                    "heap": "Min-Heap Top-K",
                    "merge": "Merge Sort",
                    "quick": "Quick Sort"
                }.get(ranking_method, ranking_method),
                "complexity": {
                    "heap": "O(R log K)",
                    "merge": "O(R log R)",
                    "quick": "O(R log R) average"
                }.get(ranking_method, "N/A"),
                "top_k": top_k
            }
    
        return analysis

    def display_results(self, results):

        if not results:
            print("\nNo results found.")
            return

        print("\nSEARCH RESULTS")
        print("=" * 50)

        for rank, (doc_id, score) in enumerate(
            results,
            start=1
        ):
            document = self.document_map[doc_id]

            print(
                f"\n{rank}. {document['title']}"
            )

            print(
                f"   Document ID: {doc_id}"
            )

            print(
                f"   TF-IDF Score: {score:.6f}"
            )

            print(
                f"   {document['content']}"
            )


if __name__ == "__main__":

    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    data_path = os.path.join(
        project_root,
        "data",
        "documents.json"
    )

    engine = SearchEngine(data_path)

    query = "n"
    

    results = engine.search(
        query,
        ranking_method="merge",
        top_k=5
    )

    print("\nQUERY:", query)

    engine.display_results(results)