#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 18:08:51 2019

@author: barey
"""

class TreeIterator(object):
  def __init__(self,tree):
    self.current = tree
    #self.queqe = queue.Queue()

class AclTree:
    nodes = []
    name = ""
    tag = ""
    def __init__(self,children,name):
        self.nodes = children
        self.name = name
        
    def add_node(self,node):
        self.nodes.append(node)
    
    def add_role(self,role_name):
      self.nodes.append(AclTree([],role_name))
    
    def get_as_string(self,text):
      pass
      #text = text + 
      
    
    def print_tree(self):
      print(self.name + " " + self.tag)
      for node in self.nodes:
        node.print_tree()
      
    def find_role(self,role_name):
      if self.name == role_name:
        return self
      else:
        for node in self.nodes:
          found = node.find_role(role_name)
          if found != None:
            return found

    def add_child_role(self,role_name,parent_name):
      parent_node = self.find_role(parent_name)
      if parent_node != None:
        parent_node.add_role(role_name)
        
    def generate_tag(self):
        self.set_tag("","0")        
    def set_tag(self, parent_tag, following):
        self.tag = parent_tag + "." + following
        for i in range(len(self.nodes)):
            self.nodes[i].set_tag(self.tag,str(i))


def tree_from_string(table):
  tree_root = AclTree([],"")
  for line in table.splitlines():
    roles = line.split(" ")
    if len(roles) < 2:
      tree_root.add_role(roles[0])
    else:
      tree_root.add_child_role(roles[0],roles[1])
  return tree_root

def tree_from_file(filename):
  with open(filename, 'r') as file:
    data = file.read()
  return tree_from_string(data)
      



