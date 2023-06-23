import fitz
import os
from fitz import Point

color_dict = {
    'Red': (1.0, 0.0, 0.0),
    'Green': (0.0, 1.0, 0.0),
    'Blue': (0.0, 0.0, 1.0),
    'Cyan': (0.0, 1.0, 1.0),
    'Magenta': (1.0, 0.0, 1.0),
    'Gold': (1.0, 0.84, 0.0),
    'Violet': (0.5, 0.0, 1.0),
    'Pink': (1.0, 0.71, 0.76),
    'Brown': (0.65, 0.16, 0.16),
    'Dark Green': (0.0, 0.5, 0.0),
    'Silver': (0.5, 0.5, 0.5),
    'Purple': (0.5, 0.0, 0.5),
    'Dark Purple': (0.29, 0.0, 0.51),
    'Choclate': (0.6, 0.4, 0.4),
    'Navy': (0.0, 0.0, 0.5)
}

class PDFUtility:
    def __init__(self, input_file, output_file):
        self.output_file = output_file
        self.color = (0,0,1)

        # Open the input PDF
        self.my_pdf = fitz.open(input_file)

        # intialize the empty book mark list
        self.bookmark_list =[]
    
    def add_bookmarks_from_text(self, search_string,color):

        self.color = color
        
        self.bookmark_list.append([1,search_string,-1,{'color':color}])

        # navigate through all the pages
        for n_page in self.my_pdf: 

            # search for will return the rects
            matchWordQuads = n_page.search_for(search_string)

            # Iterate on all the matches  
            for wordQuad in matchWordQuads: 
                
                # check to ignore white space rectangles
                if(wordQuad.height < 5 or wordQuad.width < 5):
                    continue

                # annotate the search strings
                annot = n_page.add_rect_annot(wordQuad)
                annot.set_border(width=0)
                annot.set_colors(stroke=self.color, fill=self.color)
                annot.set_opacity(0.3)
                annot.update() 

                # Get the coordinates of the rectangle
                x0, y0, x1, y1 = wordQuad

                # Calculate the center coordinates of the rectangle
                x_center = (x0 + x1) / 2
                y_center = (y0 + y1) / 2

                # off set to the visible screen position
                if n_page.rotation == 0:
                    x_center -= 50
                    y_center -= 50
                elif n_page.rotation == 90:
                    x_center += 50
                    y_center -= 50
                elif n_page.rotation == 180:
                    x_center += 50
                    y_center += 50
                elif n_page.rotation == 270:
                    x_center -= 50
                    y_center += 50
                    

                # corner cases
                if(x_center < 0):
                    x_center = 0
                if(y_center < 0):
                    y_center = 0

                # last param of the bookmark list.
                # pass the constructed point to this 
                dest ={
                    'kind': 1,
                    'page': n_page.number,
                    'to': Point(x_center,y_center),
                    'color': color
                }

                #add book marks
                self.bookmark_list.append([2,f"Page{n_page.number + 1}",n_page.number + 1,dest])
   

    def save_pdf_file(self):
        
         # toc_list = self.my_pdf.get_toc()
         # set the book mark list
        self.my_pdf.set_toc(self.bookmark_list)
        # print(self.bookmark_list)

        #remove the file if it exists
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

        self.my_pdf.save(self.output_file)
        print(f"Bookmarks added and Saved as '{self.output_file}'.")

       