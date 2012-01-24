    # -*- coding: <<encoding>> -*-
    #-------------------------------------------------------------------------------
    #   <<project>>
    # 
    #-------------------------------------------------------------------------------

import pydot
import wxversion
from xml.dom.minidom import parseString
wxversion.select("2.8")
import wx, wx.html
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
			ed = pydot.Edge(node_a , node_b, arrowhead='open', label = lab)
		    else:
			ed = pydot.Edge(node_a , node_b, arrowhead='halfopen', label = lab)
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
    
    
aboutText = """<p>Sorry, there is no information about this program. It is
    running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.
    See <a href="http://wiki.wxpython.org">wxPython Wiki</a></p>""" 

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())

class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About <<project>>", style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(700,200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class Frame(wx.Frame):
    
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(50,50), size=(800,600))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        self.m_import = menu.Append(wx.ID_EXIT, "I&mport\tAlt-M", "Choose RuleML xml file.")
        self.m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, self.m_exit)
        self.Bind(wx.EVT_MENU, self.OnOpen, self.m_import)
        menuBar.Append(menu, "&File")
            
        menu = wx.Menu()
        self.m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, self.m_about)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)
        self.statusbar = self.CreateStatusBar()
        panel = wx.Panel(self)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        box = wx.BoxSizer(wx.HORIZONTAL)
        vbox1.Add(box, 0, wx.EXPAND, 0)
        vbox1.Add(vbox2, 0, wx.EXPAND, 0)
        self.m_text = wx.StaticText(panel, -1, "Rule ML File Location")
        box.Add(self.m_text, 0, wx.ALL, 7)
        
        self.m_display = wx.TextCtrl(panel, -1, "/home/dio/sample.ruleml")
        box.Add(self.m_display,wx.EXPAND)
        
        self.m_generate = wx.Button(panel, -1, "Generate Graph")
        self.m_generate.Bind(wx.EVT_BUTTON, self.Generate)
        box.Add(self.m_generate, 0, wx.ALL, 0)
        pngFile = wx.Image("graph.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.m_pictureBox = wx.StaticBitmap(panel, -1, pngFile)
        vbox2.Add(self.m_pictureBox, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.CENTER, 0)
        panel.SetSizer(vbox1)
        panel.Layout()

    def OnOpen(self, event):
        "Open an image file, set title if successful"
            
        dlg = wx.FileDialog(self, message="Open a RuleML File...")
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.m_display.SetValue(filename)
        dlg.Destroy()

    def OnClose(self, event):
        dlg = wx.MessageDialog(self, "Do you really want to close this application?", "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()

    def Generate(self, event):
        p = Parser()
        p.read_file(self.m_display.GetValue())
        p.parse()
        pngFile = wx.Image("graph.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.m_pictureBox.SetBitmap(pngFile)
        #print "OK Parsed"

app = wx.App(redirect=True)   # Error messages go to popup window
top = Frame("Rule ML Rule Dependency Visualization")
top.Show()
app.MainLoop()
