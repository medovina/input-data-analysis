#!/usr/bin/env python
# -*- coding: utf-8

import abc
import argparse
import evemu
import sys

from . import *

class GnuPlot(object):
    def __init__(self, path, **kwargs):
        self.path_cmd = "{}.gnuplot".format(path)
        self.path_data = "{}.dat".format(path)
        self.kwargs = kwargs
        self.plots = []

    def __enter__(self):
        f = open(self.path_cmd, "w", **self.kwargs)
        f.write("# /usr/bin/gnuplot\n")
        f.write("# Do not edit, generated by {}\n".format(sys.argv[0]))
        f.write("file = '{}'\n".format(self.path_data))
        f.write("set autoscale\n")
        self.file_obj_cmd = f

        f = open(self.path_data, "w", **self.kwargs)
        f.write("# for processing see {}\n".format(self.path_cmd))
        self.file_obj_data = f
        return self.file_obj_cmd

    def __exit__(self, *args):
        self.file_obj_cmd.write("plot file {}\n".format(", \n".join(self.plots)))
        self.file_obj_cmd.write("pause -1\n")
        self.file_obj_cmd.close()
        self.file_obj_data.close()

    def labels(self, xlabel, ylabel):
        if xlabel is not None:
            self.file_obj_cmd.write("set xlabel '{}'\n".format(xlabel))
        if ylabel is not None:
            self.file_obj_cmd.write("set ylabel '{}'\n".format(ylabel))

    def ranges(self, xrange, yrange):
        if xrange is not None:
            self.file_obj_cmd.write("set xrange [{}]\n".format(xrange))
        if yrange is not None:
            self.file_obj_cmd.write("set yrange [{}]\n".format(yrange))

    def data(self, string):
        self.file_obj_data.write("{}\n".format(string))

    def comment(self, string):
        self.file_obj_data.write("# {}\n".format(string))

    def plot(self, command):
        self.plots.append(command)

