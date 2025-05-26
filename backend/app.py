
from flask_cors import CORS
from flask import Flask, request, jsonify
import osmnx as ox
import networkx as nx

app = Flask(__name__)
CORS(app)
# Load graph of a small area (Varanasi, for now)
G = ox.graph_from_place("Varanasi, India", network_type="drive")
G = ox.distance.add_edge_lengths(G)  # ensure 'length' attribute

# Find nearest node to a (lat, lon)


def get_nearest_node(lat, lon):
    return ox.nearest_nodes(G, X=lon, Y=lat)


@app.route('/shortest-path', methods=['POST'])
def shortest_path():
    data = request.json
    src = data['source']  # {lat, lng}
    dest = data['destination']

    try:
        source_node = get_nearest_node(src['lat'], src['lng'])
        dest_node = get_nearest_node(dest['lat'], dest['lng'])

        path = nx.shortest_path(G, source=source_node,
                                target=dest_node, weight='length')
        coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path]

        return jsonify({"path": coords})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
