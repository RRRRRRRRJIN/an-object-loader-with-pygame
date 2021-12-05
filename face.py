# class for face
class face(object):
    def __init__(self, p1, p2, p3):
        self.__p1 = p1
        self.__p2 = p2
        self.__p3 = p3

    # get methods for getting information from face
    def get_p1(self):
        return self.__p1

    def get_p2(self):
        return self.__p2

    def get_p3(self):
        return self.__p3
