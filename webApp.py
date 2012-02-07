from bottle import route, run, get, post, request, redirect, static_file

import pydot
from xml.dom.minidom import parseString
import sys
from sets import Set


class Variable:
    def __init__(self):
        self.m_data = ""

    def getData(self):
	return self.m_data
    
    def isSame(self, other):
        
        if(self.m_data == other.m_data):
            return True
        return False

class Relation:
    def __init__(self):
        self.m_data = ""
    
    def getData(self):
	return self.m_data

    def isSame(self, other):
        if(self.m_data == other.m_data):
            return True
        return False

class Individual:
    def __init__(self):
        self.m_data = ""
    
    def getData(self):
	return self.m_data

    def isSame(self, other):
        if(self.m_data == other.m_data):
            return True

        return False

class Atom:
    def __init__(self, data):
        self.m_inds = Set()
        self.m_vars = Set()
        self.m_rel = Relation()
        self.m_data = data
        
    def getVars(self):
	return self.m_vars

    def getInds(self):
	return self.m_inds

    def getInds(self):
	return self.m_inds

    def getRel(self):
	return self.m_rel

    def setRuleId(self, id):
        self.m_ruleId = id

    def getRule(self):
	return self.m_rule

    def setRule(self, rule):
        self.m_rule = rule
        
    def ruleId(self):
        return self.m_ruleId

    def hasSameInds(self, other):
    
        inds = other.m_inds
        diff = inds
        diff = diff.difference(self.m_inds)
        if(len(inds) == len(self.m_inds) and
        len(diff) == 0):
            return True
        
        return False
    
    def hasSameVars(self, other) :

        vars = other.m_vars
        diff = vars
        diff = diff.difference(self.m_vars)
        if(len(vars) == len(self.m_vars) and
        len(diff) == 0):
            return True

        return False

    def hasSameNumVars(self, other):
        vars = other.m_vars
	if(len(vars) == len(self.m_vars)):
	    return True

	return False
    
    def isSame(self, other):
        if(self.hasSameInds(other) and
        self.hasSameVars(other) and
        other.m_rel.isSame(self.m_rel)):
            return True
	elif(self.hasSameInds(other) and 
	other.m_rel.isSame(self.m_rel) and
	self.hasSameNumVars(other)):
	    return True
        
        return False
    
    def parse(self):
        self.m_dom = parseString(self.m_data)
        rels = self.m_dom.getElementsByTagName('Rel')
        if(len(rels) == 1) :
            self.m_rel.m_data = rels[0].toxml()
        
        if(len(rels) == 0) :
            atom = self.m_dom.getElementsByTagName('Atom')[0]
            self.m_rel.m_data = atom.getAttribute('Rel')
        
        inds = self.m_dom.getElementsByTagName('Ind')
        
        for i in inds:
            ind = Individual()
            ind.m_data = i.toxml()
            self.m_inds.add(ind.m_data)
        
        vars = self.m_dom.getElementsByTagName('Var')
        
        for v in vars:
            var = Variable()
            var.m_data = v.toxml()
            self.m_vars.add(var.m_data)

class Head:
    def __init__(self, data):
        self.m_atoms = Set()
        self.m_data = data
    
    def setRuleId(self, id):
        self.m_ruleId = id
        
    def setRule(self, rule):
        self.m_rule = rule

    def ruleId(self):
        return self.m_ruleId
    
    def numAtoms(self):
	return len(self.m_atoms)

    def parse(self):
        self.m_dom = parseString(self.m_data)
        atoms = self.m_dom.getElementsByTagName('Atom')
        
        for at in atoms:
            atom = Atom(at.toxml())
	    atom.setRule(self.m_rule);
            atom.setRuleId(self.m_ruleId)
            atom.parse()
            self.m_atoms.add(atom)

class Body:
    def __init__(self, data):
        self.m_atoms = Set()
        self.m_data = data

    def setRuleId(self, id):
        self.m_ruleId = id

    def setRule(self, rule):
	self.m_rule = rule
        
    def ruleId(self):
        return self.m_ruleId
    
    def parse(self):
        self.m_dom = parseString(self.m_data)
        atoms = self.m_dom.getElementsByTagName('Atom')
        
        for at in atoms:
            atom = Atom(at.toxml())
	    atom.setRule(self.m_rule);
            atom.setRuleId(self.m_ruleId)
            atom.parse()
            self.m_atoms.add(atom)
    
class Rule:
    def __init__(self, data):
        self.m_data = data

    def setId(self, id):
        self.m_id = id
        
    def numHeadAtoms(self):
	return self.m_head.numAtoms() 

    def id(self):
        return self.m_id
    
    def parse(self):
        
        self.m_dom = parseString(self.m_data)
        head = self.m_dom.getElementsByTagName('if')[0].toxml()
        self.m_head = Head(head);
	self.m_head.setRule(self)
        self.m_head.setRuleId(self.m_id)
        self.m_head.parse()
        body = self.m_dom.getElementsByTagName('then')[0].toxml()
        self.m_body = Body(body)
	self.m_body.setRule(self)
        self.m_body.setRuleId(self.m_id)
        self.m_body.parse()


class Graph_Edge:
    def __init__(self, headRuleId, bodyRuleId):
        self.m_headRuleId = headRuleId
        self.m_bodyRuleId = bodyRuleId

class Rule_Library:
    def __init__(self, data):
        self.m_rules = Set()
        self.m_data = data
        self.m_headAtoms = Set()
        self.m_bodyAtoms = Set()
        self.m_edges = Set()
       
    
    def collectHeadAtoms(self):
        for rule in self.m_rules:
            atoms = rule.m_head.m_atoms
            for a in atoms:
                self.m_headAtoms.add(a)
    
    def collectBodyAtoms(self):
        for rule in self.m_rules:
            atoms = rule.m_body.m_atoms
            for a in atoms:
                self.m_bodyAtoms.add(a)
    
    
    def make_graph(self):
        graph = pydot.Dot(graph_type='digraph')
        #print "head atoms len = %d" % len(self.m_headAtoms)
        #print "body atoms len = %d" % len(self.m_bodyAtoms)
        for ath in self.m_headAtoms:
            for atb in self.m_bodyAtoms:
                if(ath.isSame(atb) == True and ath.ruleId() != atb.ruleId()):
		
                    edge = Graph_Edge(ath.ruleId(), atb.ruleId())
                    self.m_edges.add(edge)
                    node_a = pydot.Node("%d" % atb.ruleId(), style="filled", fillcolor="red")
                    node_b = pydot.Node("%d" % ath.ruleId(), style="filled", fillcolor="red")
                    graph.add_node(node_a)
                    graph.add_node(node_b)
		    dot = pydot.Dot(graph)
		    rule = ath.getRule();
		    lab = ""
		    lab = self.make_label(ath)
		    if(rule.numHeadAtoms() > 1):
			ed = pydot.Edge(node_a , node_b, arrowhead='halfopen', label = lab)
		    else:
			ed = pydot.Edge(node_a , node_b, arrowhead='open', label = lab)
		    graph.add_edge(ed)
		    
                    #print "I found an edge!!!"
                        
        graph.write_png('graph.png')
   

    def make_label(self, atom):
	rel = atom.getRel()
	vrs = atom.getVars()
	inds = atom.getInds()
	l = len(rel.getData())
	label = rel.getData()[5:(l-6)] + "(";
	for var in vrs:
		l = len(var)
		label = label + var[5:(l-6)] + ","
	
	for ind in inds:
		l = len(ind)
		label = label + ind[5:(l-6)] + ","

	l = len(label)
	label = label[0:(l-1)] + ")"
	return label
		 
    
    def parse(self):
        self.m_dom = parseString(self.m_data)
        rules = self.m_dom.getElementsByTagName('Implies')
        id = 0;
        for r in rules:
            rule = Rule(r.toxml())
            rule.setId(id)
            rule.parse()
            self.m_rules.add(rule)
            id = id + 1
        
        self.collectHeadAtoms()
        self.collectBodyAtoms()
        self.make_graph()


class Parser:
    def set_data(self,data):
        self.m_data = data

    def read_file(self,filename):
        self.m_file = open(filename,'r')
        self.m_data = self.m_file.read()
        self.m_file.close()
        
    def parse(self):
        
        self.m_dom = parseString(self.m_data)
        self.m_library = Rule_Library(self.m_dom.getElementsByTagName('RuleML')[0].toxml())
        
        self.m_library.parse()

@route('/images/<filename:re:.*\.png>#')
def send_image(filename):
    return static_file(filename, root='/home/dio/images/', mimetype='image/png')
    

@route('/ruleml')
def upload_form():
	string = '<!DOCTYPE html>'
	string += '<html>'
	string += '	<head>'
	string += '		<meta charset="utf-8">'
	string += '		<title>Rule-ML Dependencies Visualizer</title>'
	string += '		</head>'

	string += '<body>'

	string += '	<h1>Rule-ML Dependencies Visualizer</h1>'
	string += '	<h2>Developer </h2>'
	string += '	<ul>'
	string += '		<li> Chatzivagias Christos</li>'
	string += '	</ul>'

	string += '	<form action="/ruleml" method="post" enctype="multipart/form-data">'
	string += 'Choose a file to upload:'
	string += '		<input type="file" name="data"/>'
	string += '		<input type="submit" name="submit" value="Submit"/>'
	string += '	</form>'

	string += '	<form action="/ruleml2" method="post" enctype="multipart/form-data">'
	string += 'Write ruleML rules here:'
	string += '		<input type="submit" name="submit" value="Submit"/>'
	string += '		<textarea name="thetext" rows="20" cols="80">Place your RULE-ML code here</textarea>'
	string += '	</form>'
	string += '</body>'
	string += '</html>'
	return string 

@route('/ruleml', method='POST')
def do_upload_file():
	submit = request.forms.submit
	data = request.files.data

	p = Parser()
	raw = data.file.read()
	p.set_data(raw)
	p.parse()
	#if data and data.file:
	#	raw = data.file.read() # This is dangerous for big files
	#	filename = data.filename
	return static_file('graph.png', root='.')

@route('/ruleml2', method='POST')
def do_upload_text():
	submit = request.forms.submit
	data = request.forms.thetext

	p = Parser()
	#raw = data.file.read()
	p.set_data(data)
	p.parse()
	#if data and data.file:
	#	raw = data.file.read() # This is dangerous for big files
	#	filename = data.filename
	return static_file('graph.png', root='.')



run(host='localhost', port=8888)
