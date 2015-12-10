import math
import os

from chameleon import PageTemplate

from accloud.finder.directoryRequestHandler import DirectoryRequestHandler


class TemplateHandler:
    def __init__(self):
        pass

    @staticmethod
    def loadCustomTemplate(request, directory_settings, template_str, fallbackoption):
        custom_template_path = None
        base_path = request.registry.settings['root_dir']
        relative_path = DirectoryRequestHandler.requestfolderpath(request)

        if 'directory_template_path' in directory_settings:
            dir_path = directory_settings['directory_template_path']
            if dir_path.startswith('projectlocal:'):
                dir_path = dir_path[len('projectlocal:'):]
                custom_template_path = os.path.join(base_path, dir_path)
            elif dir_path.startswith('folderlocal:'):
                dir_path = dir_path[len('folderlocal:')]
                custom_template_path = os.path.join(relative_path, dir_path)
            elif dir_path.startswith('absolute:'):
                dir_path = dir_path[len('absolute:'):]
                custom_template_path = dir_path

        # check if the custom_directory_template is valid
        if custom_template_path is not None and not os.path.exists(custom_template_path):
            custom_template_path = None
        if custom_template_path is None:
            custom_template_path = fallbackoption
        return custom_template_path


    @staticmethod
    def _apply_specific_templates(filenames, extension_specific):
        """
        Applies the specific templates which are set in the directory_settings to the list of files
        :param filenames:
        :param extension_specific:
        :return:
        """
        bootstrap_columns = 12
        elements_per_row = extension_specific['elements_per_row']
        column_width = int(math.ceil(bootstrap_columns / elements_per_row))

        specific_template = PageTemplate(extension_specific['template'])
        html = specific_template(grouped_files=filenames, columnwidth=column_width)
        return html

    def apply_templates(self, dict_items, directory_settings):
        # apply specific to the items
        for (filter_criteria, filenames) in dict_items.items():
            folder_template = None if 'folder_template' not in directory_settings else directory_settings[
                'folder_template']
            file_template = None if 'file_template' not in directory_settings else directory_settings['file_template']
            special_filetemplates = dict() if 'specific_filetemplates' not in directory_settings else \
            directory_settings['specific_filetemplates']

            if filter_criteria in special_filetemplates:
                extension_specific = special_filetemplates[filter_criteria]
                html = self._apply_specific_templates(filenames, extension_specific)
                dict_items[filter_criteria] = [html]
            else:
                template = None
                if filter_criteria != '' and not filter_criteria == '..' and file_template is not None:
                    template = PageTemplate(file_template)
                elif filter_criteria == '' and folder_template is not None:
                    template = PageTemplate(folder_template)
                if template is not None:
                    tmp = [template(item=file) for file in filenames]
                    dict_items[filter_criteria] = tmp
        return dict_items