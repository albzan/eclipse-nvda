#eclipseEnhance - NVDA Addon that improves access to the Eclipse IDE
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-06-27
#Copyright (C) 2021 Alberto Zanella <lapostadialberto@gmail.com>

OLD_BEHAVIOR = False

if OLD_BEHAVIOR :
	from . import eclipse_legacy as base_eclipse
	AutocompletionListItem = None
else :
	from nvdaBuiltin.appModules import eclipse as base_eclipse
	try:
		from nvdaBuiltin.appModules.eclipse import AutocompletionListItem
	except ImportError:
		AutocompletionListItem = None

from scriptHandler import script
import addonHandler
import eventHandler
import controlTypes
from comtypes import COMError
import nvwave
import tones
import api
import textInfos
import braille
from NVDAObjects.behaviors import EditableTextWithAutoSelectDetection as Edit
from NVDAObjects.IAccessible import IA2TextTextInfo
import globalCommands
import globalVars
import ui
import os.path
import oleacc
import winUser
import mouseHandler
import speech

addonHandler.initTranslation()

#Addon consts
ADDON_NAME = "eclipseEnhance"
PLUGIN_DIR = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons",ADDON_NAME))

#Global consts
RGB_ERROR = 'rgb(2550128)'
RGB_WARN = 'rgb(24420045)'
RGB_BP = 'rgb(00255)'
RGB_DBG = 'rgb(198219174)'

class SelectionChangeTextInfo(IA2TextTextInfo) :
	def expand(self, unit) :
		super(SelectionChangeTextInfo,self).expand(unit)
		self._startOffset = self._getCaretOffset()

class EclipseTextArea(base_eclipse.EclipseTextArea,Edit):
	oldpos = -1
	def _caretMovementScriptHelper(self, gesture, unit) :
		orig_tx = self.TextInfo
		if unit == textInfos.UNIT_WORD : self.TextInfo = SelectionChangeTextInfo
		super(EclipseTextArea,self)._caretMovementScriptHelper(gesture, unit)
		self.TextInfo = orig_tx
	
	def event_gainFocus(self) :
		super(EclipseTextArea,self).event_gainFocus()
		tx = self.makeTextInfo(textInfos.POSITION_SELECTION)
		self.processLine(tx)
		
	def reportFocus(self):
		if(self.appModule.lastFocusOnSuggestions) :
			self.appModule.lastFocusOnSuggestions = False
			self._reportText()
			return
		super(EclipseTextArea,self).reportFocus()

			
	def _reportText(self):
		tx = self.makeTextInfo(textInfos.POSITION_SELECTION)
		if not tx.isCollapsed:
			# Translators: This is spoken to indicate what has been selected. for example 'selected hello world'
			speech.speakSelectionMessage(_("selected %s"),tx.text)
		else:
			tx.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(tx,unit=textInfos.UNIT_LINE,reason=controlTypes.OutputReason.CARET)
			
	
	def event_caret(self) :
		super(Edit, self).event_caret()
		if OLD_BEHAVIOR == False :
			super(base_eclipse.EclipseTextArea, self).event_caret()
		if self is api.getFocusObject() and not eventHandler.isPendingEvents('gainFocus'):
			self.detectPossibleSelectionChange()
		try :
			tx = self.makeTextInfo(textInfos.POSITION_SELECTION)
			tx.collapse()
			tx.expand(textInfos.UNIT_LINE)
			if self.oldpos == tx._startOffset :
				return
			self.processLine(tx)
		except: pass
		
	def processLine(self,tx) :
		self.oldpos = tx._startOffset
		tx.collapse()
		tx.expand(textInfos.UNIT_CHARACTER)
		colors = self._hasBackground([RGB_BP,RGB_DBG],tx)
		if colors[RGB_BP] : 
			tones.beep(610,80)
		if colors[RGB_DBG] :
			tones.beep(310,160)
		
	def _caretScriptPostMovedHelper(self, speakUnit, gesture, info=None):
		if not info:
			try:
				info = self.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
		info.expand(textInfos.UNIT_CHARACTER)
		if (speakUnit == textInfos.UNIT_WORD) and (info.text == "\r\n") :
			super(EclipseTextArea,self)._caretScriptPostMovedHelper(textInfos.UNIT_CHARACTER, gesture, info)
		else :
			super(EclipseTextArea,self)._caretScriptPostMovedHelper(speakUnit, gesture, info)
	
	def script_breakpointToggle(self,gesture) :
		colors = self._hasBackground([RGB_BP])
		if(colors[RGB_BP]) : 
			ui.message(_("Breakpoint off"))
		else :
			ui.message(_("Breakpoint on"))
		gesture.send()
	
	def script_errorReport(self,gesture) :
		gesture.send()
		colors = self._hasBackground([RGB_ERROR,RGB_WARN])
		if(colors[RGB_ERROR]) : 
			braille.handler.message(_("\t\t error %% error"))
			self.appModule.play_error()
		elif(colors[RGB_WARN]) :
			braille.handler.message(_("\t\t warning %% warning"))
			self.appModule.play_warning()
		globalCommands.commands.script_reportCurrentLine(gesture)
	
	def script_checkAndSave(self,gesture) :
		gesture.send()
		colors = self._hasBackground([RGB_ERROR,RGB_WARN],ti=self.makeTextInfo(textInfos.POSITION_ALL))
		if colors[RGB_ERROR] : 
			braille.handler.message(_("\t\t saved with errors %% saved with errors"))
			self.appModule.play_error()
		elif colors[RGB_WARN] : 
			braille.handler.message(_("\t\t saved with warnings %% saved with warnings"))
			self.appModule.play_warning()
			
	def _hasBackground(self,colors,ti=None) :
		cfg = {
			"detectFormatAfterCursor":False,
			"reportFontName":False,"reportFontSize":False,"reportFontAttributes":False,"reportColor":True,"reportRevisions":False,
			"reportStyle":False,"reportAlignment":False,"reportSpellingErrors":False,
			"reportPage":False,"reportLineNumber":False,"reportTables":False,
			"reportLinks":False,"reportHeadings":False,"reportLists":False,
			"reportBlockQuotes":False,"reportComments":False,
		}
		retval = dict((color,False) for color in colors)
		if not ti :
			ti = self.makeTextInfo(textInfos.POSITION_SELECTION)
			ti._endOffset = ti._startOffset
			ti.collapse()
			ti.expand(textInfos.UNIT_CHARACTER)
		formatField=textInfos.FormatField()
		for field in ti.getTextWithFields(cfg):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField):
				if 'background-color' in field.field :
					formatField.update(field.field)
					rgb = formatField['background-color']
					if rgb in retval :
						retval[rgb] = True
		return retval
	
	
	
	__gestures = {
		"kb:control+.": "errorReport",
		"kb:control+s": "checkAndSave",
		"KB:control+shift+b":"breakpointToggle",
		"kb:control+shift+downArrow": "caret_moveByLine",
		"kb:control+shift+upArrow": "caret_moveByLine",
		"kb:control+shift+p": "caret_moveByLine",
		"kb:f5": "caret_moveByLine",
		"kb:f6": "caret_moveByLine",
		"kb:f7": "caret_moveByLine",
		"kb:f8": "caret_moveByLine",
		"kb:control+q": "caret_moveByLine",
		"kb:control+d": "caret_moveByLine",
		"kb:control+k": "caret_moveByLine",
		"kb:control+shift+k": "caret_moveByLine",
	}
	
	
class AppModule(base_eclipse.AppModule):
	terminateButton = None
	openConsoleButton = None
	pinConsoleButton = None
	lastFocusOnSuggestions = False

	def _get_statusBar(self):
		foreground = api.getForegroundObject()
		obj = foreground.simpleFirstChild

		while obj:
			if obj.role == controlTypes.Role.STATUSBAR:
				return obj.simpleFirstChild

			obj = obj.simpleNext

		return None

	def get_tool_button(self,myAccName,myAccRole,myObj) :
		if myObj != None : return myObj
		obj = api.getFocusObject()
		while (obj.parent is not None) :
			if (obj.role == controlTypes.Role.TABCONTROL) and (obj.name == 'Console') :
				break
			obj = obj.parent
		if obj.name != "Console" : return myObj
		obj = obj.firstChild
		while obj :
			objs = obj
			while objs and objs.role != controlTypes.Role.TOOLBAR :
				objs = objs.firstChild
			obj = obj.next
			if not objs : continue
			for i in range(1,objs.childCount+1) :
				if objs.IAccessibleObject.accRole(i) == myAccRole and objs.IAccessibleObject.accName(i) == myAccName : 
					return objs.children[i-1]
		
		if myAccName == "Terminate" : #Terminate button may have no accName
			return self.get_tool_button(None,myAccRole,myObj)
	
	def get_terminate_button(self) :
		self.terminateButton = self.get_tool_button("Terminate", oleacc.ROLE_SYSTEM_PUSHBUTTON, self.terminateButton)
		
	def get_open_console_button(self) :
		self.openConsoleButton = self.get_tool_button("Open Console", oleacc.ROLE_SYSTEM_SPLITBUTTON, self.openConsoleButton)
	
	def get_pin_console_button(self) :
		self.pinConsoleButton = self.get_tool_button("Pin Console", oleacc.ROLE_SYSTEM_CHECKBUTTON, self.pinConsoleButton)
	
	
	
	def event_gainFocus(self,obj,nh):
		if obj.role == controlTypes.Role.PANE and self.lastFocusOnSuggestions :
			return
		nh()
	
	def event_focusEntered(self,obj,nh):
		if obj.role == controlTypes.Role.TABCONTROL and self.lastFocusOnSuggestions :
			return
		nh()
	
	def event_NVDAObject_init(self, obj):
		super(AppModule, self).event_NVDAObject_init(obj)
		
		if obj.role == controlTypes.Role.DIALOG and "show Template Proposals" in obj.description :
			# Remove annoying tooltips
			obj.description = ""
			self.lastFocusOnSuggestions = True
		
		if obj.windowClassName == "SysListView32" and obj.role == controlTypes.Role.LISTITEM:
			if(isinstance(api.getFocusObject(),  EclipseTextArea)) :
				self.play_suggestions()

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		super(AppModule, self).chooseNVDAObjectOverlayClasses(obj, clsList)
		if obj.windowClassName == "SWT_Window0" and obj.role == controlTypes.Role.EDITABLETEXT:
			clsList.remove(base_eclipse.EclipseTextArea)
			clsList.insert(0, EclipseTextArea)
		# Autocompletion items are placed outside the main eclipse window
		if (
				AutocompletionListItem is not None and
				AutocompletionListItem not in clsList and
				obj.role == controlTypes.Role.LISTITEM
				and obj.parent.parent.parent.role == controlTypes.Role.DIALOG
				and obj.parent.parent.parent.simpleParent == api.getDesktopObject()
				and obj.parent.parent.parent.parent.simpleNext.role in (
					controlTypes.Role.BUTTON,
					controlTypes.Role.TOGGLEBUTTON
				)
			):
				clsList.insert(0, AutocompletionListItem)

	
	def play_suggestions(self) :
		wfile  = os.path.join(PLUGIN_DIR, "sounds", "suggestions.wav")
		nvwave.playWaveFile(wfile)
	
	def play_error(self) :
		wfile  = os.path.join(PLUGIN_DIR, "sounds", "error.wav")
		nvwave.playWaveFile(wfile)
	
	def play_warning(self) :
		wfile  = os.path.join(PLUGIN_DIR, "sounds", "warn.wav")
		nvwave.playWaveFile(wfile)
	
	
	@script(
		description=_("Click the Open Console toolbar button"),
		category="Eclipse",
		gestures=["kb:nvda+shift+o"]
	)
	def script_clickOpenConsoleButton(self, gesture) :
		self.get_open_console_button()
		if self.openConsoleButton != None :
			try :
				self.openConsoleButton.doAction()
			except:
				pass

	@script(
		description=_("Click the Pin Console toolbar button"),
		category="Eclipse",
		gestures=["kb:nvda+shift+p"]
	)
	def script_clickPinConsoleButton(self, gesture) :
		self.get_pin_console_button()
		if self.pinConsoleButton != None :
			try :
				oldX,oldY = winUser.getCursorPos()
				winUser.setCursorPos(self.pinConsoleButton.location.left,self.pinConsoleButton.location.top)
				#perform Mouse Left-Click
				mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN,0,0)
				mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP,0,0)
				winUser.setCursorPos(oldX,oldY)
				if controlTypes.State.CHECKED in self.pinConsoleButton.states :
					ui.message(_("Pin Console")+" "+_("not checked"))
				else :
					ui.message(_("Pin Console")+" "+_("checked"))
			except:
				pass

	
	@script(
		description=_("Click the terminate toolbar button"),
		category="Eclipse",
		gestures=["kb:NVDA+shift+t"]
	)
	def script_clickTerminateButton(self, gesture):
		self.get_terminate_button()
		if self.terminateButton != None :
			try :
				self.terminateButton.doAction()
				ui.message(_("Terminated"))
			except:
				pass
	

	def script_braille_scrollBack(self, gesture):
		try :
			globalCommands.commands.script_braille_scrollBack(gesture)
		except COMError :
			globalCommands.commands.script_braille_previousLine(gesture)
