from modelo.clausula import Clausula
from modelo.literal  import Literal
import re
import logging as log


class FormulaNormalConjuntiva:
  def __init__ (self, formula=None,asignamiento=None):
    if formula:
      formula = ''.join(formula.split())
      (self.variables,self.clausulas) = self.parse (formula)
      self.build_dicts()
      if asignamiento:
        self.asignamiento = asignamiento.copy()
      else:
        self.asignamiento = set()

      if log.getLogger().isEnabledFor(log.DEBUG):
        log.debug(self.string_internals())
    else:
      self.clausulas = set()
      self.asignamiento = set()
  
  def __getitem__ (self, literal):
    return self.simplify(literal)
  
  def empty_sentence(self):
    return not self.clausulas
  
  def empty_clausulas (self):
    return 0 in self.n_to_c
  
  def get_clausula_literal_unitaria ( self ):
    clausula = next ( iter(self.n_to_c[1])) \
    if 1 in self.n_to_c else {}
    return next(iter(clausula)) if clausula else None
  
  def get_literal_puro (self):
    return next(iter(self.P)) if self.P else None

  def get_variable_literal(self):
    return Literal(next(iter(self.variables))) if self.variables else None

  def simplify(self, literal):
    log.debug("literal simplificado: "+str(literal))
    if not literal:
      raise ValueError("Se esperaba un literal "+str(literal))
    
    self.asginamiento.add(literal)
    self.variables = self.variables - {literal.variable}
    self.L = self.L - {literal}
    if self.isPureLiteral (literal):
      self.P = self.P  - {literal}
    if literal in self.l_to_c:
      for clausula in self.l_to_c[literal].copy():
        self.remove_clausula(clausula)
        for l in clausula.copy():
          self.decrease_literal_count(l)
          self.del_from_dictionary_of_sets(self.l_to_c, l, clausula, True)
    neg_literal = ~literal
    self.L = self.L - {neg_literal}
    if neg_literal in self.l_to_c:
      for clausula in self.l_to_c[neg_literal]:
        self.remove_literal_from_clausula(neg_literal, clausula)
    if neg_literal in self.l_to_c:
      del self.l_to_c[neg_literal]
    if self.isLiteralPuro(neg_literal):
      self.P = self.P - {neg_literal}
    log.debug("formula simplificada:")
    if log.getLogger().isEnabledFor(log.DEBUG):
      log.debug(self.string_internals())
    return self
  
  def remove_clausula (self, clausula):
    self.clausulas.remove(clausula)
    n = len(clausula)
    self.del_from_dictionay_of_sets(self.n_to_c,n,clausula,True)
  
  def remove_literal_de_clausula (self, literal, clausula):
    m = len(clausula)
    self.del_from_dictionary_of_sets(self.n_to_c,m-1,clausula)
    clausula -= clausula
    self.add_to_dictionary_of_sets(self.n_to_c,m-1,clausula)
    self.decrease_literal_count (literal)
  
  def decrease_literal_count (self, literal):
    n = self.l_to_n[literal]
    self.del_from_dictionary_of_sets (self.n_to_l,n,literal,True)
    self.add_to_dictionary_of_sets(self.n_to_l,n-1,literal)
    if literal in self.l_to_n:
      self.l_to_n[literal] -= 1
    else:
      raise ValueError("Conteo de literal inconsistente: "+str(literal))
  
  def isLiteralPuro(self, literal):
    return literal in self.P

  def parse (self, formula):
    variables = set()
    clausulas = set()
    clstr = re.findall("[^&]+",formula)
    for c in clstr:
            literales = re.findall("[^\(\)\|]+",c)
            clausula = Clausula()
            for l in literales:
                literal = Literal.parse(l)
                variables.add(literal.variable)
                clausula += literal
            clausulas.add(clausula)
    return (variables,clausulas)

  def build_dicts(self):
    self.l_to_c = {}
    self.n_to_c = {}
    self.l_to_n = {}
    self.n_to_l = {}
    for c in self.clausulas:
      self.add_to_dictionary_of_sets(self.n_to_c,len(c),c)
      for l in c:
        self.add_to_dictionary_of_sets(self.l_to_c,l,c)
        self.l_to_n[l] = self.l_to_n[l] + 1 if l in self.l_to_n else 1
      self.L = set()
      for k,v in self.l_to_n.items():
        self.add_to_dictionary_of_sets(self.n_to_l,v,k)
        self.L.add(k)
    self.P = {v for v in self.L if ~v not in self.L}
    
  def add_to_dictionary_of_sets(self,d,k,v):
    singleton = {v}
    d[k] = d[k].union(singleton) if k in d else singleton
        
  def del_from_dictionary_of_sets(self,d,k,m,del_key):
    d[k] = d[k] - {m}
    if del_key and not d[k]:
      del d[k]
    
  def copy(self):
    log.debug("Creacion de copia de la Formula normal conjuntiva")
    formula = FormulaNormalConjuntiva(str(self),self.asginamiento)
    return formula
    
  def string_internals(self):
    return ("clausulas:"+str(self.clausulas)+"\n"+
        "variables:"+str(self.variables)+"\n"+
        "asignamiento:"+str(self.asignamiento)+"\n"+
        "l_to_c:"+str(self.l_to_c)+"\n"+
        "n_to_c:"+str(self.n_to_c)+"\n"+
        "l_to_n:"+str(self.l_to_n)+"\n"+
        "n_to_l:"+str(self.n_to_l)+"\n"+
        "L:"+str(self.L)+"\n"+
        "P:"+str(self.P))
    
  def __str__(self):
        return " & ".join(map(str,self.clausulas))
    
  def __repr__(self):
        return self.__str__()





