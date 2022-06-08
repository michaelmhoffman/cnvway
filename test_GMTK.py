from __future__ import division, print_function
from collections import OrderedDict
import numpy as np
from numpy import array, ndarray


def array2text(a):
    """
    Convert multi-dimensional array to text.
    :param a: array
    :return:
    """
    ndim = a.ndim
    if ndim == 1:
        return " ".join(map(str, a))
    else:
        delimiter = "\n" * (ndim - 1)
        return delimiter.join(array2text(row) for row in a)
    
def add_extra_line(l):
    """
    :param: l: list[str] or str
    Return copy of l with "\n" concatenated with the last item. 
    (l must have at least one item.) 
    For example:
    l = ["a", "b", "c"]
    new_l = add_extra_line(l)
    new_l 
    ["a", "b", "c\n"]
    """
    if isinstance(l, str):
        return "{}\n".format(l)

    last_element = "{}\n".format(l[-1])
    new_l = l[:]
    new_l[-1] = last_element
    return new_l
    

class Object(str):
    def __new__(cls, _name, content, _kind):
        return str.__new__(cls, content)

    def __init__(self, name, content, kind):
        self.kind = kind
        self.name = name


class Array(ndarray):
    def __new__(cls, *args):
        """
        :param input_array: ndarray
        :return:
        """
        input_array = array(args)
        obj = np.asarray(input_array).view(cls)
        return obj


class Section(OrderedDict):
    """
    Contains GMTK objects of a single type and supports writing them to file.
    Key: name of GMTK object
    Value: GMTK object
    """
    def __init__(self):
        """
        Initialize an empty Section object.
        """
        super(Section, self).__init__()

    def __getattr__(self, name):
        if not name.startswith('_'):
            return self[name]
        OrderedDict.__getattr__(self, name)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            if not self.kind() == value.kind:
                raise ValueError("Object has incorrect type.")
            self[name] = value
        else:
            OrderedDict.__setattr__(self, name, value)

    def kind(self):
        """
        Return string attribute kind of all GMTK objects in this Section object.
        :return: str: type of all GMTK objects in this Section object
        """
        section_kind = None
        for obj in self.values():
            if not section_kind:
                section_kind = obj.kind
            else:
                assert section_kind == obj.kind, "Objects must be of same type."
        return section_kind
    

class InlineSection(Section):

    def __str__(self):
        """
        Returns inline string representation of this Section object by calling
        the individual GMTK object's __str__().
        :return:
        """
        # if no gmtk objects
        if len(self) == 0:
            return ""
        # MC, MX are also one line types but have their own subclasses of InlineSection 
        one_line_types = ["MEAN", "COVAR", "DPMF"]  # TODO: DPMF dim > 1?

        lines = ["{}_IN_FILE inline".format(self.kind())]
        lines.append(str(len(self)) + "\n")  # total number of gmtk objects
        for i in range(len(self)):
            obj_header = []
            obj_header.append(str(i))  # index of gmtk object
            obj_header.append(list(self)[i])  # name of gmtk object
            
            if self.kind() in one_line_types:
                # string representation of gmtk object
                obj_header.append(list(self.values())[i].__str__())
                lines.append(" ".join(obj_header))
 
        return "\n".join(add_extra_line(lines))


class Mean(Array):
    """
    A single Mean object.
    """
    kind = "MEAN"

    def __array_finalize__(self, obj):
        if obj is None: return

    def __str__(self):
        """
        Returns the string format of the Mean object to be printed into the
        input.master file (new lines to be added).
        :return:
        """
        for mean in self:
            line = []
            line.append(str(self.get_dimension()))  # dimension
            line.append(array2text(mean))
            return " ".join(line)

    def get_dimension(self):
        """
        Return dimension of this Mean object.
        :return: int: dimension of this Mean object
        """
        return len(self)    


class InputMaster:

    def __init__(self):
        """
        Initialize InputMaster instance with empty attributes (InlineSection
        and its subclasses).
        """
        self.mean = InlineSection()

    def __str__(self):
        """
        Return string representation of all the attributes (GMTK types) by
        calling the attributes' (InlineSection and its subclasses) __str__().
        :return:
        """
        attrs = [self.mean]

        s = []
        for obj in attrs:
            s.append("".join(obj.__str__()))

        return "\n".join(s) # TODO: ask if you want to add a newline charecter here

    def save(self, filename, traindir='segway_output/traindir'):
        """
        Opens filename for writing and writes out the contents of its attributes.
        :param: filename: str: path to input master file 
        :param: traindir: str: path to traindir 
        (default assumes path to traindir is 'segway_output/traindir')
        :return: None 
        """
        with open(filename, 'w') as filename:
            print('# include "' + traindir + '/auxiliary/segway.inc"', file=filename)
            print(self, file=filename)

