#!/usr/bin/env python
# coding=utf-8

from xml.dom import minidom, Node

#############################################################
#goal: xml config parse
#############################################################
class ConfigParse(object):
    """
    parse xml config with minidom
    """
    def __init__(self, filepath):
        try:
            self.doc = minidom.parse(filepath)
            self.root = self.doc.documentElement
        except Exception, e:
            print 'ConfigParse init failed cause:', e

    def getValue(self, key):
        """
        return value of xml key
        :param key, must be a node without child, like 'node.ceph.host'
        """
        try:
            nodes = [self.root]
            keys = key.split('.')
            j = 0
            lens = len(keys)
            for i in range(lens):
                if i == 0:
                    if keys[0] != self.root.nodeName:
                        return None
                    else:
                        continue
                node = nodes[j].getElementsByTagName(keys[i])[0];
                nodes.append(node)
                j = j+1
            return nodes[j].childNodes[0].nodeValue
        except Exception, e:
            #打印异常时不要加空格了，异步自带空格。
            print 'getValue failed cause:', e

