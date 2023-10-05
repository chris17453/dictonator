import re
import os
import sqlite3
from reportlab.lib.units import inch  
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak  ,  Image
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Frame, NextPageTemplate, PageTemplate, FrameBreak
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, KeepTogether
from hashlib import sha1
from datetime import datetime
import math

pdf_title="Generative AI Fantasy Dictionary"

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('dictionary_entries.db')

# Create a new SQLite cursor
cur = conn.cursor()


# Retrieve data from the database
cur.execute('SELECT * FROM dictionary_entries  ORDER BY word ASC')
rows = cur.fetchall()

# Registering the Font
dejavu_font_path = "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf"  
pdfmetrics.registerFont(TTFont("DejaVuSans", dejavu_font_path))
dejavu_font_path = "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Oblique.ttf"
pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", dejavu_font_path))
dejavu_font_path = "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf"  
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", dejavu_font_path))

font_path = "fonts/GentiumPlus-Italic.ttf"
pdfmetrics.registerFont(TTFont("GentiumPlus-Itallic", font_path))

toc_style = ParagraphStyle(
    'TableOfContents',
    fontName="DejaVuSans",
    fontSize=12,
    leftIndent=20,
)

# Setup PDF
filename = "generated_pdfs/dictionary.pdf"
story = []
styles = getSampleStyleSheet()

# Customizing styles
styles.add(ParagraphStyle(
    name='Header', 
    fontName='DejaVuSans', 
    fontSize=0, 
    spaceBefore=0, 
    spaceAfter=0, 
    leftIndent=0, 
    rightIndent=0

))
styles.add(ParagraphStyle(
    name='TOCText', 
    fontName='DejaVuSans-Oblique', 
    fontSize=10, 
    spaceAfter=12
))
styles.add(ParagraphStyle(
    name='Word', 
    fontName='DejaVuSans-Bold', 
    fontSize=20, 
    textColor=colors.red,
    spaceAfter=12
))
styles.add(ParagraphStyle(
    name='WordType', 
    fontName='DejaVuSans', 
    fontSize=18, 
    textColor=colors.grey,
    spaceAfter=12
))
styles.add(ParagraphStyle(
    name='Def', 
    fontName='DejaVuSans', 
    fontSize=8,
    spaceAfter=12
))
styles.add(ParagraphStyle(
    name='Example', 
    fontName='DejaVuSans', 
    fontSize=8,
    textColor=colors.grey,
    spaceAfter=12,
    leftIndent=20
))
styles.add(ParagraphStyle(
    name='Pronouciation', 
    fontName='GentiumPlus-Itallic', 
    fontSize=8,
    textColor=colors.grey,
    spaceAfter=12,
    leftIndent=20
))


def strip_unsafe_characters(word):
    """
    Remove all characters that are not alphanumeric, hyphens, or underscores from a string.

    Parameters:
    - word (str): The input string.

    Returns:
    - str: The sanitized string.
    """
    # Regular expression pattern to match any character that is NOT alphanumeric, hyphen or underscore
    pattern = re.compile(r'[^\w-]')
    # Replace all matches of the pattern with an empty string
    return pattern.sub('', word)


def draw_background(canvas, doc):
    total_pages=200    
    # Set Background Image
    #canvas.drawImage("template/bg1.png", 0, 0, width=doc.width, height=doc.height)
    #canvas.setFillColor(colors.lightblue)
    #canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
   # Calculate the gradient: for example, red to blue
    red_value = 1 - (doc.page-1)/(total_pages-1)
    blue_value = (doc.page-1)/(total_pages-1)
     # Use sine functions to generate smooth color transitions
    red_value = 0.5 * math.sin(doc.page/2) + 0.5
    green_value = 0.5 * math.sin(doc.page/3) + 0.5
    blue_value = 0.5 * math.sin(doc.page/4) + 0.5
  
    # Set the background color
    canvas.setFillColor(colors.Color(red=red_value, green=green_value, blue=blue_value))
    canvas.rect(0, 0, 30, letter[1], fill=1, stroke=0)




class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        #self.rightMargin = 0
        #self.leftMargin = 0
        #self.topMargin = 30
        #self.bottomMargin = 30
        
        #self.allowSplitting = 0
        self.showBoundary = 0

        # Define a Frame where Table of Contents will be placed
        frameToc = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='toc')
        toc_template = PageTemplate(id='TOC', frames=[frameToc],onPage=draw_background)

        frameContent = Frame(self.leftMargin,self.bottomMargin, self.width,self.height, id='dict')
        dict_template = PageTemplate(id='LaterPages', frames=[frameContent],onPage=draw_background)

        coverContent = Frame(self.leftMargin,self.bottomMargin, self.width,self.height, id='cover')
        cover_template = PageTemplate(id='Cover', frames=[coverContent],onPage=draw_background)


        # Apply this frame to a new page template
        self.addPageTemplates(toc_template)
        self.addPageTemplates(dict_template)
        self.addPageTemplates(cover_template)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Word':
                #print(text,self.page)
                E=[0, text, self.page]
                bn = getattr(flowable,'_bookmarkName',None)
                if bn is not None: E.append(bn)
                self.notify('TOCEntry', E)

def footer(canvas, doc):
    draw_background(canvas,doc)
    canvas.saveState()
    pageNumber = canvas.getPageNumber()
    canvas.setFont("DejaVuSans", 10)
    canvas.setFillColor(colors.black)
    canvas.drawString(doc.leftMargin, doc.bottomMargin - 30, f"© 2023 Watkins Labs")
    canvas.drawString(doc.leftMargin, ppt_size[1]-30 , f"{pdf_title}")

    canvas.drawString(ppt_size[0]-doc.rightMargin-50, doc.bottomMargin - 30, f"Page - {pageNumber}")
    canvas.drawString(ppt_size[0]-doc.rightMargin-50, ppt_size[1]-30 , f"Page - {pageNumber}")
    canvas.restoreState()


ppt_size = (8.5*72, 
            10*72)  

document = MyDocTemplate("generated_pdfs/dictonary.pdf",pagesize=ppt_size)


toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle(fontName='DejaVuSans-Bold', fontSize=12, name='TOCText', leftIndent=20),
    ParagraphStyle(fontName='DejaVuSans-Bold', fontSize=12, name='TOCHeading2', leftIndent=20),
    ParagraphStyle(fontName='DejaVuSans-Bold', fontSize=12, name='TOCHeading3', leftIndent=20),
    ParagraphStyle(fontName='DejaVuSans-Bold', fontSize=12, name='TOCHeading4', leftIndent=20),
]
content=[]
#content.append(toc)
#content.append(PageBreak())


content.append(NextPageTemplate('Cover'))

# Add title page elements

# Suppose you have an image file named 'logo.png' in the same directory as your script.
#content.append(Image('images/watkins-labs-low-resolution-color-logo.png', width=500, height=375))
content.append(Image('template/chris.png',width=480/2, height=509/2))# 

content.append(Spacer(1, 50))  # Add some space below the image

# Add title text
title_style = ParagraphStyle(
    'Title',
    parent=styles['Title'],
    fontSize=24,
    textColor=colors.black,
    alignment=1  # Center alignment
)

copy_style = ParagraphStyle(
    'Copy',
    parent=styles['Title'],
    fontSize=14,
    textColor=colors.black,
    alignment=1  # Center alignment
)
email_style = ParagraphStyle(
    'Copy',
    parent=styles['Title'],
    fontSize=14,
    textColor=colors.blue,
    alignment=1  # Center alignment
)

# Get the current date and time
now = datetime.now()

# Format the date and time in a nice way
formatted_date = now.strftime("%A, %B %d, %Y")


content.append(Paragraph("Generative Lexography", title_style))
content.append(Paragraph("A fantasy dictionary created from automated layered prompting", copy_style))
content.append(Spacer(1, 20))  # Add some space below the title
content.append(Paragraph("<a href=\"https://www.linkedin.com/in/chris17453/\">Chris Watkins</a>", copy_style))
content.append(Paragraph("<a href=\"mailto:chris@watkinslabs.com\">chris@watkinslabs.com</a>", email_style))

print(formatted_date)
content.append(Paragraph(formatted_date, copy_style))

content.append(Spacer(1, 10))  # Add some space below the title

# Add copy text
copy_text_style = ParagraphStyle(
    'CopyText',
    parent=styles['BodyText'],
    fontSize=12,
    textColor=colors.black,
)
content.append(Paragraph("Code Human(AI Assisted), copy and art created by generative AI", copy_text_style))
content.append(Paragraph("Written and polished in 10 hours", copy_text_style))
content.append(Paragraph("Tools: python, VS Code, chatGPT, stable diffusion, elevenlabs", copy_text_style))
content.append(Paragraph("Build time less than 5 minutes", copy_text_style))



content.append(PageBreak())


# Start the document with the TOC page template

# Add a title to the Table of Contents page
toc_title = Paragraph('Table of Contents', styles['Heading1'])
content.append(toc_title)
content.append(Spacer(1, 12))

content.append(NextPageTemplate('TOC'))
content.append(toc)
content.append(PageBreak())
#content.append(FrameBreak())  # Break frame to enable page breaks within TOC

# Switch back to the normal page template for the dictionary entries
content.append(NextPageTemplate('LaterPages'))
content.append(PageBreak())



index=0
for row in rows:
    items=[]
    print(row)
    word, base_word, definition, word_type, pronunciation, example, etymology, synonyms, antonyms, usage_notes, frequency, language, requested_language, prompt, image_scene_prompt = row
    
    
    #items.append(heading)
    bookmark_hash=sha1(word.encode('utf-8')).hexdigest()
    word_text="<a name=\"{1}\"/>".format(word,bookmark_hash)
    header=Paragraph(word_text, styles['Header'])
    items.append(header)
    
    file=os.path.join('images',strip_unsafe_characters(word)+".jpg")
    image = Image(file, width=1024*.7   , height=256*.7)  # adjust width and height as needed
    items.append(image)
    print(word)

    word_p=Paragraph(word, styles['Word'])
    word_p._bookmarkName=bookmark_hash
    
    items.append(Spacer(1, 20))

    items.append(word_p)
    
    items.append(Spacer(1, 20))

    items.append(Paragraph(word_type, styles['WordType']))
    items.append(Paragraph(f"<a href=\"https://watkinslabs.com/dictonary/sounds/{word}.mp3\"> {pronunciation}</a> ", styles['Pronouciation']))
    items.append(Paragraph(definition, styles['Def']))
    items.append(Paragraph(f"e.g. {example}", styles['Example']))
    items.append(Paragraph(f"Etymology: {etymology}", styles['Definition']))
    items.append(Paragraph(f"Usage Notes: {usage_notes}", styles['Definition']))
    items.append(Paragraph(f"Synonyms: {synonyms}", styles['Definition']))
    items.append(Paragraph(f"Antonyms: {antonyms}", styles['Definition']))
    items.append(Paragraph(f"Frequency: {frequency}", styles['Definition']))
    items.append(Paragraph(f"Language: {language}", styles['Definition']))
    items.append(Paragraph(f"AI Gen Seed: {base_word}", styles['Definition']))
    items.append(Spacer(1, 40))

    

    # Wrap dictionary entry in KeepTogether to avoid page breaks within an entry
    entry = KeepTogether(items)
    content.append(entry)
    index=index+1
# Save the PDF
document.multiBuild(content, onFirstPage=footer, onLaterPages=footer)

# Close the SQLite connection
conn.close()



