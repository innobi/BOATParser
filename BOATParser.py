import pandas as pd
from lxml import etree

class BOAdminToolsParser():
    '''
    Class to help parse the HTML output provided by the AdminTools in Business
    Objects into a pandas DataFrame.

    For more information on how to use AdminTools, reference the following link:
    https://blogs.sap.com/2013/06/17/businessobjects-query-builder-basics/
    '''

    def _dict_from_table(self, table):
        '''
        Parameters:
        -----------
        table : BeautifulSoup tag; should be a table

        Returns:
        --------
        parsed_dict : representation of table object in dict form

        Converts an HTML table into a dict, with the first column mapping to
        the key and the second column mapping to the value. In cases where the
        second column contains an HTML table, this function will call itself
        recursively, providing a dict inside of a dict
        '''
        if table.tag != 'table': # Sanity check
            raise Exception

        parsed_dict = dict()
        for tr in table.xpath('tr'): # Get child tr elements
            if tr.get("class") == "header":
                continue  # Ignore header rows

            # Map first two columns to key / value
            key, val = tr.xpath('td[position()<=2]')
            
            # If the second column contains a table, call recursively
            subtable = val.xpath('table[1]')
            val_text = self._dict_from_table(subtable[0]) if subtable else val.text

            parsed_dict[key.text] = val_text

        return parsed_dict

    def expand_paths(self, fold_df):
        '''
        Parameters:
        -----------
        fold_df : DataFrame parsed from Business Objects containing folder
                information (SI_KIND='Folder'). Note that the 'SI_PATH' and
                'SI_NAME' need to be a part of the DataFrame, or else a KeyError
                will be raised

        Returns:
        --------
        fold_paths : Series of str representations of the absolute paths of
                each record in fold_df
        '''

        if not set(['SI_PATH', 'SI_NAME']).issubset(set(fold_df.columns)):
            raise KeyError('The expand_paths function requires a DataFrame '
                           'with SI_PATH and SI_NAME columns!!!')

        def _build_folder_path(rec):
            path_dict = rec['SI_PATH']
            nm = rec['SI_NAME']
            num_folders = int(path_dict['SI_NUM_FOLDERS'])
            fps = []
            # Walk backwards to build absolute folder paths
            for i in range(num_folders, 0, -1):
                key = 'SI_FOLDER_NAME{}'.format(i)
                fps.append(path_dict[key])

            # Add in name of current folder object
            fps.append(nm)

            # Add in blank entry at beginning, so join returns leading slash
            fps.insert(0, '')
            
            return '/'.join(fps)
        
        return fold_df.apply(_build_folder_path, axis=1)

    def frame_from_file(self, fn, **fopen_args):
        '''
        Parameters:
        -----------
        fn : filename to be parsed
        **fopen_args : keyword arguments to be passed to the open
                built-in function along with the filename

        Returns:
        --------
        df : pandas DataFrame object, representing the HTML content from fn
        '''

        # Speed up processing by only looking at tables, trs, tds
        parser = etree.HTMLParser()
        tree = etree.parse(fn, parser)

        # Every report is contained within a table with a border value of 1
        # Use xpath to find any without an ancestor (at top of document)
        tables = tree.xpath('//table[@border="1" and not(ancestor::table)]')

        parsed = dict()
        for index, table in enumerate(tables):
            parsed[index] = self._dict_from_table(table)

        df = pd.DataFrame.from_dict(parsed, orient='index')

        return df
