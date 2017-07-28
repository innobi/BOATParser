==========
BOATParser
==========

BOATParser (Business Objects AdminTools Parser) allows you to take the output of queries run in AdminTools and convert them into a pandas DataFrame. This facilitatates analysis of your metadata and also allows you to easily output that information into common sharable formats like csv and Excel.


Installation
------------

1. Clone the repository `git@github.com:WillAyd/BOATParser.git`

2. Build the source distribution and install via pip::

     python setup.py sdist
     pip install dist/BOATParser-0.1.tar.gz

3. Run any query in the AdminTools of your Business Objects environment. After the query completes, do a "Save As" on the page and be sure to save the page source locally.

4. Import the BOAdminToolsParser class and point it to your locally saved file::

     from BOATParser import BOAdminToolsParser

     bp = BOAdminToolsParser()
     df = bp.frame_from_file(<YOUR_HTML_FILE>)

5. Optionally, if your file contains folder path information (i.e. you included SI_KIND='Folder' in the WHERE clause of your query) use the `expand_paths` function to parse out an absolute directory listing::

     # Assuming df contains folder info, with SI_PATH and SI_NAME columns
     df['expanded_path'] = bp.expand_paths(df)


How it Works
------------

The output of any AdminTools query in Business Objects looks as follows:


.. raw:: html

	 <!--

	File Version Start - Do not remove this if you are modifying the file

	Build: 10.0.0

	File Version End



	(c) Business Objects 2003.  All rights reserved.

	    -->



	    <html>
	    
	    <head>

	    <link rel='stylesheet' type='text/css' name='stylelink' href="<CLIENT_URL>">

	    <title>Business Objects Business Intelligence platform - Query Builder</title>

	    <base target="_top">



	    </head>



	    <body bgcolor="#ffffff" text="#000000" link="#3300cc"  vlink="#660066" alink="#FF0000">

	    <a name="top-anchor"> </A>







	    <H2>Business Objects Business Intelligence platform - Query Builder</H2>

   <table class='basic' width='100%' border='0'>

   <tr>

   <td align='left'>Number of InfoObject(s) returned: <b>3</b></td>

   <td align='right'></td>

   </tr>

   </table>

   <HR SIZE='1'>

   

   <table class='basic' width='100%' border='0'><tr><td align='left'><b>1/3</b></td><td align='right'><a href='#top-anchor'>top</a></td></tr></table>	
   <table class='basic' width='100%' border='1' cellspacing='0'>
   <tr class='header'><td valign='top' colspan=2 width='15%' class='sectionHeader'>Properties</td></tr>
   <tr><td valign='top' width='15%'>SI_NAME</td><td valign='top'>baz</td></tr>
   <tr><td valign='top' width='15%'>SI_ID</td><td valign='top'>999999</td></tr>
   <tr><td valign='top' width='15%'>SI_CUID</td><td valign='top'>ACUID_FOR_BAZ</td></tr>
   <tr><td valign='top' width='15%'>SI_PATH</td><td valign='top'><table class='basic' width='100%' border='1' cellspacing='0'>
   <tr><td valign='top' width='15%'>SI_FOLDER_ID2</td><td valign='top'>888888</td></tr>
   <tr><td valign='top' width='15%'>SI_FOLDER_ID1</td><td valign='top'>777777</td></tr>
   <tr><td valign='top' width='15%'>SI_NUM_FOLDERS</td><td valign='top'>2</td></tr>
   <tr><td valign='top' width='15%'>SI_FOLDER_NAME1</td><td valign='top'>bar</td></tr>
   <tr><td valign='top' width='15%'>SI_FOLDER_OBTYPE2</td><td valign='top'>1</td></tr>
   <tr><td valign='top' width='15%'>SI_FOLDER_OBTYPE1</td><td valign='top'>1</td></tr>
   <tr><td valign='top' width='15%'>SI_FOLDER_NAME2</td><td valign='top'>foo</td></tr></table></td></tr></table><br><br><table class='basic' width='100%' border='0'><tr><td align='left'><b>2/3</b></td><td align='right'><a href='#top-anchor'>top</a></td></tr></table>
   <table class='basic' width='100%' border='1' cellspacing='0'>
   <tr class='header'><td valign='top' colspan=2 width='15%' class='sectionHeader'>Properties</td></tr>
   <tr><td valign='top' width='15%'>SI_NAME</td><td valign='top'>bar</td></tr>
   <tr><td valign='top' width='15%'>SI_ID</td><td valign='top'>888888</td></tr>
   <tr><td valign='top' width='15%'>SI_CUID</td><td valign='top'>ACUID_FOR_BAR</td></tr>
   <tr><td valign='top' width='15%'>SI_PATH</td><td valign='top'><table class='basic' width='100%' border='1' cellspacing='0'>
   <tr><td valign='top' width='15%'>SI_FOLDER_ID1</td><td valign='top'>777777</td></tr>
   <tr><td valign='top' width='15%'>SI_NUM_FOLDERS</td><td valign='top'>1</td></tr>
   <tr><td valign='top' width='15%'>SI_FOLDER_NAME1</td><td valign='top'>foo</td></tr>
   <tr><td valign='top' width='15%'>SI_FOLDER_OBTYPE1</td><td valign='top'>1</td></tr></table></td></tr></table><br><br><table class='basic' width='100%' border='0'><tr><td align='left'><b>3/3</b></td><td align='right'><a href='#top-anchor'>top</a></td></tr></table>
   <table class='basic' width='100%' border='1' cellspacing='0'>
   <tr class='header'><td valign='top' colspan=2 width='15%' class='sectionHeader'>Properties</td></tr>
   <tr><td valign='top' width='15%'>SI_NAME</td><td valign='top'>foo</td></tr>
   <tr><td valign='top' width='15%'>SI_ID</td><td valign='top'>777777</td></tr>
   <tr><td valign='top' width='15%'>SI_CUID</td><td valign='top'>ACUID_FOR_FOO</td></tr>
   <tr><td valign='top' width='15%'>SI_PATH</td><td valign='top'><table class='basic' width='100%' border='1' cellspacing='0'>
   <tr><td valign='top' width='15%'>SI_NUM_FOLDERS</td><td valign='top'>0</td></tr></table></td></tr></table><br><br>


The BOAdminToolsParser class contained within the BOATParser module uses BeautifulSoup to parse and focus just on table elements (this can greatly improve performance for large documents). Each table is converted into a dict entry, where the key is the first column and the value is the second. After parsing the entire file, the class converts the dict into a DataFrame, where each table parsed becomes its own record. The value in the first table column maps to the column name of the DataFrame, and the second column from the table becomes the value.

In cases where tables are nested (see SI_PATH in the test.html table provided) the BOAdminToolsParser class will parse recursively. The value for that given entry becomes a nested dict.

The BOAdminToolsParser class also provides a convenience function called `expand_paths`. Using the example above, after parsing it into a DataFrame you can call that function to get the full file path of a given record.

Bringing this altogether, here's are the steps for parsing the above table::

  from BOATParser import BOAdminToolsParser

  bp = BOAdminToolsParser()
  df = bp.frame_from_file('test.html')
  df['expanded_path'] = bp.expand_paths(df)

Yielding the following DataFrame:

.. raw:: html

	 <table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>SI_NAME</th>      <th>SI_ID</th>      <th>SI_CUID</th>      <th>SI_PATH</th>      <th>expanded_path</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>baz</td>      <td>999999</td>      <td>ACUID_FOR_BAZ</td>      <td>{'SI_FOLDER_ID2': '888888', 'SI_FOLDER_ID1': '...</td>      <td>foo/bar/baz</td>    </tr>    <tr>      <th>1</th>      <td>bar</td>      <td>888888</td>      <td>ACUID_FOR_BAR</td>      <td>{'SI_FOLDER_ID1': '777777', 'SI_NUM_FOLDERS': ...</td>      <td>foo/bar</td>    </tr>    <tr>      <th>2</th>      <td>foo</td>      <td>777777</td>      <td>ACUID_FOR_FOO</td>      <td>{'SI_NUM_FOLDERS': '0'}</td>      <td>foo</td>    </tr>  </tbody></table>
