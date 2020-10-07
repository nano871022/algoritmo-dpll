class DPLL:
    """
    DPLL algorithm

    Para tu tarea de programación tenemos la clase DPLL.
    Hemos agregado el cascarón del método que deberás implementar.
    El método se denomina 'satisfiable' y recibe como entrada una <b>fórmula en FNC</b>.

    Hemos agregado la primera verificación que hace el algoritmo para que veas como debes entregar la respuesta.

    Se espera que el método regrese una tupla con dos elementos.

    El primer elemento de la tupla de respuesta es un valor booleano: verdadero si la fórmula es satisfactible, falso si no lo es.

    El segundo elemento de la tupla es una asignación en caso de que la fórmula sea satisfactible. En caso de que la fórmula no sea satisfactible deberás regresar None en el segundo elemento de la tupla, es decir la tupla deberá ser (False,None).

    """
    @staticmethod
    def satisfiable(phi,reporter=None):
        """
        determines if phi is satisfiable
        :param phi: a CNF formula
        """
        if phi.empty_sentence():
            return (True,phi.asignamiento)