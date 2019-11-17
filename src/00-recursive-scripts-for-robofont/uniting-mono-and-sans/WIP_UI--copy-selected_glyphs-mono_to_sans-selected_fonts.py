from vanilla import FloatingWindow, Button, EditText, TextBox
from mojo.UI import Message
from mojo.roboFont import OpenWindow
from vanilla.dialogs import *

class GlyphFax(object):

    def __init__(self):
        '''Initialize the dialog.'''
        x = y = padding = 10
        buttonHeight = 20
        windowWidth = 320
        
        rows = 4
        
        self.w = FloatingWindow((windowWidth, buttonHeight*rows + padding*(rows)), "Glyph Fax Machine")

        self.fonts = {}
        
        self.w.textBox = TextBox((x, y, -padding, buttonHeight), "Glyphs to copy (space-separated list)")
        
        y += buttonHeight 
        
        self.w.editText = EditText((x, y, -padding, buttonHeight*2+padding))

        y += buttonHeight*2 + padding*2

        self.w.sans2mono = Button(
                (x, y, windowWidth/3 - padding/2, buttonHeight),
                "Sans → Mono",
                callback=self.sans2monoCallback)

        self.w.mono2sans = Button(
                (windowWidth/3 + padding, y, -padding, buttonHeight),
                "Mono → Sans",
                callback=self.mono2SansCallback)

        self.w.open()

    def copyGlyph(glyphName, fontToCopyFrom, fontToSendTo):

        if glyphName not in fontToSendTo:
            fontToSendTo.newGlyph(glyphName)

        glyphToCopy = fontToCopyFrom[glyphName]
        layerGlyph = fontToSendTo[glyphName].getLayer("foreground")

        # get the point pen of the layer glyph
        pen = layerGlyph.getPointPen()
        # draw the points of the imported glyph into the layered glyph
        glyphToCopy.drawPoints(pen)

        layerGlyph.width = g.width

        for anchor in layerGlyph.anchors:
            layerGlyph.appendAnchor(anchor.name, (anchor.x, anchor.y))

    def glyphsToCopy(self,sender):
        if self.w.editText.get() == "":
            Message('no glyphs listed', title='Glyph Fax Machine', informativeText='Please list glyphs to send copies of!')
            return
        
        return self.w.editText.get().split(" ")

    def getFonts(self, proportionToCopyFrom):
        files = getFile("Select UFOs to copy glyphs between",
                allowsMultipleSelection=True, fileTypes=["ufo"])

        for path in files:
            f = OpenFont(path, showInterface=False)
            # style = f.info.styleName
            variation = f.info.styleName.replace('Mono ','').replace('Sans ','')
            if variation not in self.fonts.keys():
                self.fonts[variation] = []

            if self.fonts[variation] == []:
                self.fonts[variation].append(f)
            elif self.fonts[variation] != []:
                # if 'Mono' already in list, put 'Sans' second
                if proportionToCopyFrom in self.fonts[variation][0].info.styleName:
                    self.fonts[variation].append(f)
                # else put 'Mono' first
                else:
                    self.fonts[variation] = [f] + self.fonts[variation]

        for variation in self.fonts.keys():
            print(variation)

            for glyphName in glyphsToCopy:
                copyGlyph(glyphName, self.fonts[variation][0], self.fonts[variation][1])

            for f in self.fonts[variation]:
                print('\t', f)
                f.close()


    def mono2SansCallback(self, sender):
        '''Copy glyphs from Mono to Sans masters.'''

        glyphsToCopy = self.glyphsToCopy(sender)

        if glyphsToCopy is not None:
            self.getFonts('Mono')

    def sans2monoCallback(self, sender):
        '''Copy glyphs from Sans to Mono masters.'''

        glyphsToCopy = self.glyphsToCopy(sender)

        if glyphsToCopy is not None:
            self.getFonts('Sans')



if __name__ == '__main__':

    OpenWindow(GlyphFax)