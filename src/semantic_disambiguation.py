import pandas as pd

def load_cilin(cilin_path):
    cilin_dict = {}
    with open(cilin_path, 'r', encoding='GBK') as file:  # 使用GBK编码
        for line in file:
            parts = line.strip().split('=')
            if len(parts) > 1:
                words = parts[1].split()
                for word in words:
                    if word not in cilin_dict:
                        cilin_dict[word] = set()
                    cilin_dict[word].update(words)

    return cilin_dict



def calculate_similarity_with_cilin(content, relation, cilin_dict):
    content_words = set(content.split())
    relation_words = set(relation.split())
    for word in content_words:
        if word in cilin_dict:
            synonyms = cilin_dict[word]
            if synonyms & relation_words:
                return True  # 找到相似的同义词
    return False

def process_csv(csv_file, output_file, cilin_dict, threshold=0.9, positive_threshold=0.915):
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, encoding='GBK')  # 尝试使用GBK编码

    df['Classification'] = 'Negative'  # 默认为负例

    for index, row in df.iterrows():
        if row['Non-Entity Content&Subclass Relation Similarity Score'] < threshold:
            is_positive = calculate_similarity_with_cilin(row['Extracted Non-Entity Content'], row['Relation'], cilin_dict)
            df.at[index, 'Classification'] = 'Positive' if is_positive else 'Negative'
        elif row['Non-Entity Content&Subclass Relation Similarity Score'] >= positive_threshold:
            df.at[index, 'Classification'] = 'Positive'

    df.to_csv(output_file, index=False)



cilin_dict = load_cilin('cilin.txt')
process_csv('output.csv', 'final.csv', cilin_dict)
