import re
import pandas as pd
import matplotlib.pyplot as plt
import spacy
import networkx as nx

# 1. Загрузите данные train.txt, test.txt, val.txt
with open('./data/drake_lyrics.txt', 'r', encoding='utf-8') as f:
    train = f.readlines()

# Переведите данные в формат pandas DataFrame
data = pd.DataFrame(train, columns=['text'])

def remove_bracketed_lines(data):
    return [line for line in data if not re.match(r'\[\w+\]', line)]

# 2. Select random 1000 values
data = data.sample(n=1000, random_state=42)

# Filter text by len > 30
print(len(data))

all_sentences = data['text'].values

all_sentences = remove_bracketed_lines(all_sentences)

nlp = spacy.load('en_core_web_sm')

parsed_sentences = []

for sentence in all_sentences:
    doc = nlp(sentence)
    parsed_sentences.append(doc)

for i in range(2):
    print(f"Пример синтаксического разбора для предложения {i + 1}:")
    for token in parsed_sentences[i]:
        print(f"{token.text:<12} {token.pos_:<10} {token.dep_:<10} {token.head.text}")
    print()

ner_results = []

for sentence in parsed_sentences[:10]: 
    doc = nlp(sentence)
    ner_results.append(doc.ents)

for i, entities in enumerate(ner_results):
    if len(entities) == 0:
        continue
    print(f"Именованные сущности в предложении {i + 1}:")
    for entity in entities:
        print(f"{entity.text:<20} {entity.label_:<15}")
    print()

G = nx.DiGraph()

for i, text in enumerate(parsed_sentences, 1):
    doc = nlp(text)

    for token in doc:
        if token.dep_ == 'ROOT':
            verb = token.lemma_
            subject = None
            obj = None

            for child in token.children:
                if 'subj' in child.dep_:
                    subject = child.lemma_
                elif 'obj' in child.dep_ or 'obl' in child.dep_:
                    obj = child.lemma_

            if subject and obj:
                G.add_node(subject)
                G.add_node(obj)
                G.add_edge(subject, obj, label=verb)

while True:
    
    print(G.nodes)
    # Prompt for user input
    search_term = input("Введите название объекта (вершины): ")

    # Break the loop if the user enters an empty string
    if search_term == "":
        break

    # Create a subgraph containing only the relevant nodes and edges
    subgraph = G.subgraph(list(G.neighbors(search_term)) + [search_term])

    # Draw the subgraph
    pos = nx.spring_layout(subgraph)
    labels = nx.get_edge_attributes(subgraph, 'label')
    nx.draw(subgraph, pos, with_labels=True, font_weight='bold', node_size=700, node_color="skyblue", font_size=8)
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=labels)
    plt.show()

    # Search for the entered object in the graph
    if search_term in G.nodes:
        neighbors = list(G.neighbors(search_term))
        print(f"Объект {search_term} связан с:")
        for neighbor in neighbors:
            edge_label = G.get_edge_data(search_term, neighbor)['label']
            print(f"{neighbor} по отношению '{edge_label}'")
    else:
        print(f"Объект {search_term} не найден в графе.")