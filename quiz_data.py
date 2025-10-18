"""
quiz_data.py

Question bank and helper functions for the Kodland quiz application.

This module provides:
- 'questions': a list of question dictionaries used by the quiz UI. Each dict contains:
    - 'text': the question string
    - 'options': list of answer option strings
    - 'answer': the correct answer string (used to compute the correct index after shuffling)
- '_asked_questions': internal tracker of question texts already served in the current cycle.
- 'get_random_question()': returns a single question with shuffled options and the index of the correct answer.
- 'total_questions()': returns the count of available questions.

Notes:
- Options are shuffled for presentation; the original 'answer' value is used to compute the 'correct' index.
- The returned 'id' is an ephemeral random integer (1000-9999) and should not be treated as a persistent identifier.
"""

import random

# Base question set (teenager leve, include HOTS type questions)
# NLP Quiz Question Set
questions = [
    {
        "text": "You have a sentiment analysis model trained on movie reviews. It performs poorly on tweets. What is the most likely cause?",
        "options": [
            "Domain shift due to different vocabulary and style",
            "The model is overfitting the training data",
            "Tweets are too short for NLP models",
            "The tokenizer cannot handle hashtags",
        ],
        "answer": "Domain shift due to different vocabulary and style",
    },
    {
        "text": "Two sentences have identical Bag-of-Words vectors but different meanings. What does this reveal about the model?",
        "options": [
            "It fails to capture word order and context",
            "It has too many layers",
            "It overfits to specific words",
            "It ignores rare words",
        ],
        "answer": "It fails to capture word order and context",
    },
    {
        "text": "Which technique would improve sarcasm detection in social media text?",
        "options": [
            "Use contextual embeddings like BERT",
            "Increase stopword removal",
            "Train on only long sentences",
            "Use aggressive lemmatization",
        ],
        "answer": "Use contextual embeddings like BERT",
    },
    {
        "text": "You need a translation system for multiple languages. Why choose a shared encoder-decoder over separate models?",
        "options": [
            "Enables cross-lingual transfer and parameter sharing",
            "No tokenization is required",
            "Faster training on individual languages",
            "Simpler preprocessing",
        ],
        "answer": "Enables cross-lingual transfer and parameter sharing",
    },
    {
        "text": "During text preprocessing, which step could remove meaningful political context if done carelessly?",
        "options": [
            "Stopword removal",
            "Lowercasing text",
            "Removing punctuation",
            "Trimming short words",
        ],
        "answer": "Stopword removal",
    },
    {
        "text": "Why might freezing lower layers of BERT and fine-tuning higher layers reduce overfitting on small datasets?",
        "options": [
            "Lower layers capture general language knowledge; higher layers adapt to task",
            "It speeds up training significantly",
            "Prevents gradient vanishing",
            "Reduces vocabulary size",
        ],
        "answer": "Lower layers capture general language knowledge; higher layers adapt to task",
    },
    {
        "text": "You are building a chatbot that understands both intent and emotion. Which architecture is most suitable?",
        "options": [
            "Transformer-based intent classifier + sentiment analysis model",
            "Rule-based keyword matching",
            "POS tagging with Word2Vec",
            "LSTM-based summarizer",
        ],
        "answer": "Transformer-based intent classifier + sentiment analysis model",
    },
    {
        "text": "A Transformer outperforms an RNN on long texts. Why?",
        "options": [
            "Models global dependencies without sequential limitations",
            "Has fewer parameters",
            "Uses convolution layers",
            "Ignores word order completely",
        ],
        "answer": "Models global dependencies without sequential limitations",
    },
    {
        "text": "Your NLP model achieves high accuracy but high perplexity. What does this indicate?",
        "options": [
            "It is less confident in its predictions despite accuracy",
            "It generalizes better",
            "It was trained on more data",
            "It has lower cross-entropy loss",
        ],
        "answer": "It is less confident in its predictions despite accuracy",
    },
    {
        "text": "Which strategy helps handle class imbalance in hate speech detection datasets?",
        "options": [
            "Oversampling or weighted loss functions",
            "Removing rare classes",
            "Training longer on the same data",
            "Reducing vocabulary size",
        ],
        "answer": "Oversampling or weighted loss functions",
    },
    {
        "text": "What is zero-shot learning in NLP?",
        "options": [
            "Making predictions without task-specific training",
            "Training without data",
            "Evaluating without validation",
            "Testing on identical data",
        ],
        "answer": "Making predictions without task-specific training",
    },
    {
        "text": "Why might contextual embeddings like BERT perform better than Word2Vec on sentiment analysis?",
        "options": [
            "They capture context-dependent meaning",
            "They have smaller vector sizes",
            "They ignore rare words",
            "They reduce dimensionality",
        ],
        "answer": "They capture context-dependent meaning",
    },
    {
        "text": "A multilingual translation system uses a shared encoder. What is the key advantage?",
        "options": [
            "Leverages knowledge across languages",
            "No preprocessing is needed",
            "Faster per-language training",
            "Smaller vocabulary per language",
        ],
        "answer": "Leverages knowledge across languages",
    },
    {
        "text": "Why might a transformer-based summarizer outperform an RNN-based one?",
        "options": [
            "Better at capturing long-range dependencies",
            "Requires less memory",
            "Uses fewer parameters",
            "Processes sequentially only",
        ],
        "answer": "Better at capturing long-range dependencies",
    },
    {
        "text": "If a model misclassifies sarcastic reviews, which approach improves understanding?",
        "options": [
            "Incorporate context-aware embeddings",
            "Remove stopwords aggressively",
            "Only train on positive sentences",
            "Use bag-of-words vectors",
        ],
        "answer": "Incorporate context-aware embeddings",
    },
    {
        "text": "Why is positional encoding important in transformers?",
        "options": [
            "Adds information about word order",
            "Normalizes embeddings",
            "Reduces dimensions",
            "Identifies stopwords",
        ],
        "answer": "Adds information about word order",
    },
    {
        "text": "Two sentences have identical embeddings but different sentiment. What does this suggest?",
        "options": [
            "Embedding fails to capture subtle differences",
            "Vocabulary is too large",
            "Model is overfitting",
            "It uses RNN instead of Transformer",
        ],
        "answer": "Embedding fails to capture subtle differences",
    },
    {
        "text": "Which method would best improve machine translation quality on low-resource languages?",
        "options": [
            "Transfer learning from high-resource languages",
            "Training separate monolingual models",
            "Using only bag-of-words features",
            "Ignoring rare words",
        ],
        "answer": "Transfer learning from high-resource languages",
    },
    {
        "text": "Why is fine-tuning important when using pre-trained language models?",
        "options": [
            "Adapts general knowledge to a specific task",
            "Reduces vocabulary size",
            "Speeds up tokenization",
            "Prevents any training errors",
        ],
        "answer": "Adapts general knowledge to a specific task",
    },
    {
        "text": "When a sentiment model fails on slang words, which solution helps most?",
        "options": [
            "Update tokenizer and embeddings with social media data",
            "Remove stopwords",
            "Train only on formal text",
            "Increase hidden layers",
        ],
        "answer": "Update tokenizer and embeddings with social media data",
    },
        {
        "text": "What does NLP stand for in AI?",
        "options": [
            "Neuro-Linguistic Programming",
            "Natural Language Processing",
            "Network Language Parser",
            "Neural Logic Processor",
        ],
        "answer": "Natural Language Processing",
    },
    {
        "text": "Which Python library is often used to work with text in NLP?",
        "options": ["NumPy", "NLTK", "OpenCV", "Matplotlib"],
        "answer": "NLTK",
    },
    {
        "text": "What is the full name of NLTK?",
        "options": [
            "Natural Language Toolkit",
            "Neural Language Tool Kit",
            "Network Logic Testing Kit",
            "Natural Logic Token Kit",
        ],
        "answer": "Natural Language Toolkit",
    },
    {
        "text": "Which method helps computers understand words as numbers?",
        "options": ["Bag of Words", "Word2Vec", "TF-IDF", "Counting Words"],
        "answer": "Word2Vec",
    },
    {
        "text": "What does tokenization do?",
        "options": [
            "Breaks text into words or sentences",
            "Removes punctuation",
            "Makes text lowercase",
            "Counts words",
        ],
        "answer": "Breaks text into words or sentences",
    },
    {
        "text": "Which library has ready-made AI models like BERT and GPT?",
        "options": ["Scikit-learn", "Hugging Face Transformers", "Pandas", "OpenCV"],
        "answer": "Hugging Face Transformers",
    },
    {
        "text": "What are stopwords?",
        "options": [
            "Common words like 'the', 'is', 'and' that we sometimes ignore",
            "Rare words in a text",
            "Numbers in the text",
            "Punctuation marks",
        ],
        "answer": "Common words like 'the', 'is', 'and' that we sometimes ignore",
    },
    {
        "text": "Which is an example of stemming?",
        "options": [
            "running → run",
            "better → good",
            "cats → cat",
            "went → go",
        ],
        "answer": "running → run",
    },
    {
        "text": "What does TF-IDF help with?",
        "options": [
            "Finding important words in documents",
            "Counting all letters",
            "Sorting words alphabetically",
            "Making text lowercase",
        ],
        "answer": "Finding important words in documents",
    },
    {
        "text": "Which model helps translate one language to another?",
        "options": ["BERT", "GPT", "Seq2Seq", "Naive Bayes"],
        "answer": "Seq2Seq",
    },
    {
        "text": "What is lemmatization?",
        "options": [
            "Turning words into their base form (e.g., 'running' → 'run')",
            "Removing punctuation",
            "Making words lowercase",
            "Removing numbers",
        ],
        "answer": "Turning words into their base form (e.g., 'running' → 'run')",
    },
    {
        "text": "Which technique turns text into a list of numbers showing word frequency?",
        "options": ["Bag of Words", "Word2Vec", "FastText", "ELMo"],
        "answer": "Bag of Words",
    },
    {
        "text": "Which algorithm can tell if a sentence is positive or negative?",
        "options": ["Naive Bayes", "K-Means", "PCA", "SVM Regression"],
        "answer": "Naive Bayes",
    },
    {
        "text": "POS tagging stands for what?",
        "options": [
            "Part of Speech tagging",
            "Position of Sentence tagging",
            "Probability of Syntax tagging",
            "Parsing of Semantics tagging",
        ],
        "answer": "Part of Speech tagging",
    },
    {
        "text": "What does named entity recognition (NER) do?",
        "options": [
            "Finds names, places, and dates in text",
            "Translates text",
            "Summarizes text",
            "Finds if text is happy or sad",
        ],
        "answer": "Finds names, places, and dates in text",
    },
    {
        "text": "Which model can write new text like stories or chat responses?",
        "options": ["BERT", "GPT-3", "RoBERTa", "XLNet"],
        "answer": "GPT-3",
    },
    {
        "text": "What is word embedding?",
        "options": [
            "Turning words into numbers so computers can understand them",
            "Splitting text into words",
            "Removing common words",
            "Sorting words alphabetically",
        ],
        "answer": "Turning words into numbers so computers can understand them",
    },
    {
        "text": "Which type of neural network is often used for text?",
        "options": ["CNN", "RNN", "GAN", "Autoencoder"],
        "answer": "RNN",
    },
    {
        "text": "What's a downside of Bag of Words?",
        "options": [
            "It ignores the order of words",
            "It’s slow to compute",
            "It works only in English",
            "It removes common words automatically",
        ],
        "answer": "It ignores the order of words",
    },
]

_asked_questions = []

def get_random_question():
    """Return one random question with shuffled options.
    If all questions have been used, reset the cycle.
    """
    global _asked_questions

    # Reset if all questions are used
    if len(_asked_questions) == len(questions):
        _asked_questions.clear()

    # Pick random unused question
    available = [q for q in questions if q["text"] not in _asked_questions]
    q = random.choice(available)

    # Mark as used
    _asked_questions.append(q["text"])

    # Shuffle options
    opts = q["options"].copy()
    random.shuffle(opts)

    # Correct index must match shuffled options
    correct_idx = opts.index(q["answer"])

    return {
        "id": random.randint(1000, 9999),  # temporary unique ID
        "question": q["text"],
        "options": opts,
        "correct": correct_idx,
    }

def total_questions():
    return len(questions)

