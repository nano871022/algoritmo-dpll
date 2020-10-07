from modelo.literal import Literal

class Clausula:
  def __init__(self, literales=None, frozen_hash=True):
    self.frozen_hash = frozen_hash
    if literales:
      self.literales = frozenset(literales) if frozen_hash else literales
    else:
      self.literales = set()
  
  def __hash__ (self):
    return id(self) if self.frozen_hash else hash(self.literales)
  
  def __eq__ (self, clausula):
    if self.__hash__ () == hash(clausula):
      if self.frozen_hash:
        return True
      else:
        return self.literales == clausula.literales
    else:
      return False

  def __iadd__ (self, literal):
    if isinstance (literal, Literal):
      self.literales = self.literales.union({literal})
      return self
    else:
      raise TypeError("Se esperaba un literal")
  
  def __add__ (self, literal):
    if isinstance ( literal, Literal ):
      return Clausula( self.literales.union({literal}),self.frozen_hash)
    else:
      raise TypeError("Se esperaba un literal")
  
  def __isubs__ ( self, literal):
    if isinstance(literal, Literal):
      self.literales = self.literales.difference({literal})
      return self
    else:
      raise TypeError("Se esperaba un literal")
  
  def __subs__ (self, literal):
    if isinstance(literal, Literal):
      return Clausula(self.literales.difference({literal}),self.frozen_hash)
    else:
      raise TypeError("Se esperaba un literal")
  
  def __str__ (self):
    return "( "+" | ".join(map(str,self.literales))+" )"

  def __repr__ (self):
    return self.__str__ ()
  
  def __iter__ (self):
    return (i for i in self.literales)

  def __len__(self):
    return len(self.literales)
  
  def copy (self):
    return Clausula(self.literales.copy(), self.frozen_hash)