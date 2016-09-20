from src.Blocks.Base          import Block
from src.Blocks.Common        import EmptyLineBlock, IndentationBlock
from src.Blocks.Comment       import SingleLineCommentBlock, MultiLineCommentBlock
from src.Token.Parser import *
from src.Token.Keywords import *


class SharedVariableBlock(Block):
	def RegisterStates(self):
		return [
			self.stateSharedVariableKeyword,
			self.stateWhitespace1,
			self.stateSharedVariableName,
			self.stateWhitespace2,
			self.stateColon1,
			self.stateWhitespace3,
			self.statePossibleVariableAssignment,
			self.stateVariableAssignment
		]

	@classmethod
	def stateSharedVariableKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword SharedVariable."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace1
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected sharedVariable name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.stateSharedVariableName
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateSharedVariableName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';' after library name."
		if isinstance(token, CharacterToken):
			if (token == ":"):
				parserState.NewToken =    BoundaryToken(token)
				parserState.NextState =   cls.stateColon1
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace2
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected sharedVariable name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == ":"):
				parserState.NewToken =    BoundaryToken(token)
				parserState.NextState =   cls.stateColon1
				return
			elif (token == "-"):
				parserState.NewBlock = SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock = SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken = IdentifierToken(token)
			parserState.NextState = cls.stateColon1()
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateColon1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected typemark or whitespace after ':'."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace3
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace3
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace3
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace3
			return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.stateTypeMarkName
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace3(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected sharedVariable name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock = SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock = SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken = IdentifierToken(token)
			parserState.NextState = cls.stateTypeMarkName
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateTypeMarkName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ':=' or whitespace after type mark."
		if isinstance(token, CharacterToken):
			if (token == ":"):
				parserState.NewToken =    BoundaryToken(token)
				parserState.NextState =   cls.statePossibleVariableAssignment
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace4
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace4(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ':=' after type mark."
		if isinstance(token, CharacterToken):
			if (token == ":"):
				parserState.NewToken =    BoundaryToken(token)
				parserState.NextState =   cls.statePossibleVariableAssignment
				return
			elif (token == "-"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def statePossibleVariableAssignment(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "=")):
			parserState.NewToken =      VariableAssignmentKeyword(parserState.TokenMarker)
			parserState.TokenMarker =   parserState.NewToken
			parserState.NextState =     cls.stateVariableAssignment
			return

		raise NotImplementedError("State=PossibleCommentStart: {0!r}".format(token))

	@classmethod
	def stateVariableAssignment(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ':=' or whitespace after type mark."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken = LinebreakToken(token)
				parserState.NewBlock = SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState = cls.stateWhitespace5
				parserState.PushState = EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock = SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState = cls.stateWhitespace5
				parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock = SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState = cls.stateWhitespace5
				parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState = cls.stateWhitespace5
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace5(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected expression after ':='."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock = SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NextState = cls.stateExpressionEnd
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateExpressionEnd(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';'."
		if isinstance(token, CharacterToken):
			if (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
			elif (token == "-"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    SharedVariableBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return

		raise BlockParserException(errorMessage, token)