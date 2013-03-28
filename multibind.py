
# Sublime Text imports
import sublime, sublime_plugin
# Python imports
from collections import defaultdict
import socket



if True:

	# NEW
	class ruleSet():
		"""	multibind.[barrierName]:[parameter] """

		_env = {}

		def __init__(self):
			self._env['platform'] = sublime.platform()
			self._env['hostname'] = socket.gethostname().lower()
			self._env['test'] = "test"
		
		def default_rule(self,*arg,**kwargs):
			return False

		def platform(self, param):
			return param == self._env['platform']

		def hostname(self, param):
			return param == self._env['hostname']

		def test(self, param):
			return param == self._env['test']



	####### End of rules #######

		def __iter__(self):
			for key in self.__class__.__dict__.keys():
				if not key.startswith("_"):
					yield (key,self.__getattribute__(key))

		def __getattr__(self, key):
			if key.startswith("_"):
				raise AttributeError
			setattr(self, key, self.default_rule)
			return self.default_rule

		def __getitem__(self, key):
			return getattr(self, key)


	# NEW
	class boolDict(dict):
		"""	multibind.[barrierName] """

		default_value = False

		def __missing__(self, key):
			res = self[key] = self.default_value
			return res

		def reset(self):
			val = self.default_value
			self.update( (key,val) for key in self )

		def toggle(self, keys)            : self.update( (key,not self[key]) for key in keys )
		def enable_only(self, keys)       : self.update( (key, key in keys) for key in self.keys() )

		def set(self, keys, newVal =True) : self.update( (key, newVal==True) for key in keys )

		def enable(self, keys)            : return self.set(keys, True)
		def disable(self, keys)           : return self.set(keys, False)

		def getAll(self, state =True)     : return [ key for key in self.keys() if self[key] == state ]

		def enabled(self)                 : return self.getAll(True)
		def disabled(self)                : return self.getAll(False)


	# NEW
	class MultiBind:
		debug      = False
		# debugState = True

		# NEW
		barriers      = boolDict()
		auto_barriers = ruleSet()


		def reset(self, name):
			MultiBind.debug      = False
			# MultiBind.debugState = False
			# NEW
			MultiBind.barriers.reset()

		# Toggle Command
		def actionToggle(self, options):
			# NEW
			barrier = options['layout'] # Temporary variable
			MultiBind.barriers.toggle([barrier])
			self.doFeedback("MultiBind: Now using "+str(MultiBind.barriers.enabled())+" keymap(s)", True)

		# Show Active Command
		def actionShow(self, options):
			# NEW
			self.doFeedback("MultiBind: Currently using "+str(MultiBind.barriers.enabled())+" keymap(s)", True)


		# Binding Contexts Handler
		def barrierHandler(self, key, operand):
			# New version
			if not key.startswith('multibind.'):
				return None

			prefix, barrier = key.split('.')
			if ':' not in barrier:
				# print("------ ",barrier)
				return MultiBind.barriers[barrier] == operand

			barrier, param = barrier.split(':')
			# print("------ ",barrier," : ",param)
			return MultiBind.auto_barriers[barrier](param) == operand

		# Feedback Controller
		def doFeedback(self, msg, inStatusbar =False):
			if inStatusbar:
				sublime.status_message(msg)
			if MultiBind.debug:
				print(msg)

		# Debug Controller
		# def doDebug(self, layoutName, operand =True): # , inStatusbar =False
		# 	if MultiBind.debugState:
		# 		res = MultiBind.chk( layoutName ) == operand
		# 		print( "MultiBind: -Request " + ("allowed" if res else "stopped") )


	# Create instance of MultiBind
	g_multibind = MultiBind()


	# Multibind Listener
	class MultibindListener(sublime_plugin.EventListener):
		def on_query_context(self, view, key, op, operand, match_all):
			return g_multibind.barrierHandler(key, operand)


	# Toggle Command
	class MultibindToggleCommand(sublime_plugin.TextCommand):
		def run(self, edit, **args):
			g_multibind.actionToggle( args )


	# Show Active Command In Console
	class MultibindShowCommand(sublime_plugin.TextCommand):
		def run(self, edit, **args):
			g_multibind.actionShow( args )