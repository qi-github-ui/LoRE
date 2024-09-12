def read_people_relations(file_path):
    """ 读取人物关系文件并返回字典 """
    relations = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # 跳过标题行
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 4:
                key = (parts[0], parts[3])  # 人物对作为键
                relations[key] = parts[1]  # 小类关系
    return relations

def process_sentences(read_file, relations):
    """ 处理句子并保存到相应的CSV文件 """
    with open(read_file, 'r', encoding='utf-8') as file:
        sentences = file.readlines()

    for (person1, person2), relation in relations.items():
        matched_sentences = [s for s in sentences if person1 in s and person2 in s]
        if matched_sentences:
            csv_filename = f"{person1}&{person2}.csv"
            save_to_csv(csv_filename, person1, person2, relation, matched_sentences)

def save_to_csv(filename, person1, person2, relation, sentences):
    """ 将匹配的句子保存到CSV文件 """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Person1', 'Person2', 'Relation', 'Text'])
        for sentence in sentences:
            csv_writer.writerow([person1, person2, relation, sentence])


# freebase_file_path = 'freebase.txt'
# read_file_path = 'read.txt'

# relations = read_people_relations(freebase_file_path)
# process_sentences(read_file_path, relations)

process_sentences("read_file_path", read_people_relations("freebase_file_path"))