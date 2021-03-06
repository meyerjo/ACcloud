--- Unmaintained ---
# Fork purpose
The purpose of this branch is to enhance the web browser experience. Therefore, multiple extensions to the previous framework are made. 
Every result is wrapped within a bootstrap design with an navigation bar, which allows to leave the file preview more easily, and allows direct file access.

# How to manipulate the folder behaviour?
The user is able to add a .settings.json to every folder below the specified root_directory. These settings are propagated recursively to all the subfolders. They can be used to add a specific behaviour to certain filetypes.
Remove specific filetypes from the specific output and so on. An exemplaric .settings.json and a description can be found below

```
{

  "blacklist": ["\\.asv"],
  
  "folder_template": "<i class='fa fa-folder'></i><a tal:attributes='href item' tal:content='item'></a>",
  
  "file_template": "<i class='fa fa-file'></i><a tal:attributes='href item' tal:content='item'></a>",
  
  "specific_filetemplates": {
  
    ".png": {
    
      "group_by": ["^.{4}", "(grid|scalp)plot"],
      
      "elements_per_row": 2,
      
      "template": "<div tal:repeat='(group, rows) sorted(grouped_files.items())' metal:define-macro='filter_depth'><h1 tal:content='group'></h1><div tal:condition='python: type(rows) is dict' tal:define='grouped_files rows'><div  metal:use-macro='template.macros[\"filter_depth\"]'></div></div><div class='row' tal:condition='python: type(rows) is list' tal:repeat='files rows'><div tal:repeat='file files' class='col-sm-${columnwidth}'><div class='row-fluid'><div class='col-sm-12'>File: <span tal:content='file'></div><div class='col-sm-12'><img tal:attributes='src file' class='col-sm-12'></div></div></div></div></div>"
      
    },
    
    ".csv": {
    
      "group_by": ["^.{2}"],
      
      "elements_per_row": 2,
      
      "template": "<div tal:repeat='(group, rows) sorted(grouped_files.items())'><div class='row' tal:repeat='files rows'><div tal:repeat='file files' class='col-sm-${columnwidth}'><div class='row-fluid'><div class='col-sm-12'>File: <a tal:attributes='href file' tal:content='file'></a></div><div class='col-sm-12'><iframe tal:attributes='src file' class='col-sm-12'></iframe></div></div></div></div></div>"
      
    }
    
  }
  
}
```

## blacklist
The field blacklist, contains an array of regular expressions specifying filenames, which shouldn't be displayed in a directory listing.

## folder_template / file_template
The fields folder / file_template specify the template which should be used for regular files. **Usage of folder_template still under development.**

## specific_filetemplates
The field specific_filetemplates, contains a dictionary of behaviour rules for specific filetypes. In this example all png files are supposed to be grouped first, by the first 4 letters of their filename and then by their category as grid or scalpplot.
Furthermore it is specified that always 2 pictures should be displayed in one row. The last field is the template used to display the files.


# Authentication
It is possible to add an authentication layer to the server. If you wish so you can add --authentication = standard and --authenticationmodel = FileBased to the server call. The server expects a .users.yaml file in the root_dir.

**Note:**
The .users.yaml file doesn't get auto-generated at the moment. You can use the following snippet as a start and generate your own users later on.

Username: admin
Password: admin
```

admin:

  active: 'true'
  
  apikey: null
  
  password: 805d3d8280a360c310ddb42fe7f034be6a7781c1ed69de8a9b68e684280eafd0c16cba0f52c39b4657aeddd7244e76d137a47af559da35581aabe437180cf5a5
  
  roles:
  
  - g:admin
  
  salt: 'QEpO3ClIa3fN2jm3/m8BRw==

    '
    
  settings: {}
  
```



# Run server instance

Two options to run the server

python bin/Finder [options]

pserve [bin/production.ini, bin/development.ini] <-- recommended method





# TODO
## Done/Partial
* new directories have to be detected and the directory_settings from the parent folder should be used - Done
* Add a button which can be used to add an local .settings.json file which can later be edited - Done
* allow user to select plots over multiple folders in order to gnerate a report - partial
    * allow user to select a folder or a specific filetype in a directory and create a presentation - done
    * allow users to create a pdf report - partial
        * images can't be included at the moment
* allow to toggle entries - done
* download a folder as zip container - done
* download a specific subset as a zip container - done
* add a button/view to manipulate the .settings.json file - done
* filename specific preview option ==> change the identificator for filespecific templates to a regex string (i.e. README.md) - done
* user authentication - done
* disable specific keys in folder/presentation view - done / see below
    * assign ids to the specific key entries and add a widget to select/deselect them - done / see below
* allow user to add comments to a folder about content contained - done

## Open
* add favorite files, which can be displayed in other folders
* file-based preprocessing i.e. convert pptx files to another kind of documnet which can be visualized in a presentation
* add a inputbox to each row or use something like a feedback slider (e.g https://github.com/vedmack/feedback_me)
* store "presentations" in a specific format and make them editable
* fix the item selection bug
    * for some reason you have to click twice before the menu opens
    * the menu looses the information which items are saved
* store the item selection
* auto save the description fields, user-dependent
* search function on webpage
 
