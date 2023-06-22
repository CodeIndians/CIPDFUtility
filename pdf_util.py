import fitz
from fitz import Point

class PDFUtility:
    def __init__(self, input_file, output_file,color):
        self.output_file = output_file
        self.color = color

        # Open the input PDF
        self.my_pdf = fitz.open(input_file)

        # intialize the empty book mark list
        self.bookmark_list =[]
    
    def add_bookmarks_from_text(self, search_string):
        
        self.bookmark_list.append([1,search_string,-1])

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
                }

                #add book marks
                self.bookmark_list.append([2,f"Page{n_page.number + 1}",n_page.number + 1,dest])
   

    def save_pdf_file(self):
        
         # toc_list = self.my_pdf.get_toc()
         # set the book mark list
        self.my_pdf.set_toc(self.bookmark_list)
        # print(self.bookmark_list)

        self.my_pdf.save(self.output_file)
        print(f"Bookmarks added and Saved as '{self.output_file}'.")

       