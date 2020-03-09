'''
                                         ########## NOTES ###########

    # For the taglines of the movies, I fetch them using IMDbpy however there are no taglines I guess..
    #
    # Since the directories of the given tag files may vary from computer to another I didn't risk it by fetching
    # throughout seted path. Thats why th taglines are empty almost all of the movies.
    #
    # As for the GUI side of the project, it is not perfectly same as in the given pictures but I believe that the
    # consept is well defined.
    #
    # The reccomendation file is not implemented in the code it is imported from the same directory.
    #
    # At the first step of the program after pressing the 'Upload Ratings' button there are two different dictionaries
    # are being created and one of them has the movieId's as the key. Since there are loads of movies the process takes
    # some time so there is nothing wrong just the process time.
    #
    #
    #Written and Developed by Veysi Furkan Bisen.
'''

from Tkinter import *
import csv
import tkFileDialog
from imdb import IMDb
from recommendations import *

class movie_engine(Frame):
    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.grid()
        self.parent = parent
        self.initUI()


    def initUI(self):

        # ---Title---
        self.title_label = Label(self, text="Movie Reccomendation Engine", font="Arial 10 bold")
        self.title_label.grid(row=0, column=0, columnspan=8, sticky="NEW", padx=200, pady=25)

        # ---First Column---
        # Engine
        self.engine_selection = StringVar()

        self.engine_label = Label(self, text='Engine', font="Arial 10 bold")
        self.engine_label.grid(row=1, column=0, columnspan=2, padx=25)

        self.erbv = IntVar()
        self.movie_based_rb = Radiobutton(self, state = DISABLED, text="Movie Based", variable=self.erbv, value=1,
                                          bg="gray", command=self.movie_radio)
        self.movie_based_rb.grid(row=2, column=0, columnspan=2, padx=25, pady=10, sticky="NSEW")

        self.user_based_rb = Radiobutton(self, state = DISABLED, text="User Based", variable=self.erbv, value=2,
                                         bg="gray", command=self.user_radio)
        self.user_based_rb.grid(row=3, column=0, columnspan=2, padx=25, pady=10, sticky="NSEW")

        # Similarity Metric
        self.similarity_selection = StringVar()

        self.sim_met_label = Label(self, text="Similarity Metric", font="Arial 10 bold")
        self.sim_met_label.grid(row=4, column=0, columnspan=2, padx=25)

        self.smrbv = IntVar()
        self.pearson_rb = Radiobutton(self, state = DISABLED, text="Pearson", variable=self.smrbv, value=1, bg="gray",
                                      command=self.pearson_radio)
        self.pearson_rb.grid(row=5, column=0, columnspan=2, padx=25, pady=10, sticky="NSEW")

        self.euclidean_rb = Radiobutton(self, state = DISABLED, text="Euclidean", variable=self.smrbv, value=2,
                                        bg="gray", command=self.euclidean_radio)
        self.euclidean_rb.grid(row=6, column=0, columnspan=2, padx=25, pady=10, sticky="NSEW")

        # Rating Button
        self.raitng_up = Button(self, text="Upload Ratings", bd=5, font="Arial 10 bold", command=self.upload_ratings)
        self.raitng_up.grid(row=7, column=0, columnspan=2, padx=25, pady=10, sticky="NSEW")

        # Movies Button
        self.raitng_up = Button(self, text="Upload Movies", bd=5, font="Arial 10 bold", command=self.upload_movies)
        self.raitng_up.grid(row=8, column=0, columnspan=2, padx=25, pady=10, sticky="NSEW")

        # Links Button
        self.raitng_up = Button(self, text="Upload Links", bd=5, font="Arial 10 bold", command=self.upload_links)
        self.raitng_up.grid(row=9, column=0, columnspan=2, padx=25, pady=10, sticky="NSEW")

        # ---Second Column---
        self.movie_user_label = Label(self, text="Movie / User", font="Arial 10 bold")
        self.movie_user_label.grid(row=1, column=2, columnspan=2, padx=25)

        self.movie_user_listbox = Listbox(self)
        self.movie_user_listbox.grid(row=2, column=2, columnspan=2, rowspan=10, padx=25, pady=10, sticky="NSEW")

        self.first_listbox_scroll = Scrollbar(self)
        self.first_listbox_scroll.config(command=self.movie_user_listbox.yview)
        self.movie_user_listbox.config(yscrollcommand=self.first_listbox_scroll.set)
        self.first_listbox_scroll.grid(row=2, column=2, columnspan=2, rowspan=10, sticky="NSE", padx=25, pady=10)

        self.movie_user_listbox.bind('<<ListboxSelect>>', self.entry_onselect)

        # ---Third Column---
        self.recommended_movie_label = Label(self, text="Recommended Movie", font="Arial 10 bold")
        self.recommended_movie_label.grid(row=1, column=4, columnspan=3, padx=25)

        self.recommended_movie_listbox = Listbox(self, width=30)
        self.recommended_movie_listbox.grid(row=2, column=4, columnspan=3, rowspan=10, padx=25, pady=10, sticky="NSEW")

        self.second_listbox_scroll = Scrollbar(self, orient=HORIZONTAL)
        self.second_listbox_scroll.config(command=self.recommended_movie_listbox.xview)
        self.recommended_movie_listbox.config(xscrollcommand=self.second_listbox_scroll.set)
        self.second_listbox_scroll.grid(row=11, column=4, columnspan=3, padx=25, pady=10, sticky="NSEW")

        self.recommended_movie_listbox.bind('<<ListboxSelect>>', self.recommended_onselect)

        # ---Fourth Column---
        self.info_list = ["Director: ", "Stars: ", "Rating: ", "Genre: ", "Plot: ", ":Taglines: ", "Trailer(Link)"]

        self.information_label = Label(self, text="Information", font="Arial 10 bold")
        self.information_label.grid(row=1, column=7, columnspan=2, padx=25)

        self.information_box = Text(self, width=20, bg='gainsboro', relief=FLAT, selectborderwidth=2, wrap=WORD)
        self.information_box.grid(row=2, column=7, columnspan=2, rowspan=10, padx=25, pady=10, sticky="NSEW")

        self.textbox_scroll = Scrollbar(self)
        self.textbox_scroll.config(command=self.information_box.yview)
        self.information_box.config(yscrollcommand=self.textbox_scroll.set)
        self.textbox_scroll.grid(row=2, column=7, columnspan=2, rowspan=10, sticky='NSE', padx=25, pady=10)

        for item in self.info_list:
            self.information_box.insert(END, item + '\n\n')

        self.information_box.config(state=DISABLED)

    def upload_ratings(self):

        self.rating_dict = dict()
        self.rating_dict_2 = dict()

        file_path = tkFileDialog.askopenfilename()
        #splash = Splash(root)
        with open(file_path, mode='r') as infile:
            reader = csv.reader(infile)
            for i in reader:
                self.rating_dict.setdefault(i[0], {})
                self.rating_dict_2.setdefault(i[1], {})
                if "userId" in self.rating_dict.keys():
                    self.rating_dict.pop("userId")
                if 'movieId' in self.rating_dict_2.keys():
                    self.rating_dict_2.pop('movieId')
                if i[0] in self.rating_dict.keys():
                    self.rating_dict[i[0]][i[1]] = float(i[2])
                if i[1] in self.rating_dict_2.keys():
                    self.rating_dict_2[i[1]][i[0]] = float(i[2])
        #self.after(5000, splash.destroy)

    def upload_movies(self):
        self.movie_dict = dict()

        file_path = tkFileDialog.askopenfilename()
        with open(file_path, mode='r') as infile:
            reader = csv.reader(infile)
            for i in reader:
                self.movie_dict.setdefault(i[0], {})
                if "movieId" in self.movie_dict.keys():
                    self.movie_dict.pop("movieId")
                if i[0] in self.movie_dict.keys():
                    self.movie_dict[i[0]].setdefault("genre", i[2])
                    self.movie_dict[i[0]].setdefault("moviename", i[1])

    def upload_links(self):
        self.link_dict = dict()

        file_path = tkFileDialog.askopenfilename()
        with open(file_path, mode='r') as infile:
            reader = csv.reader(infile)
            for i in reader:
                self.link_dict.setdefault(i[0], [])
                if "movieId" in self.link_dict.keys():
                    self.link_dict.pop("movieId")
                if i[0] in self.link_dict.keys():
                    self.link_dict[i[0]].append(i[1:])

        self.printing_to_listbox()

    def printing_to_listbox(self):
        self.user_based_rb.config(state=NORMAL, bg="gray")
        self.movie_based_rb.config(state=NORMAL, bg="gray")

        self.pearson_rb.config(state=NORMAL, bg="gray")
        self.euclidean_rb.config(state=NORMAL, bg="gray")

        self.user_based_rb.select()
        self.pearson_rb.select()

        self.similarity_selection = "pearson"

        self.user_radio()

    def user_radio(self):
        self.engine_selection = "users"
        self.movie_user_listbox.delete(0, END)

        self.movie_user_label['text'] = "Users"

        userId_list = []
        for item in self.rating_dict:
            userId_list.append(int(item))
            userId_list.sort()

        for i in userId_list:
            self.movie_user_listbox.insert(END, i)

    def movie_radio(self):
        self.engine_selection = "movies"
        self.movie_user_listbox.delete(0, END)

        self.movie_user_label['text'] = "Movies"

        movieId_list = []
        for item in self.movie_dict:
            movieId_list.append(int(item))
            movieId_list.sort()

        for i in movieId_list:
            self.movie_user_listbox.insert(END, i)

    def pearson_radio(self):
        self.similarity_selection = ""
        self.similarity_selection = "pearson"

    def euclidean_radio(self):
        self.similarity_selection = ""
        self.similarity_selection = "distance"

    def entry_onselect(self, event):

        w = event.widget
        idx = w.curselection()[0]
        value = str(w.get(idx))

        self.recommended_movie_listbox.delete(0,END)
        self.printing_list = []

        if self.similarity_selection == "pearson":
            if self.engine_selection == "users":
                self.recom_result = getRecommendations(self.rating_dict, value, similarity=sim_pearson)

                counter = 0
                while counter <= 5:
                    self.printing_list.append(self.recom_result[counter][1])
                    counter += 1

            if self.engine_selection == "movies":
                self.recom_result = topMatches(self.rating_dict_2, value, 10, similarity=sim_pearson)

                counter = 0
                while counter <= 5:
                    self.printing_list.append(self.recom_result[counter][1])
                    counter += 1


        if self.similarity_selection == "distance":
            if self.engine_selection == "users":
                self.recom_result = getRecommendations(self.rating_dict, value, similarity=sim_distance)

                counter = 0
                while counter <= 5:
                    self.printing_list.append(self.recom_result[counter][1])
                    counter += 1

            if self.engine_selection == "movies":
                self.recom_result = topMatches(self.rating_dict_2, value, 10, similarity=sim_distance)

                counter = 0
                while counter <= 5:
                    self.printing_list.append(self.recom_result[counter][1])
                    counter += 1

        self.movie_id_list = []
        self.movie_name_list = []
        for item in self.printing_list:
            if item in self.movie_dict:
                self.movie_id_list.append(item)
                self.movie_name_list.append(self.movie_dict[item]['moviename'])
                self.recommended_movie_listbox.insert(END, self.movie_dict[item]['moviename'])

    def recommended_onselect(self, event):
        self.movie_info_list = ['director']

        w = event.widget
        idx = w.curselection()[0]
        value = str(w.get(idx))

        movie_id = self.movie_name_list.index(value)
        movie_link = self.link_dict[self.movie_id_list[movie_id]][0][0]

        ia = IMDb()
        movie = ia.get_movie(movie_link)

        detailed_info = []
        Directors = []

        for director in movie['directors']:
            Directors.append(director['name'])

        Cast = []
        for star in movie['cast']:
            Cast.append(star['name'])

        Genres = []
        for genre in movie['genres']:
            Genres.append(genre)

        Tag = []
        if movie.get('tagline') != None:
            for tag in movie.get('tagline'):
                Tag.append(tag)
        else: Tag.append("")

        detailed_info.append(','.join(Directors))
        detailed_info.append(','.join(Cast))
        detailed_info.append(str(movie.get('rating')))
        detailed_info.append(','.join(Genres))
        detailed_info.append(movie['plot'][0])
        detailed_info.append(','.join(Tag))
        detailed_info.append("")

        self.information_box.config(state=NORMAL)
        self.information_box.delete("1.0", "end")
        self.information_box.config(width = 35)
        self.information_box.config(state=DISABLED)

        i=0
        while i<=len(self.info_list)-1:
            self.information_box.config(state=NORMAL)
            self.information_box.insert(END, self.info_list[i] + detailed_info[i] + '\n\n')
            self.information_box.config(state=DISABLED)
            i+=1

class Splash(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        Label(self, text="Show Image here").grid()
        self.overrideredirect(1)
        self.initUI()

    def initUI(self):
        self.label = Label(self, text="Please wait while proceeding...", font="Arial 24 bold")
        self.label.grid(row=0, column=0, columnspan=8, sticky="NEW", padx=200, pady=25)


root = Tk()
root.title("Movie Reccomendation Engine")
app = movie_engine(root)
app.pack(fill=BOTH, expand=True)
root.mainloop()