import pandas as pd
import Levenshtein
import torch
from transformers import BertTokenizer, BertModel

# 归一化编辑距离计算函数
def normalize_edit_distance(a, b):
    distance = Levenshtein.distance(str(a), str(b))
    max_distance = len(str(a)) + len(str(b))
    return distance / max_distance if max_distance > 0 else 0

def calculate_bert_similarity(text1, text2, model, tokenizer):
    text1, text2 = str(text1), str(text2)
    inputs1 = tokenizer(text1, return_tensors='pt')
    inputs2 = tokenizer(text2, return_tensors='pt')
    outputs1 = model(**inputs1)
    outputs2 = model(**inputs2)
    cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
    similarity = cos(outputs1.pooler_output, outputs2.pooler_output).item()
    return similarity


def process_files(csv_file, txt_file, output_file):
    df_csv = pd.read_csv(csv_file, encoding='gbk')
    df_txt = pd.read_csv(txt_file, names=['人物1', '小类关系', '大类关系', '人物2'], sep=',')

    # 从txt文件中提取唯一的行
    txt_row = df_txt.iloc[0]

    tokenizer = BertTokenizer.from_pretrained('../.bert-base-chinese')
    model = BertModel.from_pretrained('../.bert-base-chinese')

    results = []
    for index, csv_row in df_csv.iterrows():
        entity1, entity2, non_entity_content = csv_row['Extracted Entity1'], csv_row['Extracted Entity2'], csv_row[
            'Extracted Non-Entity Content']
        person1, subclass_relation = txt_row['人物1'], txt_row['小类关系']

        distance1 = normalize_edit_distance(entity1, person1)
        distance2 = normalize_edit_distance(entity2, person1)  # 注意这里是否应该是person2
        bert_similarity = calculate_bert_similarity(non_entity_content, subclass_relation, model, tokenizer)

        results.append(
            [entity1, entity2, non_entity_content, csv_row['Original Text'], distance1, distance2, bert_similarity,
             subclass_relation])

    df_results = pd.DataFrame(results,
                              columns=["Extracted Entity1", "Extracted Entity2", "Extracted Non-Entity Content",
                                       "Original Text", "Entity1&Person1 Distance Score",
                                       "Entity2&Person2 Distance Score",
                                       "Non-Entity Content&Subclass Relation Similarity Score", "Relation"])
    df_results.to_csv(output_file, index=False)


process_files("deal.csv", "d.txt", "output.csv")


