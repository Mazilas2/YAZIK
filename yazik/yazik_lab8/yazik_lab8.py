import json
import re
import pandas as pd
import matplotlib.pyplot as plt
import spacy
import networkx as nx

#import spacy.cli

#spacy.cli.download("en_core_web_sm")

# 1. Загрузите данные train.txt, test.txt, val.txt
with open('/workspaces/codespaces-blank/yazik/yazik_lab8/data/drake_lyrics.txt', 'r', encoding='utf-8') as f:
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

ner_results = []

for sentence in parsed_sentences[:]: 
    doc = nlp(sentence)
    ner_results.append(doc.ents)

for i, entities in enumerate(ner_results):
    if len(entities) == 0:
        continue
    print(f"Именованные сущности в предложении {i + 1}:")
    for entity in entities:
        #entity_id = f"ENTITY_{i}_{entity.text.replace(' ', '_')}"
        entity_id = f"ENTITY_{i}_{entity.start}_{entity.end}"
        all_sentences[i] = all_sentences[i].replace(entity.text, entity_id)
        print(f"{entity_id:<20} {entity.label_:<10} {entity.text}")
    print()

parsed_sentences = []

for sentence in all_sentences:
    doc = nlp(sentence)
    parsed_sentences.append(doc)

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
    
nodes_data = []
for node in G.nodes:
    nodes_data.append({"id": node, "label": node})

edges_data = []
for edge in G.edges:
    source, target = edge
    label = G.get_edge_data(source, target)["label"]
    edges_data.append({"from": source, "to": target, "label": label})

# Write the node and edge data to a JavaScript file
with open("graph_data.js", "w") as f:
    f.write("var nodes = " + json.dumps(nodes_data) + ";\n")
    f.write("var edges = " + json.dumps(edges_data) + ";\n")