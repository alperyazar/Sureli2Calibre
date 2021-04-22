# Sureli2Calibre
This is a small Python 2 script to add periodicals (magazines) to an existing [Calibre](https://calibre-ebook.com/) library automatically. **Sureli** (actually Süreli with Turkish letters) means periodical in Turkish.

I am trying to follow and read some e-magazines related with electronics mostly (over 30 at this moment). I am using Calibre to categorize e-magazines. Calibre is a great software. After I download a magazine (most of the time it is a PDF file), I add it to Calibre library and rename it according to my own convention. Then I wrote this script to automatate this process.

This script searches folders to find new issues of magazines, filters them and add them to a Calibre library. You don't need to modify script to support new magazines. All necessary settings are stored in configuration files and they are read from this script.

I used Python 2.7 on Windows 7 to test this script. It may not work with Python 3 or Python 2 on other operating systems. Also I am not a professional programmer. This script just works and it is far away from being perfect.

# How to use?

First, you should make sure that executables of Calibre software are in your path. To test this, just open a command line and type

    calibredb

If everything is fine you should see a blinking cursor, just press Ctrl-C to terminate it. If there is a problem, command window will say that it can't find this program. In that case you should Google it to find out how to add Calibre to your path.

On Windows, after you install Python 2 and add it to path, you should run the following command from the directory of `Sureli2Calibre.py`

    python Sureli2Calibre.py

You will encounter an error since there is no `Sureli2Calibre.ini` configuration file yet! Now, just go to **examples** directory and copy `Sureli2Calibre.ini` next to `Sureli2Calibre.py`. Then, open `.ini` file with a text editor like Notepad++. There are two settings: `sureli_path` and `calibre_path`. `sureli_path` should point to your e-magazine download directory actually. `calibre_path` should point to your Calibre library directory.

Each magazine (not each issue individually) has an ID number and a name according to my convention. Let's consider the example directory again. You see a **5LTJournal** folder. LTJournal (notice that no spacing here) is the name of the magazine and 5 is its ID number. You should use this convention in `sureli_path` folder like that (we will talk about files in a minute):

    sureli_path
	    1FunnyMagazine
		    1FunnyMagazine.ini
		    funnymagazine_issue45.pdf
		    ...
	    2BoringMagazine
		    2BoringMagazine.ini
		    Boring_vol45_num2.pdf
		    ...
	    ....
	    48JustAnotherMagazine
		    48JustAnotherMagazine.ini
		    67.zip
		    ...

`Sureli2Calibre.py` will parse folder names according to this convention: Bunch of numbers followed by letters. You should use an ID number only once.

In each `IDFolder`, `IDFolder.ini` file should exist, just analyze the given `5LTJournal` folder as an example. Now let's open `5LTJournal.ini` to understand it.

    [S2Csettings]
    filefilter = ^(.*\.pdf)$
    filefilterComment = Should end with .pdf
    fileformat = LT Journal of Analog Innovation, Volume $$$VOL$$$, Number $$$NUM$$$
    fileformatComment = LT Journal of Analog Innovation, Volume 26, Number 2
    VOL_RegExp = (?<=V)([0-9]+)(?=\N)
    VOL_RegExpComment = LTJournal_V20N1_Apr10.pdf
    NUM_RegExp = (?<=N)([0-9]+)
    NUM_RegExpComment = LTJournal_V20N1_Apr10.pdf
    author = Linear Technology

Each magazine should have a setting file. `Sureli2Calibre.py` uses setting files to parse magazine files. Each setting should start with `[S2CSsettings]` line. First, you should set up a filter to scan files related with magazine `filefilter` setting is used for this. For this example, this is a regular expression which accepts files ending with `.pdf`. The most important setting is `fileformat`. This is the name of the file that will appear on Calibre library. Notice that it looks little weird. What about `$$$` signs? Well, they are the dynamic areas, they are *placeholders*. For this particular magaizine, Linear Technology publishes each issue with a volume and number. After `Sureli2Calibre.py` adds an issue of LT Journal magazine, the resultant name will be like given in `fileformatComment`. `$$$VOL$$$` is replaced by volume and `$$$NUM$$$` is replaced by number. That is good, right? But how does `Sureli2Calibre.py` know volume and number for a particular issue. It knows by looking at file name.

In general, each publisher uses a name convention. They rarely change their conventions. Now just look at the `VOL_RegExpComment` or `NUM_RegExpComment` setting. This is the convention of Linear Technology for LT Journal magazine. This is the format of the file when you download it from their website. `Sureli2Calibre.py` uses regular expressions to extract information from filenames. `VOL_RegExp` setting defines a regular expression used to extract volume information. It takes first numbers between `V` and `N` characters in a file. Similarly the first number after `N` character denotes the number field in file name. Placeholders in fileformat settings are replaced with these extracted data and filename is constructed. The last author setting denotes the author of the magazine which is always a constant name.

There may be any number of placeholders in fileformat setting. Each placeholder should be in between triple dollar signs. For each placeholder you should add `PLACEHOLDER_RegExp` and `PLACEHOLDER_RegExpComment` line. Just look at the other example given in **examples** folder.

#Let's test it

Let's try to use `Sureli2Calibre.py` together and understand its operation.

We did copy `Sureli2Calibre.ini` next to `Sureli2Calibre.py` previously. To test the script I will create an empty Calibre library. I don't reccomend you test it on an existing library.

I opened Calibre. At that moment, its version is 2.69[64bit]. I created an empty test library at location

    C:\TestCalibre

I created another folder:

    C:\TestSureli

Now let's copy **1CircuitCellar** and **5LTJournal** from **examples** folder to under **TestSureli** folder. You may delete `Sureli2Calibre.ini` file under **examples** folder. Let's open `Sureli2Calibre.ini` file next to `Sureli2Calibre.py` and edit it:

    [Sureli2Calibre]
    sureli_path = C:\TestSureli
    calibre_path = C:\TestCalibre

Now lets run our script with `python Sureli2Calibre.py` command.

Here is my output:

    Sureli2Calibre beta1
    Main Config File: C:\Sureli2Calibre\Sureli2Calibre.ini
    Search folder:C:\TestSureli
    Calibre folder:C:\TestCalibre
    
    
    **********
    2 folders.
    **********
    
    
    Folders with wrong naming:
    Folders with no INI:
    Accepted folders
    [5] - 5LTJournal
    [27] - 27CircuitCellar
    
    
    
    Enter folder number:

As you can see, everyting is fine. We will use numbers between `[ ]` to navigate. Let's type `5` and press `Enter`. Here is my output:

    Listing all files
    C:\TestSureli\5LTJournal
    **********
    [1]: 5LTJournal.ini
            filefilter mismatched
    [2]: LTJournal-V24N1-2014-04.pdf
            Searching placeholders.
                    Entry Name: LT Journal of Analog Innovation, Volume 24, Number 1
     (5)
                    Author Name: Linear Technology
    No books matching the search expression: "LT Journal of Analog Innovation, Volum
    e 24, Number 1 (5)"
                    Unique?: Yes
    [3]: LTJournal_V20N1_Apr10.pdf
            Searching placeholders.
                    Entry Name: LT Journal of Analog Innovation, Volume 20, Number 1
     (5)
                    Author Name: Linear Technology
    No books matching the search expression: "LT Journal of Analog Innovation, Volum
    e 20, Number 1 (5)"
                    Unique?: Yes
    Enter file number:

What did script do? Well, there are 3 files (1 `.ini` and 2 `.pdf`) under **5LTJournal** folder. The script first tests a file name according to `filefilter` setting given in `.ini` file of the selected magazine. For this particular example, a valid filename should end with `.pdf`. For that reason `.ini` file wasn't accepted. `LTJournal-V24N1-2014-04.pdf` is OK however. It parsed this name and converted it to a valid name like `LT Journal of Analog Innovation, Volume 24, Number 1 (5)`. Then it searched the Calibre library to avoid duplicate. Since our Calibre library is empty now, it is new and a unique file. Now let's add first issue to our library. Type `2` then press `Enter` then open your Calibre and look at your new library. You should see an entry with `Title: LT Journal of Analog Innovation, Volume 24, Number 1 (5)` and `Author: Linear Technology`. Isn't that good?

Now let's open `C:\TestSureli\5LTJournal`. Now, we have a new folder: `_S2CMoved_`. `LTJournal-V24N1-2014-04.pdf` was moved here. If you are OK with your Calibre entry and everyting is fine, you may delete the added file to free up some disk space. Let's open `C:\Sureli2Calibre`. There is a new file with format `5_YYYY-MM-DD.txt`. This is a log file for the magazine with ID 5. Let's open this. Here is mine:

    2016-11-12 21:22:14,612	INFO:process_selected_folder():210	Starting to add C:\TestSureli\5LTJournal\LTJournal-V24N1-2014-04.pdf to C:\TestCalibre
    2016-11-12 21:22:14,615	INFO:process_selected_folder():215	EXE: calibredb add "C:\TestSureli\5LTJournal\LTJournal-V24N1-2014-04.pdf" --authors="Linear Technology" --title="LT Journal of Analog Innovation, Volume 24, Number 1 (5)" --library-path="C:\TestCalibre"
    2016-11-12 21:22:18,641	INFO:process_selected_folder():219	EXE Result: 0
    2016-11-12 21:22:18,641	INFO:process_selected_folder():225	Checking...
    2016-11-12 21:22:18,644	INFO:process_selected_folder():229	EXE: calibredb search """LT Journal of Analog Innovation, Volume 24, Number 1 (5)""" --library-path="C:\TestCalibre"
    2016-11-12 21:22:20,107	INFO:process_selected_folder():233	EXE Result: 0
    2016-11-12 21:22:20,108	INFO:process_selected_folder():238	File is added calibre db.
    2016-11-12 21:22:20,111	WARNING:process_selected_folder():245	C:\TestSureli\5LTJournal\_S2CMoved_ doesn't exist. Creating...
    2016-11-12 21:22:20,114	INFO:process_selected_folder():265	Moving from C:\TestSureli\5LTJournal\LTJournal-V24N1-2014-04.pdf to C:\TestSureli\5LTJournal\_S2CMoved_\LTJournal-V24N1-2014-04.pdf
    2016-11-12 21:22:20,115	INFO:process_selected_folder():272	Moved

`Sureli2Calibre.py` tries to log its actions in detail.

Now let's run our script again. If you select LTJournal `[5]` again, you will see a single available entry now. You can try to add Circuit Cellar to understand operation. Notice that the .pdf file under **27CircuitCellar** is a fake file due to copyrights. You may also analyze `27CircuitCellar.ini`. Different from LT Journal, Circuit Cellar uses a single issue number in `filreformat` setting.

You can expand magazines by creating corresponding `.ini` files. If you are having difficulties with regular expressions, you can use this excellent site to test your expressions: https://regex101.com/

# Questions or problems?
Please send me a message over https://www.ayazar.com/contact/ or create issue on https://github.com/alperyazar/Sureli2Calibre/issues

# Improvements?
That's great! The code is in bad condition actually. It works but... yeah. Just fork on Github: https://github.com/alperyazar/Sureli2Calibre

*C:16396*
*M:16456*
*Alper Yazar*
