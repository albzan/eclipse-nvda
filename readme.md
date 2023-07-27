# Eclipse Enhance

## [Download the latest version of the addon](https://github.com/albzan/eclipse-nvda/releases/download/0.7/eclipseEnhance-0.8.nvda-addon)

This NVDA Add-on offers an enhanced support while working in the eclipse IDE.

## Add-On Features:
### Main Features:
* Play different sounds while you use the Eclipse shortcut **CTRL+. (dot)** to identify whether an error or a warning is selected.
* Play different sounds when you press **CTRL+S** to indicate if the saved file contains errors / warnings.
* Play a sound when the Eclipse's **ContentAssist** code completion pops-up. 
* Let the user to choose if she prefers the new behaviour of NVDA (automatically reading and braille autocompletion) or let the standard Eclipse behaviour where you can access ContentAssist by pressing the TAB Key;
* Announce the breackpoint toggle while pressing **CTRL+SHIFT+B**.
* Play a sound when you are in the editor during debug and you move on a line containing a breakpoint or in the current paused line.
* Fixes the NVDA status bar command to read if there is an error on the current line
* Let the user to click the Terminate button on Console view toolbar (default nvda-shift-t)
* Let the user to click the Pin Console button on Console view toolbar (default nvda-shift-p)
* Let the user to click the Open Console button on Console button on Console view toolbar (default nvda-shift-o)

The latter are expetially useful when multiple output is used. You can use alt+f7 and alt+shift+f7 (Eclipse commands), to navigate through the running application output if you are running more than one program at a time. Useful to choose which app to terminate, or which output you would like to pin to this console view. Only available in the console view.

All key bindings can be redefined within the Input Gestures dialog.

### Additional Braille Features:
* Reports braille messages if you save a file that contains errors and / or warnings;
* Fixes an issues while you can't press the braille scroll back key to move on the previous line

### Additional Speech Features:
* Reports the current line while you move through using debugging keys
* Reports the current line while you press CTRL+. and the cursor moves.
* Reports the current line while you press CTRL+SHIFT+UP/DOWN ARROW and jump to previous / jump to next method
* Reports the current line while you press CTRL+SHIFT+P with a bracket selected: jump to the matching closing or opening bracket

## Eclipse Configuration
In order to take advantages of all the features of this addon, you have to configure Eclipse to highlight errors and warnings instead of underline them.
To do so, proceed as follow:
* Open the Eclipse IDE
* Open the Window Menu (ALT-W)
* Choose the "Preferences" item
* Tab to the tree view
* Navigate to General, then to Editors, Text Editors, Annotations
* Press TAB to move to the list of annotations

For each annotation you can choose:
* Three check boxes (Vertical ruler, Overview ruler and Text As)
* A combo box that indicates how the annotation is presented in the text (Available when the Text check box has been selected).

Set annotations as follow:

* **Breackpoints**: Text As Check Box selected, then TAB and choose "highlighted" from the combo box.
* **Errors**: Text As Check Box selected, then TAB and choose "highlighted" from the combo box.
* **Info**: Text As Check Box Unselected
* **Matching tags**: Text As Check Box Unselected
* **Occurrences**: Text As Check Box Unselected
* **Search Results**: Text As Check Box Unselected
* **Warnings**: Text As Check Box selected, then TAB and choose "highlighted" from the combo box.

## NVDA 2019.2 and next behavior
if you don't like the new NVDA behavior in Eclipse, expetially if you are using a braille display and you don't want to have the line hidden by autocompetition each time **ContentAssist** pops-up, you can enable the old behaviour of NVDA.
In this way, you can access **ContentAssist** pressing the **TAB** key.
To do this, edit the eclipse.py file of this addon, and set the **OLD_BEHAVIOR** variable to **True** . 

## Sounds Copyrights
Sounds used to reports errors and warnings are covered by the Creative Commons License.
* [For the error sound please refer to this page](https://www.freesound.org/people/Autistic%20Lucario/sounds/142608/)
* [For the warning sound please refer to this page](https://www.freesound.org/people/ecfike/sounds/135125/)
* [For the suggestions pop-up sound please refer to this page](https://freesound.org/people/debsound/sounds/320549/)

## Author:
* Alberto Zanella

## Translations:
* Iván Novegil C.

## Contribs:
* Timothy Breitenfeldt
* Pawel Urbanski
* Alessandro Albano

