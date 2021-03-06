Usage
#####

The following shows two code examples on how to use the block generator. The
first is generator-based. The second one retrieves an iterator from the generator
and uses low-level access to the chain of blocks.

Block Generator
***************

At first, a file is opened and the file content is read into a string buffer
called ``content``. Strings are iterable, thus a string can be an input for the
Tokenizer.

At second, two chained generator objects are created by ``GetVHDLTokenizer(...)``
and ``Transform(...)``.

Finally, a *for*-loop can process each block from :class:`~pyVHDLParser.Blocks.StartOfDocumentBlock`
to :class:`~pyVHDLParser.Blocks.EndOfDocumentBlock`.

.. code-block:: Python

   # Open a source file
   with file.open('r') as fileHandle:
     content = fileHandle.read()

   from pyVHDLParser.Token.Parser      import Tokenizer
   from pyVHDLParser.Blocks            import TokenToBlockParser
   from pyVHDLParser.Base              import ParserException

   # get a token generator
   tokenStream = Tokenizer.GetVHDLTokenizer(content)
   # get a block generator
   blockStream = TokenToBlockParser.Transform(tokenStream)

   try:
     for block in blockStream:
       print("{block!s}".format(block=block))
       for token in block:
         print("  {token!s}".format(token=token))
   except ParserException as ex:
     print("ERROR: {0!s}".format(ex))
   except NotImplementedError as ex:
     print("NotImplementedError: {0!s}".format(ex))



Block Iterator
**************

Similar to the previous example, a stream of blocks is generated by a block
generator. This time, iteration is manually implemented with a *while*-loop. The
function :func:`iter` creates an iterator object from a generator object. At
next, calling :func:`next` returns a new block for each call.

The example wants to print the outer objects (first and last) of the block chain.
So at first, :func:`next` is called once to get the first element. Then an
endless loop is used to generate all blocks. If the generator ends, it raises
a :exec:`StopIteration` exception. The last block will be stored in variable
``lastBlock``.

.. code-block:: Python

   # Open a source file
   with file.open('r') as fileHandle:
     content = fileHandle.read()

   from pyVHDLParser.Token.Parser      import Tokenizer
   from pyVHDLParser.Blocks            import TokenToBlockParser
   from pyVHDLParser.Base              import ParserException

   # get a token generator
   tokenStream = Tokenizer.GetVHDLTokenizer(content)
   # get a block generator
   blockStream = TokenToBlockParser.Transform(tokenStream)

   # get the iterator for that generator
   blockIterator = iter(blockStream)
   firstBlock =    next(blockIterator)

   try:
     while lastBlock := next(blockIterator):
       pass
   except StopIteration:
     pass

   print("first block: {block}".format(block=firstBlock))
   print("last block:  {block}".format(block=lastBlock))



Token Iterator
**************

.. todo::

   Document the token iterator for a block. (limited range)
