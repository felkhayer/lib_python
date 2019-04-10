# lib_python
useful technical python tools

## saxFilteredXMLGenerator
Extension of sax.saxutils.XMLGenerator. 
P
roduce a filtered XML even for very big XML (several Gb). As stream (thanks Sax) there's no limit in size.

A filter_func has to be defined. It's must return None for input sax element (name, attrs) to filter it and all it's children.
