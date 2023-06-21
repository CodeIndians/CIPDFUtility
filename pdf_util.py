import fitz

class PDFUtility:
    def __init__(self, input_file, output_file,color):
        self.output_file = output_file
        self.color = color
        # Open the input PDF
        self.my_pdf = fitz.open(input_file)
    
    def add_bookmarks_from_text(self, search_string):
        
        # navigate through all the pages
        for n_page in self.my_pdf: 
            # search for will return the rects
            matchWordQuads = n_page.search_for(search_string)

            # Add annotations with the specified color for all the acquired rects  
            for wordQuad in matchWordQuads:  
                annot = n_page.add_rect_annot(wordQuad)
                annot.set_border(width=0)
                annot.set_colors(stroke=self.color, fill=self.color)
                annot.set_opacity(0.3)
                annot.update() 

    def save_pdf_file(self):
        # Save the modified PDF with bookmarks and annotations to a new
        self.my_pdf.save(self.output_file)
        print(f"Bookmarks added and Saved as '{self.output_file}'.")
