# class for vertex
class vertex(object):
    def __init__(self, id, x, y, z):
        self.__id = id
        self.__x = x
        self.__y = y
        self.__z = z

    # get methods for getting information for each vertex
    def get_id(self):
        return self.__id

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_z(self):
        return self.__z
