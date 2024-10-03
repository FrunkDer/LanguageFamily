import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from Levenshtein import distance as levenshtein_distance
from sklearn.preprocessing import normalize

class SentenceSimilarity:
    def __init__(self, weight_cosine=0.5, weight_levenshtein=0.5):
        self.weight_cosine = weight_cosine
        self.weight_levenshtein = weight_levenshtein

    def calculate_levenshtein(self, word1, word2):
        return levenshtein_distance(word1, word2)

    def compute_normalized_levenshtein(self, word1, word2):
        distance = self.calculate_levenshtein(word1, word2)
        max_len = max(len(word1), len(word2))
        return 1 - (distance / max_len) if max_len > 0 else 0

    def combine_similarities(self, cosine_sim, levenshtein_sim):
        return (self.weight_cosine * cosine_sim) + (self.weight_levenshtein * levenshtein_sim)

    def sentence_similarity(self, sentence1, sentence2):
        words_lang1 = sentence1.split()
        words_lang2 = sentence2.split()

        # Tokenization and n-grams
        vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=(2, 4))
        X = vectorizer.fit_transform([' '.join(words_lang1), ' '.join(words_lang2)])
        X_lang1 = X[0:1]
        X_lang2 = X[1:2]

        # Cosine similarity
        cosine_similarities = cosine_similarity(X_lang1, X_lang2)[0][0]

        # Initialize matrix for Levenshtein similarities
        levenshtein_similarities = np.zeros((len(words_lang1), len(words_lang2)))

        # Compute pairwise Levenshtein distances and normalize
        for i, word1 in enumerate(words_lang1):
            for j, word2 in enumerate(words_lang2):
                levenshtein_similarities[i, j] = self.compute_normalized_levenshtein(word1, word2)

        # Combine Levenshtein and Cosine similarities
        combined_similarities = np.zeros((len(words_lang1), len(words_lang2)))
        for i in range(len(words_lang1)):
            for j in range(len(words_lang2)):
                combined_similarities[i, j] = self.combine_similarities(cosine_similarities, levenshtein_similarities[i, j])

        # Sum top similarities
        num_similarities = min(len(words_lang1) * len(words_lang2), 10)
        top_similarities = np.sort(combined_similarities.flatten())[-num_similarities:]
        sentence_similarity_score = np.sum(top_similarities)

        return sentence_similarity_score

# from sentence_transformers import SentenceTransformer, util
# import torch

# class SentenceSimilarity:
#     def __init__(self):
#         self.model = SentenceTransformer('all-MiniLM-L6-v2')
#         self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
#         self.model.to(self.device)

#     def sentence_similarity(self, sentence1, sentence2):
#         # Encode sentences to get their embeddings
#         embeddings1 = self.model.encode(sentence1, convert_to_tensor=True, device=self.device)
#         embeddings2 = self.model.encode(sentence2, convert_to_tensor=True, device=self.device)
        
#         # Compute cosine similarity
#         similarity_score = util.pytorch_cos_sim(embeddings1, embeddings2).item()
        
#         return similarity_score * 10

