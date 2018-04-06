#!/usr/bin/env python
# encoding: utf-8
"""
HelperMethods.py

Created by Miguel Molero on 2013-08-28.
Copyright (c) 2013 MMolero. All rights reserved.
"""

import os
from PySide.QtCore import *
from PySide.QtGui import *

import collections
import re, copy
import numpy as np


def sort_nicely(l):
    """
    Sort the given list in the way that humans expect.
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    l.sort(key=alphanum_key)


def createAction(parent, text, slot=None, shortcut=None, icon=None,
                 tip=None, checkable=False, signal="triggered()"):
    action = QAction(text, parent)
    if icon is not None:
        action.setIcon(QIcon(":/%s" % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        parent.connect(action, SIGNAL(signal), slot)
    if checkable:
        action.setCheckable(True)
    return action


def addActions(target, actions):
    if not isinstance(actions, collections.Iterable):
        target.addAction(actions)
    else:
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


def addWidgets(target, widgets):
    if not isinstance(widgets, collections.Iterable):
        target.addWidget(widgets)
    else:
        for widget in widgets:
            target.addWidget(widget)


def setEnabled(actions, state):
    if not isinstance(actions, collections.Iterable):
        actions.setEnabled(state)
    else:
        for action in actions:
            if action is not None:
                action.setEnabled(state)


def setVisible(target, state):
    if not isinstance(target, collections.Iterable):
        target.setVisible(state)
    else:
        for item in target:
            if item is not None:
                item.setVisible(state)


def setText(target, string):
    if not isinstance(target, collections.Iterable):
        target.setText(string)
    else:
        for item in target:
            if item is not None:
                item.setText(string)


def clear(target):
    if not isinstance(target, collections.Iterable):
        target.clear()
    else:
        for item in target:
            item.clear()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def mat2Obj(fromMat, toObj):
    for name in fromMat._fieldnames:
        value = getattr(fromMat, name)
        if hasattr(toObj, name):
            # print toObj, name
            if isinstance(value, float) or isinstance(value, str) or isinstance(value, int):
                setattr(toObj, name, value)
            elif isinstance(value, np.ndarray):
                if value.size == 1:
                    setattr(toObj, name, value.item())
                else:
                    setattr(toObj, name, value)

    return toObj


def objWithListstoArrays(obj):
    for name in obj._fieldnames:
        value = getattr(obj, name)
        if isinstance(value, list):
            setattr(obj, name, np.array(value))

    return obj


def objWithArraysToLists(obj):
    for name in obj._fieldnames:
        value = getattr(obj, name)
        if isinstance(value, np.ndarray):
            setattr(obj, name, value.tolist())

    return obj


def loadDataFromList(data2load, key, Class):
    if key in data2load:
        target = list()
        if isinstance(data2load[key], np.ndarray):
            for item in (data2load[key]).tolist():
                _item = copy.deepcopy(mat2Obj(item, Class))
                target.append(_item)
        else:
            _class = copy.deepcopy(mat2Obj(data2load[key], Class))
            target.append(_class)

        return target
    else:
        None


def loadDataFromListWithLabels(data2load, key, listLabels, listClasses):
    if key in data2load:
        target = list()

        if isinstance(data2load[key], np.ndarray):
            for item in (data2load[key]).tolist():
                for i in range(len(listLabels)):
                    if item.Name == listLabels[i]:
                        _class = copy.deepcopy(mat2Obj(item, listClasses[i]))
                        target.append(_class)
        else:
            item = data2load[key]
            for i in range(len(listLabels)):
                if item.Name == listLabels[i]:
                    _class = copy.deepcopy(mat2Obj(item, listClasses[i]))
                    target.append(_class)
        return target

    else:
        None


def loadDataWithLabels(data2load, key, listLabels, listClasses):
    if key in data2load:
        item = data2load[key]
        for i in range(len(listLabels)):
            if item.Name == listLabels[i]:
                target = copy.deepcopy(mat2Obj(item, listClasses[i]))
        return target
    else:
        None
