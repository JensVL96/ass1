# page-rank-mapper.py

def mapper(line):

    origin = line.split()[0]
    destinations = line.split()[1:]

    # Calculate the rank contribution for each link
    rank_contribution = 1.0 / len(destinations)

    # Emit (destination, rank_contribution) for each link
    for page in destinations:
        yield (page.replace(',', ''), rank_contribution)

    # Emit (node, links) to reconstruct the graph structure
    # yield (node, links)

# page-rank-reducer.py

def reducer(intermediate_data):
    grouped_data = {}
    
    # Group by key (node)
    for link, rank_contribution in intermediate_data:
        if link in grouped_data:
            grouped_data[link] += rank_contribution
        else:
            grouped_data[link] = rank_contribution

    return [(link, grouped_data[link]) for link in grouped_data.keys()]

    # reduced_data = []
    # for node in grouped_data:
    #     links = None

        # for value in values:
        #     if isinstance(value, list):
        #         links = value
        #     else:
        #         total_rank += value

        # Example damping factor for PageRank
        # damping_factor = 0.85
        # new_rank = (1 - damping_factor) + damping_factor * total_rank

        # Emit the new rank and the graph structure
        # reduced_data.append((node, (new_rank.keys(), links)))

        # Hot tip: Print out the amount of ranks on each node
        #print(f"Node {node} has a new rank of {new_rank} with {len(values)} contributions")

    # return reduced_data