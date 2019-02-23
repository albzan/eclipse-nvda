# Eclipse Enhance

## [Download the latest version of the addon](https://github.com/albzan/eclipse-nvda/releases/download/0.2/eclipseEnhance-0.3.nvda-addon)

This NVDA Add-on offers an enhanced support while working in the eclipse IDE.

## Add-On Features:
### Main Features:
* Play different sounds while you use the Eclipse shortcut **CTRL+. (dot)** to identify whether an error or a warning is selected.
* Play different sounds when you press **CTRL+S** to indicate if the saved file contains errors / warnings.
* Play a sound when the Eclipse's **ContentAssist** code completion pops-up. You can access it by pressing the TAB Key;
* Announce the breackpoint toggle while pressing **CTRL+SHIFT+B**.
* Play a sound when you are in the editor during debug and you move on a line containing a breakpoint or in the current paused line.

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
* Pawel Urbanski
* Alessandro Albano

