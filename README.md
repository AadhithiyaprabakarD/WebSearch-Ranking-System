# WebRank — Web Search Ranking System

A data-structure-driven web search ranking system that demonstrates how searching, indexing, retrieval, information retrieval, and ranking algorithms can be combined to build a functional search engine.

## 🚀 Live Demo

**WebRank:** https://websearch-ranking-system.onrender.com

## 📌 Project Overview

WebRank is a web-based search engine designed to demonstrate the practical application of Data Structures and Algorithms in information retrieval.

The system accepts a user query, preprocesses the query terms, searches an inverted index, retrieves relevant documents, calculates TF-IDF relevance scores, and ranks the results using different ranking algorithms.

The project also provides an interactive algorithm dashboard that exposes the processing pipeline and theoretical complexity of the algorithms used.

## 🔄 System Architecture


                    User Query
                        │
                        ▼
              Query Preprocessing
                        │
                        ▼
                 Term Lookup
              ┌─────────┼─────────┐
              ▼         ▼         ▼
           Linear    Binary      Hash
           Search    Search     Search
                        │
                        ▼
                 Inverted Index
                        │
                        ▼
               Document Retrieval
                        │
                        ▼
             Two-Pointer Intersection
                        │
                        ▼
                  TF-IDF Scoring
                        │
                        ▼
                    Ranking
              ┌─────────┼──────────┐
              ▼         ▼          ▼
          Merge Sort  Quick Sort  Min-Heap
                                   Top-K
                        │
                        ▼
                 Ranked Results
                        │
                        ▼
                    Web UI



## ✨ Features
🔎 Search across a 100-document dataset
⚡ Hash-based term lookup
🔍 Linear and binary search comparison
📚 Inverted index for document retrieval
🔗 Two-pointer posting-list intersection
📊 TF-IDF relevance scoring
🏆 Merge Sort, Quick Sort, and Min-Heap Top-K ranking
🎯 Configurable Top-K results
📈 Algorithm benchmarking
🧠 Live algorithm execution trace
📋 Ranking analysis for individual documents
📖 Wikipedia-inspired article pages
🔗 Related article navigation
🌐 Publicly deployed web application

## 🧠 Algorithms and Data Structures
1. Inverted Index

The inverted index maps each term to a posting list containing the documents in which the term occurs.

Term → [(Document ID, Term Frequency), ...]

This avoids scanning every document for every query.

Average lookup: O(1) using hash-based access.

2. Linear Search

Linear search checks vocabulary terms sequentially until the target term is found.

Complexity: O(V)

where V is the vocabulary size.

It is included as a baseline for comparison.

3. Binary Search

Binary search operates on the sorted vocabulary.

Complexity: O(log V)

It significantly reduces the number of comparisons compared with linear search.

4. Hash Search

The inverted index is implemented using a hash table.

Average complexity: O(1)

Worst case: O(V)

Hash search is used as the primary exact term lookup mechanism.

5. Two-Pointer Intersection

Posting lists are stored in sorted document-ID order.

The two-pointer algorithm traverses two posting lists simultaneously to find common documents.

Complexity:

O(n + m)

This is compared against the naive nested-loop intersection:

O(n × m)
6. TF-IDF

WebRank uses TF-IDF to calculate the relevance of a document to a query.

Term Frequency:

TF(t,d) = frequency of term t in document d
         ----------------------------------
         total number of terms in d

Inverse Document Frequency:

IDF(t) = log(N / df(t))

where:

N = number of documents
df(t) = number of documents containing term t

The final contribution of a term is:

TF × IDF

The contributions of matching query terms are combined to produce the document's relevance score.

7. Merge Sort

Merge Sort is used as a full-ranking baseline.

Complexity:

O(R log R)

where R is the number of candidate results.

8. Quick Sort

Quick Sort is provided as another full-ranking alternative.

Average complexity:

O(R log R)

Worst case:

O(R²)
9. Min-Heap Top-K

Instead of sorting every candidate document, WebRank can maintain a min-heap containing only the best K results.

Complexity:

O(R log K)

Space:

O(K)

This is particularly useful when K is much smaller than R.

## 📊 Benchmark Results

The following measurements were obtained from the project's benchmark module.

Search Algorithms

Vocabulary size: 10,000
Trials: 1,000

Algorithm	Execution Time
Linear Search	549.5925 μs
Binary Search	2.1330 μs
Hash Search	0.1478 μs
Retrieval Algorithms

Posting list A: 5,000
Posting list B: 5,000
Trials: 100

Algorithm	Execution Time
Naive Intersection	709,334.8270 μs
Two-Pointer	2,103.8110 μs

The benchmark demonstrates the difference between:

Naive Intersection → O(n × m)

Two-Pointer        → O(n + m)
Ranking Algorithms

Number of results: 10,000
Top-K: 10
Trials: 20

Algorithm	Execution Time
Merge Sort	31,562.0000 μs
Quick Sort	15,421.4050 μs
Min-Heap	1,519.1700 μs

The theoretical complexities are:

Merge Sort → O(R log R)

Quick Sort → O(R log R) average
             O(R²) worst case

Min-Heap   → O(R log K)

## 📈 Complexity Summary
Component	Algorithm	Complexity
Query preprocessing	Tokenization	O(Q)
Exact term lookup	Hash Search	O(1) average
Vocabulary search	Binary Search	O(log V)
Baseline vocabulary search	Linear Search	O(V)
Posting-list intersection	Two-Pointer	O(n + m)
Baseline intersection	Naive	O(n × m)
Full ranking	Merge Sort	O(R log R)
Full ranking	Quick Sort	O(R log R) average
Top-K ranking	Min-Heap	O(R log K)

Where:

Q = number of query terms
V = vocabulary size
R = number of candidate documents
K = number of requested results

## 🗂️ Project Structure
WebSearch-Ranking-System/
│
├── algorithms/
│   ├── inverted_index.py
│   ├── min_heap.py
│   ├── preprocessing.py
│   ├── retrieval.py
│   ├── searching.py
│   ├── sorting.py
│   └── tfidf.py
│
├── benchmark/
│   └── benchmark.py
│
├── data/
│   └── documents.json
│
├── engine/
│   └── search_engine.py
│
├── examples/
│   └── small_graph.py
│
├── src/
│   └── graph/
│       ├── __init__.py
│       └── directed_graph.py
│
├── static/
│   └── style.css
│
├── templates/
│   ├── document.html
│   └── index.html
│
├── tests/
│   └── test_graph.py
│
├── app.py
├── main.py
├── requirements.txt
└── .gitignore
🛠️ Technologies Used
Python
Flask
HTML
CSS
JavaScript
Chart.js
Git & GitHub
Render

## ▶️ Run Locally
1. Clone the repository
git clone https://github.com/AadhithiyaprabakarD/WebSearch-Ranking-System.git
cd WebSearch-Ranking-System
2. Create a virtual environment
python -m venv .venv
3. Activate the environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Run the application
python app.py

Open:

http://127.0.0.1:5000

## 🌐 Deployment

The application is deployed using Render.

Live application:

https://websearch-ranking-system.onrender.com

The deployment uses:

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app

## 🎯 Project Objective

The primary objective of WebRank is to demonstrate how different Data Structures and Algorithms affect the efficiency of a practical search system.

Rather than using a single search technique, the system implements and compares multiple approaches for:

Searching
Indexing
Document retrieval
Ranking
Top-K selection

This allows their theoretical complexity and measured performance to be examined within one working application.

## 🔮 Future Enhancements
Trie-based autocomplete
Larger real-world document corpus
Phrase searching
OR-query support
More advanced ranking models
Search result highlighting
Persistent benchmark history
Improved query understanding
Additional retrieval algorithms

## 👨‍💻 Project

WebRank — Web Search Ranking System

Built as a Data Structures and Algorithms project demonstrating practical algorithm selection, complexity analysis, benchmarking, and interactive visualization.
