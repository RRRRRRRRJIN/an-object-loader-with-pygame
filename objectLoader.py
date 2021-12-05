from polyhedron import polyhedron
from vertex import vertex
from face import face


def main():
    # create object and draw lines
    with open('object.txt', 'r') as f:
        lines = f.readlines()
        summary = lines[0].split(',', 1)
        poly = polyhedron(int(summary[0]), int(summary[1]))

        # create vertex list for this poly
        for i in range(1, int(summary[0])+1):
            vertexline = lines[i].strip().split(',', 4)
            newVertex = vertex(int(vertexline[0]), float(
                vertexline[1]), float(vertexline[2]), float(vertexline[3]))
            poly.setVertex(newVertex)

        # create face list for this poly
        for i in range(int(summary[0])+1, int(summary[0])+1+int(summary[1])):
            faceline = lines[i].strip().split(',', 3)
            newFace = face(int(faceline[0]), int(
                faceline[1]), int(faceline[2]))
            poly.setFace(newFace)

    poly.draw()


if __name__ == "__main__":
    main()
