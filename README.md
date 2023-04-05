Web scraper for collecting data from russian recruitment platform hh.ru.  

The parser collects data based on three parameters:  

      1) area (region of the country),
      2) number of pages to be opened,
      3) number of links to be analysed per page.  
      
The data is collected directly from API (see parser_api.py) into two dataframes:  

      1) all the vacancies (link, name, skills, description, wage and category),
      2) most frequent skills for each category  
      
The results are presented using streamlit (see app.py).
![image](https://user-images.githubusercontent.com/88784838/230091000-70998fc1-40c0-46be-868a-4607f3781e28.png)

