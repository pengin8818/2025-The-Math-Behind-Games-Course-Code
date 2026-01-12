def parse_obj_complete(text_content):
    """
    Parse OBJ file content and extract vertices and edges from faces.

    Args:
        text_content (str): The text content containing vertex and face data

    Returns:
        tuple: (points, connections) where:
            points: List of vertices in format [[[x], [y], [z]], ...]
            connections: List of edges in format [(v1, v2), ...]
    """
    points = []
    connections = []
    connection_set = set()  # Use set to avoid duplicate edges

    lines = text_content.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if not parts:
            continue

        # Parse vertices (v x y z)
        if parts[0] == 'v':
            if len(parts) >= 4:
                try:
                    x = 1000 * float(parts[1])
                    y = 1000 * float(parts[2])
                    z = 1000 * float(parts[3])
                    points.append([[x], [y], [z]])
                except ValueError as e:
                    print(f"Error parsing vertex line: {line}")
                    print(f"Error: {e}")

        # Parse faces (f v1 v2 v3 ...) and create edges
        elif parts[0] == 'f':
            if len(parts) >= 4:  # Need at least 3 vertices for a face
                try:
                    face_vertices = []
                    # Extract vertex indices from face definition
                    for part in parts[1:]:
                        # Handle different formats: f v1, f v1/vt1, f v1/vt1/vn1
                        vertex_index = part.split('/')[0]
                        if vertex_index:
                            # OBJ uses 1-based indexing, convert to 0-based
                            v_idx = int(vertex_index) - 1
                            # Validate vertex index exists
                            if 0 <= v_idx < len(points):
                                face_vertices.append(v_idx)
                            else:
                                print(f"Warning: Vertex index {v_idx} out of range in face: {line}")

                    # Create edges from the face vertices
                    if len(face_vertices) >= 2:
                        for i in range(len(face_vertices)):
                            v1 = face_vertices[i]
                            v2 = face_vertices[(i + 1) % len(face_vertices)]
                            # Store edges in consistent order (smaller index first) to avoid duplicates
                            edge = (min(v1, v2), max(v1, v2))
                            connection_set.add(edge)

                except ValueError as e:
                    print(f"Error parsing face line: {line}")
                    print(f"Error: {e}")

    # Convert set to list for final output
    connections = list(connection_set)
    return points, connections


def parse_obj_from_file(filename):
    """
    Parse OBJ file and extract vertices and edges.

    Args:
        filename (str): Path to the OBJ file

    Returns:
        tuple: (points, connections)
    """
    try:
        with open(filename, 'r') as file:
            text_content = file.read()
        return parse_obj_complete(text_content)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return [], []
    except Exception as e:
        print(f"Error reading file: {e}")
        return [], []