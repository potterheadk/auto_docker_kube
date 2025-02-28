from flask import Flask, request, jsonify, Response
from auto_docker_kube.docker_logs import get_container_logs

app = Flask(__name__)

@app.route('/fetch_logs', methods=['POST'])
def fetch_logs():
    """
    Fetch logs from a given container.
    Supports optional parameters for limiting logs.
    """
    data = request.json
    container_id = data.get("container")
    tail = data.get("tail")  # Number of last lines to fetch
    follow = data.get("follow", False)  # Whether to stream logs

    if not container_id:
        return jsonify({"error": "Container ID/Name required"}), 400

    logs = get_container_logs(container_id, tail=tail, follow=follow)

    if isinstance(logs, dict):  # If an error occurs
        return jsonify(logs), 500

    if follow:  # Streaming response for real-time logs
        return Response(logs, mimetype="text/plain")

    return jsonify({"logs": logs})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
