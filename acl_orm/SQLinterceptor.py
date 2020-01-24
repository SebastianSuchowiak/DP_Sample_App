#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 02:31:28 2020

@author: barey
"""
from sqlalchemy import event
from sqlalchemy.engine import Engine


class SQLinterceptor():
  
  def start(db):
    class Roles(db.Model):
      __tablename__ = 'roles'
      parrent_role = db.Column(db.String)
      child_role = db.Column(db.String, primary_key=False, unique=True, nullable=False)
      tag = db.Column(db.String, unique = True, nullable = False,primary_key=True)
  
  #def table_from_tree(tree):
    
  def tree_from_table():
    
  
  @event.listens_for(Engine, "before_execute", retval=True)
  def before_execute(conn, clauseelement, multiparams, params):
      print(f"{clauseelement} {multiparams}   {params}")
      return clauseelement, multiparams, params