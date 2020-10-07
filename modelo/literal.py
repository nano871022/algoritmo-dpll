import re

class Literal:

  VAR_NOMBRE = re.compile(r"^[^\d\W]\w*\Z",re.UNICODE)
  """
  la sentencia Propositiva tiene una variable o una variable negada
  """

  def __init__ (self,variable,positivo=True):
    if re.match(Literal.VAR_NOMBRE, variable) :
      self.variable = variable
    else:
      raise SyntaxError("Nombre de variable invalida: '"+variable+"'")
    self.positivo = positivo

  @staticmethod
  def parse(literal):
    literal = literal.replace(" ","") 
    positivo = not literal.startswith("~")
    return Literal( literal if positivo else literal[1:],positivo)
  
  def __repr__ (self):
    return self.__str__ ()
  
  def __str__ (self):
    return ("" if self.positivo else "~") + self.variable
  
  def __hash__ (self):
    return hash(self.__str__ ())
  
  def __eq__ (self, literal):
    return self.__str__() == literal.__str__()
  
  def __invert__ (self):
    return Literal(self.variable, not self.positivo)