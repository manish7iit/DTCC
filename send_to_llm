from langchain import OpenAI

def main():
    with open('data.txt', 'r') as f:
        data = f.read()
    llm = OpenAI(api_key="", temperature=0)

    prompt = f"""
    # 
You are an intelligent system that will convert a structure JSON format text file into knowledge graph that will be used for graphRAG system.
This JSON file includes all key nodes, their relationships and their description. Here are steps to follow:

1. **Detect communities** - Identify clusters of highly connected nodes(entities) (use themes, summaries and relationships of nodes)
2. **Traverse hierarchically** - Start with relevant communities, then go down to specific nodes and relationships and make communities 
    or group of nodes at different hierarchical levels.
3. **community summary": Generate summaries of each community at each hierarchical level that is used as characteristic property of that
    community. 

## Response Format:
**Answer**: [Direct response to the question]
**Community Analysis**: [Relevant node clusters/themes identified and level of Hierarchy.]
**Key Entities**: [Relevant nodes from graph with their community context]
**Relationships**: [Important connections within and across communities]
**Hierarchical Insights**: [Patterns from community-level to node-level analysis]

## Rules:
- Only use information from the provided JSON graph
- Follow edges to explore multi-hop relationships
- Include entity descriptions and relationship details when relevant
- Include community summaries relevant to nodes/entities at that level of Hierarchy.

#strict note: Please make sure that these nodes are financial entities , so make communities keeping this point in mind.

This is your data in JSON format:-
    {data}
    Please analyze this data and make a GraphRAG system.
    """
    response = llm(prompt)
    print("LLM Response:")
    print(response)

if __name__ == "__main__":
    main()

