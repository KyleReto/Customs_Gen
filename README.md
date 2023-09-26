Fair warning, the below instructions haven't been tested in a while and may not be up to date. Feel free to contact @Shabacka for help if something breaks.

***Development Setup Instructions:***

1. In VSCode, activate the virtual environment:   
    Use `Ctrl+Shift+P` to open the command palette.   
    Type `Python: Create Environment` into the command palette.   
    Select `Venv` from the list.   
    If prompted, select some variant of Python 3.11 as your interpreter.   
    If prompted, check the box to install `requirements.txt`, then click "OK".   
2. Ensure that your terminal in VSCode says `(.venv)` in green. If it does, you're all set!   
   
If prompted to update dependencies, use `pip install -r requirements.txt` in VSCode's terminal.   
Ensure that your terminal says `(.venv)` before you do this.

***Template Creation Instructions:***
Create a folder for your template in the templates directory.   
Create a `template_info.json` file for your template by copying and editing the example.   
For your fonts, download a `.ttf` or `.otf` file for each font you plan to use, and place them anywhere in your template folder.   
Edit `template_info.json` so that the file paths match up with wherever you put your fonts. For example, in the `street_fighter` template, the fonts are in a `fonts` folder, and within that folder each has its own name. We use WCManoNegraBoldBTA for the card names, so under `"card_names"`, in the section that says `"path":`, we wrote the path to that font: `templates/street_fighter/fonts/WCManoNegraBoldBta.otf`.   
If you'd like to use different styles for a font, place their file paths inside the square brackets(`[]`), separated by commas, in this order: [Regular, Bold, Italic, Bold-Italic]. We highly recommend you do this for your card_effect font at least, as the cards may be difficult to understand without font styles. See the street_fighter template's card_effect section of template_info for an example.   
For your images, download all of the images you plan to use, and place them anywhere in your template folder.   
Edit `template_info.json`'s `path` sections to point to the images you added. The x- and y-offset sections can be edited to fine-tune each image's position if necessary.
