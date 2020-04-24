# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

class Element(object):
    """
        in unity game Element is just GameObject
    Attributes:
        object_name:GameObject的全路径
        instance:GameObject Instance,the instance id of gameobject is always guarnnteed to be unique
    """

    def __init__(self, object_name, instance):
        self.__object_name = object_name
        self.__instance = instance

    @property
    def object_name(self):
        return self.__object_name

    @property
    def instance(self):
        return self.__instance

    def __str__(self):
        return "GameObject {0} Instance = {1}".format(self.object_name, self.instance)

    def __eq__(self, element):
        return hasattr(element, '__instance') and self.__instance == element.instance

    def __ne__(self, element):
        return not self.__eq__(element)

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (object_name="{1}", instance="{2}")>'.format(type(self), self.object_name, self.instance)

