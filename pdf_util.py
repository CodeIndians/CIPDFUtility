import fitz

class PDFUtility:
    def __init__(self, input_file, output_file,color):
        self.input_file = input_file
        self.output_file = output_file
        self.color = color
    
    def add_bookmarks_from_text(self, search_string):
        # Open the input PDF
        my_pdf = fitz.open(self.input_file)

        for n_page in my_pdf:  
            matchWords = n_page.search_for(search_string)      
            for word in matchWords:  
                annot = n_page.add_rect_annot(word)
                annot.set_border(width=0)
                annot.set_colors(stroke=self.color, fill=self.color)
                annot.set_opacity(0.3)
                annot.update() 

        # Save the modified PDF with bookmarks
        my_pdf.save(self.output_file)
        print(f"Bookmarks added to '{self.input_file}'. Saved as '{self.output_file}'.")
