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
    # init ACL and Roles db models
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
      tag = db.Column(db.String, unique = True, nullable = False, primary_key=True)

    db.create_all()
    self.acl = ACL
    self.roles = Roles

    #if we pass the file tree in db gets overwritten
    if(tree_file):    
      self.tree = tree_from_file(tree_file)
      self.tree.generate_tag()
      db.session.query(Roles).delete()
      self.insert_tree_todb(self.tree)
      #a = (self.roles.query.values(self.roles.parent_role,self.roles.child_role,self.roles.tag))
      self.tree_from_db()
      #self.db.session.commit()

    ## Create Tree from Database
    self.tree_from_db()
       
    
    db.session.commit()
    
    self.select_user("Role2")
    #self.insert_to_acl()
    
  def insert_to_acl(self):
    self.db.session.add(self.acl(id_row=2,role=".0.1",tablename="employee"))
    self.db.session.commit()
    print("ACLCLLCALCLA")
    #print(self.acl.query.values(self.roles.parent_role,self.roles.child_role,self.roles.tag))
    
  def tree_from_db(self):
    a = self.roles.query.all()
    self.db.session.commit()
    print(a)

  def insert_tree_todb(self,tree):
    for node in tree.nodes:
      print(node.name + "  " + tree.name + "   " + node.tag)
      self.db.session.add(self.roles(child_role = node.name,parent_role=tree.name,tag=node.tag))
      #self.insert_tree_todb(node)

  def select_user(self,role_name):
    global curent_user
    curent_user = self.tree.find_role(role_name)
      
            
  @event.listens_for(Engine, "before_cursor_execute", retval=True)
  def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    excluded_tables = ["roles","flasklogin-users"]

    print(f"{statement} {parameters}   {context}")
    tables_from = re.search("FROM.*",str(statement))
    
    if tables_from and statement[:6] == "SELECT" and curent_user:
      tables_from = str(tables_from[0][5:])
      cut_table_name = tables_from[1:-2]
      if cut_table_name not in excluded_tables:
        user_role = curent_user.tag
        print(user_role)
        statement = statement + " where " + tables_from + """.id in ( SELECT acl.id_row from acl where acl.role ilike '""" + user_role + """%%' and acl.tablename  = '""" + tables_from +"""' )"""
        print(statement)
    return statement, parameters