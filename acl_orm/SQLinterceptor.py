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
  
  def start(self,db,tree_file = None, acl_file = None):
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
    class UserRoles(db.Model):
      __tablename__ = 'user-roles'
      __table_args__ = {'extend_existing': True} 
      username = db.Column(db.String, primary_key=True,unique=True,nullable=False)
      role = db.Column(db.String, nullable=False)      
    db.create_all()
    self.acl = ACL
    self.roles = Roles
    self.user_roles = UserRoles
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
    if acl_file:
      db.session.query(ACL).delete()
      self.acl_from_file(acl_file)

    
    db.session.commit()
    
    #self.select_user("u1")
    self.insert_to_acl()

  def assign_role(self,username,role):
    self.db.session.add(self.user_roles(username = username,role=role))
    self.db.session.commit()

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
      self.insert_tree_todb(node)

  def acl_from_file(self,aclfile):
      with open(aclfile, 'r') as file:
        data = file.read()
      for line in data.splitlines():
        values = line.split(" ")
        self.db.session.add(self.acl(id_row=int(values[0]),role=values[1],tablename=values[2]))
      self.db.session.commit()

  def select_user(self,username):
    global curent_user
    query = self.db.session.query(self.user_roles).filter(username == username).first()
    role_name = query.role
    print(">>>>>>>>" + role_name)
    curent_user = self.tree.find_role(role_name)
    #print(self.acl.query.values(self.roles.parent_role,self.roles.child_role,self.roles.tag))
      
            
  @event.listens_for(Engine, "before_cursor_execute", retval=True)
  def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    excluded_tables = ["roles","flasklogin-users"]

    print(f"{statement} {parameters}   {context}")
    tables_from = re.search("FROM.*",str(statement))
    where_statement = re.search("WHERE",str(statement))
    #if where_statement:
    #  return statement, parameters

    if tables_from and statement[:6] == "SELECT" and curent_user:
      tables_from = str(tables_from[0][5:])
      cut_table_name = tables_from[1:-2]

      if cut_table_name not in excluded_tables and tables_from not in excluded_tables:
        print(">>>>>>>>>>>>>>>>>"+cut_table_name+"<<<<<")
        user_role = curent_user.tag
        print(user_role)
        if where_statement:
          statement = statement + " and " + tables_from[:-1] + """.id in ( SELECT acl.id_row from acl where acl.role ilike '""" + user_role + """%%' and acl.tablename  = '""" + tables_from[:-1] + """' )"""
        else:
          statement = statement + " where " + tables_from + """.id in ( SELECT acl.id_row from acl where acl.role ilike '""" + user_role + """%%' and acl.tablename  = '""" + tables_from +"""' )"""
        print(statement)
    return statement, parameters