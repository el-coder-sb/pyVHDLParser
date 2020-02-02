from pathlib import Path
from textwrap import dedent

from pyAttributes.ArgParseAttributes import CommandAttribute

from pyVHDLParser.Base             import ParserException
from pyVHDLParser.Token            import Token, StartOfDocumentToken, EndOfDocumentToken
from pyVHDLParser.Token.Parser     import Tokenizer
from pyVHDLParser.Blocks           import TokenToBlockParser, Block, StartOfDocumentBlock, EndOfDocumentBlock, CommentBlock
from pyVHDLParser.Blocks.Common    import LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.List      import GenericList, PortList
from pyVHDLParser.Blocks.InterfaceObject import InterfaceConstantBlock, InterfaceSignalBlock
from pyVHDLParser.Blocks.Structural import Entity

from FrontendHandler import FilenameAttribute, translate, FrontEndProtocol, WithTokensAttribute


class BlockStreamHandlers:

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "blockstreaming" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("blockstreaming", help="Create a stream of block objects.", description="Create a stream of block objects.")
	@WithTokensAttribute()
	@FilenameAttribute()
	def HandleBlockStreaming(self: FrontEndProtocol, args):
		self.PrintHeadline()

		file = Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		tokenStream = Tokenizer.GetVHDLTokenizer(content)
		blockStream = TokenToBlockParser.Transform(tokenStream)

		try:
			for block in blockStream:
				if isinstance(block, (LinebreakBlock, IndentationBlock)):
					self.WriteNormal("{DARK_GRAY}{block!r}{NOCOLOR}".format(block=block, **self.Foreground))
				elif isinstance(block, CommentBlock):
					self.WriteNormal("{DARK_GREEN}{block!r}{NOCOLOR}".format(block=block, **self.Foreground))
				elif isinstance(block, (Entity.NameBlock, Entity.NameBlock, Entity.EndBlock)):
					self.WriteNormal("{DARK_RED}{block!r}{NOCOLOR}".format(block=block, **self.Foreground))
				elif isinstance(block, (GenericList.OpenBlock, GenericList.DelimiterBlock, GenericList.CloseBlock)):
					self.WriteNormal("{DARK_BLUE}{block!r}{NOCOLOR}".format(block=block, **self.Foreground))
				elif isinstance(block, (PortList.OpenBlock, PortList.DelimiterBlock, PortList.CloseBlock)):
					self.WriteNormal("{DARK_CYAN}{block!r}{NOCOLOR}".format(block=block, **self.Foreground))
				elif isinstance(block, (InterfaceConstantBlock, InterfaceSignalBlock)):
					self.WriteNormal("{BLUE}{block!r}{NOCOLOR}".format(block=block, **self.Foreground))
				else:
					self.WriteNormal("{YELLOW}{block!r}{NOCOLOR}".format(block=block, **self.Foreground))

				for token in block:
					self.WriteVerbose(repr(token))

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "check-blockstreaming" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("check-blockstreaming", help="Check a stream of block objects.", description="Check a stream of block objects.")
	@WithTokensAttribute()
	@FilenameAttribute()
	def HandleCheckBlockStreaming(self: FrontEndProtocol, args):
		self.PrintHeadline()

		file = Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)
		vhdlBlockStream = TokenToBlockParser.Transform(vhdlTokenStream)

		try:
			blockIterator = iter(vhdlBlockStream)
			firstBlock = next(blockIterator)
			self.WriteVerbose(str(firstBlock))

			if (not isinstance(firstBlock, StartOfDocumentBlock)):
				self.WriteError("{RED}First block is not StartOfDocumentBlock: {block}{NOCOLOR}".format(block=firstBlock, **self.Foreground))
				self.WriteError("{YELLOW}  Block:  {block}{NOCOLOR}".format(block=firstBlock, **self.Foreground))
			startToken = firstBlock.StartToken
			self.WriteDebug(str(startToken))
			if (not isinstance(startToken, StartOfDocumentToken)):
				self.WriteError("{RED}First token is not StartOfDocumentToken: {token}{NOCOLOR}".format(token=startToken, **self.Foreground))
				self.WriteError("{YELLOW}  Token:  {token}{NOCOLOR}".format(token=startToken, **self.Foreground))

			lastBlock: Block = firstBlock
			endBlock: Block = None
			lastToken: Token = startToken

			for vhdlBlock in blockIterator:
				self.WriteNormal(str(vhdlBlock))

				if isinstance(vhdlBlock, EndOfDocumentBlock):
					self.WriteDebug("{GREEN}Found EndOfDocumentBlock...{NOCOLOR}".format(**self.Foreground))
					endBlock = vhdlBlock
					break

				tokenIterator = iter(vhdlBlock)

				for token in tokenIterator:
					self.WriteVerbose(str(token))

					#					if (token.NextToken is None):
					#						self.WriteError("{RED}Token has an open end (NextToken).{NOCOLOR}".format(**self.Foreground))
					#						self.WriteError("{YELLOW}  Token:  {token}{NOCOLOR}".format(token=token, **self.Foreground))
					#					el
					if (lastToken.NextToken is not token):
						self.WriteError("{RED}Last token is not connected to the current token.{NOCOLOR}".format(**self.Foreground))
						self.WriteError("{YELLOW}  Last:   {token!s}{NOCOLOR}".format(token=lastToken, **self.Foreground))
						self.WriteError("{YELLOW}    Next: {token!s}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))
						self.WriteError("")
						self.WriteError("{YELLOW}  Cur.:   {token!s}{NOCOLOR}".format(token=token, **self.Foreground))
						self.WriteError("")

					if (token.PreviousToken is None):
						self.WriteError("{RED}Token has an open end (PreviousToken).{NOCOLOR}".format(**self.Foreground))
						self.WriteError("{YELLOW}  Token:  {token}{NOCOLOR}".format(token=token, **self.Foreground))
					elif (token.PreviousToken is not lastToken):
						print("{RED}Current token is not connected to lastToken.{NOCOLOR}".format(**self.Foreground))
						# print("{RED}  Block:  {block}{NOCOLOR}".format(block=vhdlBlock, **self.Foreground))
						print("{YELLOW}  Cur.:   {token}{NOCOLOR}".format(token=token, **self.Foreground))
						print("{YELLOW}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken, **self.Foreground))
						self.WriteError("")
						print("{YELLOW}  Last:   {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
						print("{YELLOW}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))
						self.WriteError("")

					lastToken = token

				lastBlock = vhdlBlock
			else:
				self.WriteError("{RED}No EndOfDocumentBlock found.{NOCOLOR}".format(**self.Foreground))

			if (not isinstance(endBlock, EndOfDocumentBlock)):
				self.WriteError("{RED}Last block is not EndOfDocumentBlock: {block}{NOCOLOR}".format(block=endBlock, **self.Foreground))
				self.WriteError("{YELLOW}  Block:  {block}{NOCOLOR}".format(block=firstBlock, **self.Foreground))
			elif (not isinstance(endBlock.EndToken, EndOfDocumentToken)):
				self.WriteError("{RED}Last token is not EndOfDocumentToken: {token}{NOCOLOR}".format(token=endBlock.EndToken, **self.Foreground))
				self.WriteError("{YELLOW}  Token:  {token}{NOCOLOR}".format(token=endBlock.EndToken, **self.Foreground))

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.WriteNormal("")
		self.WriteNormal("{CYAN}All checks are done.{NOCOLOR}".format(**self.Foreground))
		self.exit()