# AutoDCM
Code for methods in the paper: AutoDCM A Novel Framework for Automatic Relation Extraction Dataset Construction via Distant Supervision and Large Language Models for Low-Resource Tasks

## The AutoDCM Framework
![AutoDCM](https://github.com/user-attachments/assets/cb1a04a9-289f-496d-958a-8260852e1747)
>This framework automates the extraction of open triples from unstructured text using ChatGPT, hypothesizing their alignment with corresponding entities and relations within a knowledge base. Heuristic methods, reinforced by BERT-based semantic validation, are then applied to assess the veracity of these triples. The >integration of Tongyici Cilin facilitates the ultimate semantic disambiguation, certifying the accurate reflection of the knowledge base's entity relationships.




## Datasets
1. ***CPRE***
>The CPRE dataset is located in the `data/CPRE` folder.

2. ***DuIE***
>For detailed information about the DuIE dataset, refer to the paper: [Duie: A large-scale Chinese dataset for information extraction]>(https://link.springer.com/chapter/10.1007/978-3-030-32236-6_72).

3. ***IPRE***
>For detailed information about the IPRE dataset, refer to the paper: [Ipre: A dataset for inter-personal relationship extraction]([link to the paper]>(https://link.springer.com/chapter/10.1007/978-3-030-32236-6_9)https://link.springer.com/chapter/10.1007/978-3-030-32236-6_9).
>

## Framework

1. ***Freebase***
>Freebase plays a crucial role in the AutoDCM framework as a comprehensive knowledge base. It provides structured information that assists in aligning extracted triples with existing entities and relationships. >For more information about how Freebase is utilized within AutoDCM, refer to the section 'Constructing the Knowledge Base for Enhanced RE' in our paper.

>The knowledge base used in our paper is located in the `src/freebase/PersonGraphDataSet-master` directory. For more details about this dataset, visit [PersonRelationKnowledgeGraph on GitHub]>(https://github.com/liuhuanyong/PersonRelationKnowledgeGraph).

2. ***Data Crawling***
>Instructions for data crawling and preparation.
* `src/craw_data/data_craw.py`
   * Automatically accesses multiple search engines, such as Baidu and Bing.
   * Searches for pairs of people as provided in the `src/freebase/PersonGraphDataSet-master/person_rel_kg.txt` file.
   * Saves the search results to the `read.txt` file.
* `src/craw_data/txt_to_csv.py`
   * Reads the read.txt file to find sentences containing specific pairs of people.
   * Creates corresponding CSV files based on the matched pairs and their relationships.
   * Each CSV file is named `Person1&Person2.csv` and includes people's names, relationships, and sentences.


3. ***LLM-Driven OpenIE***
>This component leverages the capabilities of large language models, specifically GPT-3.5, for open information extraction (OpenIE). The process involves >extracting open triples (subject, relation, object) from texts to obtain a more granular understanding of the relationships between entities.
* `src/openIE.py`
  * Utilizes GPT-3.5 for extracting open triples from texts.
  * Processes input from CSV files, where each row contains a pair of entities and a related text snippet.
  * The script reads the input file where the first column is Entity1, the second is Entity2, the third is the relationship, and the fourth is the text.
  * For each text entry, it extracts the open triples and stores them in a new CSV file.
  * The output CSV file format includes columns for Extracted Entity1, Extracted Entity2, Extracted Non-Entity Content, and the Original Text.

4. ***Heuristic Entity and Relationship Alignment***
>This stage of the AutoDCM framework involves aligning the extracted entities and relationships with the known entities and relationships from the Freebase >knowledge base. It uses a combination of heuristic methods to enhance the accuracy of alignment.
* `src/ER_Alignment.py`
* Processes the data to align the extracted information with the Freebase dataset.
* These similarity scores are then normalized and integrated into the alignment process to refine the matching accuracy.
* The results are saved in a new CSV file, which includes the original extracted information along with the calculated distance and similarity scores, providing a comprehensive view of the entity and relationship alignment.
   
5. ***Semantic Disambiguation***
>The Semantic Disambiguation stage in the AutoDCM framework is vital for determining the veracity and relevance of the extracted entity-relationship pairs. This >stage involves assessing the context and semantic content of the relationships extracted, enhancing the precision of the dataset construction.
* `src/semantic_disambiguation.py`
* The script then utilizes the TongYiCi CiLin for Chinese semantic analysis or a similar semantic database for other languages, to determine the semantic proximity between the extracted content and the predefined relationships.
* Each row in the dataset is labeled as 'Positive' or 'Negative' based on the semantic similarity assessment. A 'Positive' label indicates a high degree of semantic alignment with the known relationships in the Freebase knowledge base, while a 'Negative' label suggests a lack of such alignment.

## Model
Please refer to the mentioned evaluation model in the paper for assessment.
