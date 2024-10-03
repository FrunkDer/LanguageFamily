import csv
import os
from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from cognates import SentenceSimilarity
from datetime import datetime
from scipy.cluster.hierarchy import linkage

comparator = SentenceSimilarity()

# Path to your folder containing CSV files
csv_folder_path = r'C:\Users\jinfa\OneDrive\Desktop\UDHR AI\csvs'

def read_csv_and_compare(csv_folder_path, testmode):
    # Initialize a dictionary to store cumulative scores and counts
    pair_scores = defaultdict(lambda: {'total_score': 0, 'count': 0})
    if not testmode:
        # Iterate over each CSV file in the folder
        for csv_file_name in os.listdir(csv_folder_path):
            # Check if the file is a CSV
            if csv_file_name.endswith('.csv'):
                csv_file_path = os.path.join(csv_folder_path, csv_file_name)
                print(f"Article {csv_file_path[-6:-4]}")
                # Initialize an empty dictionary for this file
                data_dict = {}
                
                # Read the CSV file and populate the dictionary
                with open(csv_file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        language = row['Language']
                        text = row['Text']
                        data_dict[language] = text
                
                languages = list(data_dict.keys())
                
                # Compare
                for i in range(len(languages)):
                    lang1 = languages[i]
                    for j in range(i + 1, len(languages)):
                        lang2 = languages[j]
                        similarity_score = round(comparator.sentence_similarity(data_dict[lang1], data_dict[lang2]), 2)
                        pair = tuple(sorted([lang1, lang2]))  # Ensure lang1 < lang2 to avoid duplicates
                        pair_scores[pair]['total_score'] += similarity_score
                        pair_scores[pair]['count'] += 1

    if testmode:
        data_dict = {}
                
        # Read the CSV file and populate the dictionary
        csv_file_path = r"C:\Users\jinfa\OneDrive\Desktop\UDHR AI\csvs\csv1.csv"
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                language = row['Language']
                text = row['Text']
                data_dict[language] = text
        
        languages = list(data_dict.keys())
        
        # Compare
        for i in range(len(languages)):
            lang1 = languages[i]
            for j in range(i + 1, len(languages)):
                lang2 = languages[j]
                similarity_score = round(comparator.sentence_similarity(data_dict[lang1], data_dict[lang2]), 2)
                pair = tuple(sorted([lang1, lang2]))  # Ensure lang1 < lang2 to avoid duplicates
                print(f"Article {csv_file_path[-6:-4]}, {pair}")
                pair_scores[pair]['total_score'] += similarity_score
                pair_scores[pair]['count'] += 1
    return pair_scores

def get_average_score(pair_scores):
    #Calculate average scores
    average_scores = [(pair, pair_scores[pair]['total_score'] / pair_scores[pair]['count']) for pair in pair_scores]

    # Sort highest correlating language pairs
    average_scores.sort(key=lambda x: x[1], reverse=True)

    return average_scores

def store_results(average_scores):
    results = []
    for pair, avg_score in average_scores:
        result_line = f"Pair: {pair[0]} - {pair[1]}\nAverage Similarity: {avg_score:.2f}\n"
        results.append(result_line)
        
    return results

def create_graph(pair_scores, average_scores):
    # Create a similarity matrix for the heatmap
    languages = sorted(set(lang for pair in pair_scores for lang in pair))
    similarity_matrix = pd.DataFrame(index=languages, columns=languages).fillna(0)

    for pair, avg_score in average_scores:
        similarity_matrix.loc[pair[0], pair[1]] = avg_score
        similarity_matrix.loc[pair[1], pair[0]] = avg_score

    # Fill the diagonal with the highest possible similarity score (since a language is 100% similar to itself)
    for language in languages:
        similarity_matrix.loc[language, language] = 10

    # Standardize the similarity matrix (optional)
    similarity_matrix = (similarity_matrix - similarity_matrix.mean()) / similarity_matrix.std()

    # Use a different clustering method and metric
    methods = [
        ['average', 'euclidean'],
        ['complete', 'cosine'],
        ['complete', 'euclidean'],
    ]
    figures = []
    for method in methods:
        linkage_method = method[0]
        metric = method[1]
        try:
            # Generate the linkage matrix
            row_linkage = linkage(similarity_matrix, method=linkage_method, metric=metric)
            col_linkage = linkage(similarity_matrix.T, method=linkage_method, metric=metric)

            # Plot the clustered heatmap
            clustermap = sns.clustermap(similarity_matrix, annot=True, cmap="YlGnBu", fmt=".2f",
                                        linewidths=.5, figsize=(20, 20),
                                        row_linkage=row_linkage, col_linkage=col_linkage)
            plt.title(f'Lexical Similarity Clustermap ({linkage_method}, {metric})')
            plt.setp(clustermap.ax_heatmap.get_xticklabels(), rotation=90)  # Rotate x-axis labels for better visibility
            plt.setp(clustermap.ax_heatmap.get_yticklabels(), rotation=0)   # Ensure y-axis labels are horizontal
            plt.show()
            figures.append([clustermap.figure, linkage_method, metric])

        except Exception as e:
            print(f"Clustering failed for method={linkage_method} and metric={metric}: {e}")

    return figures
    
def save_progress(note, timestamp, results, seaborn_graphs, folder_path=r'C:\Users\jinfa\OneDrive\Desktop\UDHR AI\Updates'):
    # Create the main directory if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Create a timestamped subdirectory
    timestamp_folder_path = os.path.join(folder_path, timestamp)
    if not os.path.exists(timestamp_folder_path):
        os.makedirs(timestamp_folder_path)

    # Save the results to a text file
    results_file_path = os.path.join(timestamp_folder_path, "results.txt")
    with open(results_file_path, 'w') as results_file:
        results_file.write(note)
        results_file.write('\n\n')
        if isinstance(results, list):
            for result in results:
                results_file.write(result + "\n")
        else:
            results_file.write(results)
    
    # Save the Seaborn graph to an image file
    for graph in seaborn_graphs:
        graph_file_path = os.path.join(timestamp_folder_path, f"graph{graph[1]}{graph[2]}.png")
        graph[0].savefig(graph_file_path)
        plt.close(graph[0])  # Close the figure to free up memory

    print(f"Files successfully saved in {timestamp_folder_path}.")

pair_scores = read_csv_and_compare(csv_folder_path, testmode=False)

average_scores = get_average_score(pair_scores)

results = store_results(average_scores)

seaborn_graph = create_graph(pair_scores, average_scores)

note = '''
Frisian, Kyrgyz to latin, Baltics
'''
##SE-Asian languages

save_progress(note, datetime.now().strftime("%m-%d_%H-%M-%S"), results, seaborn_graph)
