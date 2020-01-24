#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 02:31:28 2020

@author: barey
"""
from sqlalchemy import event
from sqlalchemy.engine import Engine
from acl_orm.AclTree import AclTree,tree_from_file
import re
from flask import session
from werkzeug.local import LocalProxy
from flask.globals import _lookup_req_object
from functools import partial



curent_user = None

class SQLinterceptor():
  
  def start(self,db,tree_file = None):
    self.db = db
    class ACL(db.Model):
      __tablename__ = 'acl'
      __table_args__ = {'extend_existing': True} 
      id = db.Column(db.Integer, primary_key=True)
      id_row = db.Column(db.Integer)
      role = db.Column(db.String, nullable=False)      
      tablename = db.Column(db.String, nullable = False)
    class Roles(db.Model):
      __tablename__ = 'roles'
      __table_args__ = {'extend_existing': True} 
      parent_role = db.Column(db.String)
      child_role = db.Column(db.String, primary_key=False, unique=True, nullable=False)      
      tag = db.Column(db.String, unique = True, nullable = False,primary_key=True)
    
    #ACL.insert().values=(1,1,"0.0","employee")
    #db.session.add(ACL(id_row=2,role="0.0",tablename="employee"))
    if(tree_file):      
      self.tree = tree_from_file(tree_file)
      self.tree.generate_tag()
    else:
      roles = Roles.query.all()
      print(roles)
    session = LocalProxy(partial(_lookup_req_object, "session"))
    db.session.add(Roles(child_role = "gsdg",parent_role="eg",tag="53te"))
    
    num_rows_deleted = db.session.query(Roles).delete()
    db.session.commit()
    
    self.select_user("Role2")
    self.acl = ACL
  def tree_from_db(self):
    roles = self.Roles.query.all()

  def insert_tree_todb(self,tree):
    for node in tree.nodes:
      self.db.session.add(Roles(child_role = node.name,parent_role=tree.name,tag=node.tag))
      insert_tree_todb(node)

  def select_user(self,role_name):
    global curent_user
    curent_user = self.tree.find_role(role_name)
      
            
  @event.listens_for(Engine, "before_cursor_execute", retval=True)
  def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    print(f"{statement} {parameters}   {context}")
    tables_from = re.search("FROM.*",str(statement))
    if tables_from and statement[:6] == "SELECT":
      tables_from = str(tables_from[0][5:])
      if tables_from != "roles":
        user_role = curent_user.tag
        statement = statement + " where " + tables_from + """.id in ( SELECT acl.id_row from acl where acl.role ilike '""" + user_role + """%%' and acl.tablename  = '""" + tables_from +"""' )"""
        print(statement)
    return statement, parameters