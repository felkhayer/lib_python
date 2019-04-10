# -*- coding: utf-8 -*-
import xml.sax.saxutils as saxutils

def identity_filter(element_tuple):
	"""
		element_tuple est consitute des (name, attrs) de chaque element XML recupere par la methode startElement 
	"""
	return element_tuple

class FilteredXMLGenerator(saxutils.XMLGenerator):
	"""
		Permet de creer un fichier XML alteré d'après la function filter_func.
		filter_func peut renvoyer 
			- un tuple (name: String, attrs: [xml.sax.Attributes])
			- None --> l'element XML ainsi que tous ses enfants seront retire de la sortie.
		
		ALERT : ne pas modifier le *name* de l'element XML par la fonction filter_func 
			Si on modifie le *name* de l'element XML dans la fonction filter_func il n'est pas pris en compte par l'evenement endElement
			il en resulte un fichier XML incorrecte
	"""
	def __init__(self, filter_func=identity_filter, out=None, encoding='iso-8859-1', short_empty_elements=False):
		super().__init__(out, encoding, short_empty_elements)
		self.__filter_func = filter_func
		self.__filtered_stack = []
	
	def startElement(self, name, attrs):
		if self.__filtered_stack:
			self.__filtered_stack.append((name, attrs))
		else:
			transformed_element = self.__filter_func((name, attrs))
			if not transformed_element:
				self.__filtered_stack.append((name, attrs.copy())) # 'attrs' est copié car il peut etre reutilisé par le parser par la suite.
			else:
				(transformed_name, transformed_attrs) = transformed_element
				super().startElement(transformed_name, transformed_attrs)
			
	def characters(self, content):
		if self.__filtered_stack:
			pass
		else:
			super().characters(content)
		
	def endElement(self, name):
		"""
			TODO: prise en compte du nom de l'element modifié par filter_func
		"""
		if self.__filtered_stack:
			(filtered_name, filtered_attrs) = self.__filtered_stack.pop()
			if name != filtered_name:
				raise Exception("Balises incoherentes : '%s' fermant '%s'" % (name, filtered_name))
		else:
			super().endElement(name)