# Core imports
import sublime, sublime_plugin

# Python imports
# from collections import namedtuple, defaultdict

# DefaultDict value factory
# def default_factory():  return False


# MultiBind Properties
class MultiBind:
	default    = None
	current    = None
	_options   = ["layout", "alt"]
	debug      = False
	debugState = False


	def reset(self, name):
		MultiBind.default    = None
		MultiBind.current    = None
		MultiBind.debug      = False
		MultiBind.debugState = False
		return True

	# def getDefault(self):
	# 	return MultiBind.default
	def get(self, name =None):
		return str(MultiBind.current or MultiBind.default or "default")
	# def set(self, name, state =True):
	# 	return None
	def chk(self, name =None):
		return MultiBind.current == name
	def toggle(self, name, alt =None):
		MultiBind.current = name if (MultiBind.current != name) else alt


	# Options checks and preparation
	def formatOptions(self, optionsDict):
		for key in self._options:
			if key not in optionsDict:
				  optionsDict[key] = MultiBind.default
			else: optionsDict[key] = str(optionsDict[ key ]) or MultiBind.default


	# Toggle Command
	def actionToggle(self, options):
		self.toggle( options['layout'] )
		self.doFeedback("MultiBind: Now using ["+self.get()+"] keymap", True)

	# Show Current Command
	def actionShow(self, options):
		self.doFeedback("MultiBind: Currently using ["+self.get()+"] keymap", True)


	# Binding Contexts Handler
	def handlerBindingContext(self, key, operand):
		if not key.startswith('multibind.'):
			return None
		prefix, layoutName = key.split('.')
		self.doDebug(layoutName, operand)
		return self.chk(layoutName) == operand


	# Feedback Controller
	def doFeedback(self, msg, inStatusbar =False):
		if inStatusbar:
			sublime.status_message(msg)
		if MultiBind.debug:
			print(msg)

	# Debug Controller
	def doDebug(self, layoutName, operand =True): # , inStatusbar =False
		if MultiBind.debugState:
			res = g_multibind.chk( layoutName ) == operand
			print( "MultiBind: -Request " + ("allowed" if res else "stopped") )


# Create instance of MultiBind
g_multibind = MultiBind()


# Layout Context Handler
class LayoutContextHandler(sublime_plugin.EventListener):
	def on_query_context(self, view, key, op, operand, match_all):
		return g_multibind.handlerBindingContext(key, operand)


# Toggle Command
class MultibindToggleCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		g_multibind.actionToggle( args )


# Show Active Command In Console
class MultibindShowCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		g_multibind.actionShow( args )