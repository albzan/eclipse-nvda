#eclipseEnhance - NVDA Addon that improves access to the Eclipse IDE
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 Alberto Zanella, Alessandro Albano

import tones
from logHandler import log
import appModuleHandler
import addonHandler
from comtypes import COMError
import nvwave
import controlTypes
import api
import textInfos
import braille
from NVDAObjects.IAccessible import IAccessible
import globalCommands
import globalVars
import os.path
import ui
from NVDAObjects.behaviors import EditableText as Edit
import eventHandler

addonHandler.initTranslation()

ADDON_NAME = "eclipseEnhance"
PLUGIN_DIR = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons",ADDON_NAME))

class EclipseTextArea(IAccessible,Edit):
	oldpos = -1
	
	def event_gainFocus(self) :
		super(IAccessible, self).event_gainFocus()
		tx = self.makeTextInfo(textInfos.POSITION_SELECTION)
		self.processLine(tx)
		
	def event_caret(self) :
		super(Edit, self).event_caret()
		if self is api.getFocusObject() and not eventHandler.isPendingEvents('gainFocus'):
			self.detectPossibleSelectionChange()
		tx = self.makeTextInfo(textInfos.POSITION_SELECTION)
		tx.collapse()
		tx.expand(textInfos.UNIT_LINE)
		if self.oldpos == tx._startOffset :
			return
		self.processLine(tx)
		
	def processLine(self,tx) :
		self.oldpos = tx._startOffset
		tx.collapse()
		tx.expand(textInfos.UNIT_CHARACTER)
		formatField=textInfos.FormatField()
		for field in tx.getTextWithFields(self.appModule.cfg):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField):
				formatField.update(field.field)
		if(not formatField.has_key('background-color')) :
			return
		else :
			rgb = formatField['background-color']
			if(rgb == self.appModule.RGB_BP) : 
				tones.beep(610,80)
			if(rgb == self.appModule.RGB_DBG) :
				tones.beep(310,160)

	def event_valueChange(self):
		# #2314: Eclipse incorrectly fires valueChange when the selection changes.
		# Unfortunately, this causes us to speak the entire selection
		# instead of just the changed selection.
		# Therefore, just drop this event.
		pass


class AppModule(appModuleHandler.AppModule):
	terminateButton = None
	RGB_ERROR = 'rgb(2550128)'
	RGB_WARN = 'rgb(24420045)'
	RGB_BP = 'rgb(00255)'
	RGB_DBG = 'rgb(198219174)'
	cfg = {
			"detectFormatAfterCursor":False,
			"reportFontName":False,"reportFontSize":False,"reportFontAttributes":False,"reportColor":True,"reportRevisions":False,
			"reportStyle":False,"reportAlignment":False,"reportSpellingErrors":False,
			"reportPage":False,"reportLineNumber":False,"reportTables":False,
			"reportLinks":False,"reportHeadings":False,"reportLists":False,
			"reportBlockQuotes":False,"reportComments":False,
		}
		
	
	def get_terminate_button(self) :
		if self.terminateButton != None : return
		obj = api.getFocusObject()
		while (obj.parent is not None) :
			if (obj.role == controlTypes.ROLE_TABCONTROL) and (obj.name == 'Console') :
				break
			obj = obj.parent
		if obj.name != "Console" : return
		while obj.role is not controlTypes.ROLE_TOOLBAR :
			obj = obj.firstChild
		for i in xrange(1,obj.childCount) :
			if obj.IAccessibleObject.accName(i) == "Terminate" : 
				self.terminateButton = obj.children[i-1]
				return
			
	
	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "SysTreeView32" and obj.role in (controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_CHECKBOX) and controlTypes.STATE_FOCUSED not in obj.states:
			# Eclipse tree views seem to fire a focus event on the previously focused item before firing focus on the new item (EclipseBug:315339).
			# Try to filter this out.
			obj.shouldAllowIAccessibleFocusEvent = False
		if obj.role == controlTypes.ROLE_DIALOG and "show Template Proposals" in obj.description :
			# Remove annoying tooltips
			obj.description = ""

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "SWT_Window0" and obj.role == controlTypes.ROLE_EDITABLETEXT:
			clsList.insert(0, EclipseTextArea)


	def script_breakpointtoggle(self,gesture) :
		info = api.getFocusObject().makeTextInfo(textInfos.POSITION_SELECTION)
		info._endOffset = info._startOffset
		info.collapse()
		info.expand(textInfos.UNIT_CHARACTER)
		formatField=textInfos.FormatField()
		for field in info.getTextWithFields(self.cfg):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField):
				formatField.update(field.field)
		if(not formatField.has_key('background-color')) :
			ui.message(_("Breakpoint on"))
		else :
			rgb = formatField['background-color']
			if(rgb == self.RGB_BP) : 
				ui.message(_("Breakpoint off"))
			else :
				ui.message(_("Breakpoint on"))
		gesture.send()
	
	def script_errorReport(self,gesture) :
		gesture.send()
		info = api.getFocusObject().makeTextInfo(textInfos.POSITION_SELECTION)
		info._endOffset = info._startOffset
		info.collapse()
		info.expand(textInfos.UNIT_CHARACTER)
		formatField=textInfos.FormatField()
		for field in info.getTextWithFields(self.cfg):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField):
				formatField.update(field.field)
		if(not formatField.has_key('background-color')) :
			return
		rgb = formatField['background-color']
		if(rgb == self.RGB_ERROR) : 
			braille.handler.message(_("\t\t error %% error"))
			self.play_error()
		elif(rgb == self.RGB_WARN) :
			braille.handler.message(_("\t\t warning %% warning"))
			self.play_warning()
		globalCommands.commands.script_reportCurrentLine(gesture)
	
	#Used for:
	#jump to previous / jump to next method in editor
	#jump to previous / jump to next brachets in editor
	#in debug mode F5 / F6 / F7 / F8 read current line in editor
	def script_readfocusline(self,gesture) :
		gesture.send()
		globalCommands.commands.script_reportCurrentLine(gesture)
	
	def script_checkAndSave(self,gesture) :
		gesture.send()
		info = api.getFocusObject().makeTextInfo(textInfos.POSITION_ALL)
		formatField=textInfos.FormatField()
		foundErrors = False
		foundWarnings = False
		for field in info.getTextWithFields(self.cfg):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField):
				if field.field.has_key('background-color') :
					formatField.update(field.field)
					rgb = formatField['background-color']
					if (rgb == self.RGB_ERROR) : foundErrors = True
					if (rgb == self.RGB_WARN) : foundWarnings = True

		if(foundErrors) : 
			braille.handler.message(_("\t\t saved with errors %% saved with errors"))
			self.play_error()
		elif(foundWarnings) :
			braille.handler.message(_("\t\t saved with warnings %% saved with warnings"))
			self.play_warning()
	
	def play_error(self) :
		wfile  = os.path.join(PLUGIN_DIR, "sounds", "error.wav")
		nvwave.playWaveFile(wfile)
	
	def play_warning(self) :
		wfile  = os.path.join(PLUGIN_DIR, "sounds", "warn.wav")
		nvwave.playWaveFile(wfile)
	
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
		
	__gestures = {
		"kb:control+.": "errorReport",
		"kb:control+s": "checkAndSave",
		"kb:nvda+shift+t": "clickTerminateButton",
		"KB:control+shift+b":"breakpointtoggle",
		"kb:control+shift+downArrow": "readfocusline",
		"kb:control+shift+upArrow": "readfocusline",
		"kb:control+shift+p": "readfocusline",
		"kb:f5": "readfocusline",
		"kb:f6": "readfocusline",
		"kb:f7": "readfocusline",
		"kb:f8": "readfocusline",
	}
