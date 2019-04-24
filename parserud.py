
# coding: utf-8

# In[1]:

import requests
from bs4 import BeautifulSoup
import lxml
import re
from jinja2 import Template
import argparse


# In[2]:

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing Udacity Course Fron Page')
    parser.add_argument('course_url', help='Udacity Course URL')
    args = parser.parse_args()

    url = args.course_url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    # Parsing

    link = '[{}]({})'.format(soup.find('h1', class_=re.compile('course--title')).string, url)

    title = soup.find('h1', class_=re.compile('course--title')).string

    ret = soup.find_all('h5')
    duration = ret[1].string
    skill = ret[2].contents[-1].string
    for x in ret:
        xs = x.string
        xc = x.contents
        if xs is not None:
            if 'day' in xs or 'month' in xs or 'week' in xs:
                duration = xs
        for y in xc:
            xs = y.string
            if xs is not None:
                if 'beginner' in xs or 'intermediate' in xs or 'advance' in xs:
                    skill = xs

    ret = soup.find('h3', class_=re.compile('instructor--name'))
    instructor = ret.string

    # ret = soup.find('div', class_=re.compile('summary-text'))
    # about = ret.find('p')
    about = soup.find('div', class_=re.compile('summary-text')).contents

    # prerequisite = soup.find('div', class_=re.compile('course-reqs--summary')).find('p')
    prerequisite = soup.find('div', class_=re.compile('course-reqs--summary')).contents

    # why = soup.find('ir-why-take-course').find(class_='ng-star-inserted').find('p')
    why = soup.find('ir-why-take-course').find(class_='ng-star-inserted').contents

    projects = "No"
    for x in why:
        if "project" in why:
            projects = "May Be"

    ret = soup.find_all('h2')
    heading = []
    for x in ret:
        heading.append(x.string)
    sz = len(heading)

    i = 0
    lesson = ""
    for x in soup.find_all('div', class_='syllabus--lower ng-star-inserted'):
        lesson += " - **Lesson " + str(i+1) + ": " + heading[i]+"**" + "\n"
        for name in x.find_all('li'):
            #lesson += "\t" + "- " + name.string + "\n"
            lesson += "{}{}{}{}{}".format('\t', ' ', '- ', name.string, '\n')
        i = i + 1
    # Parsing Complete

    # Sanitization
    pre = [str(x).replace('\n','') for x in prerequisite]
    prerequisite = pre
    # Sanitization Complete

    # Base File Content
    base = '# {{title}} {ignore = true}\n\n{{myname}}\n\n\n<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->\n<!-- code_chunk_output -->\n\n* [Basic Info](#basic-info)\n* [Lesson Details: What You Will Learn](#lesson-details-what-you-will-learn)\n* [Important Notes/Links:](#important-noteslinks)\n\n<!-- /code_chunk_output -->\n\n## Basic Info\n - **Link**: {{link}}\n - **Skill Level**: {{skill}}\n - **Duration**: {{duration}}\n - **Instructor**: {{instructor}}\n - **About**: {% for x in About %}{{x}}{% endfor %}\n - **Prerequisite**: {% for x in prerequisite %}{{x}}{% endfor %}\n - **Why Take This Course**: {% for x in why %}{{x}}{% endfor %}\n - **Projects**: {{projects}}\n - **Software Install**: {{install}}\n\n\n## Lesson Details: What You Will Learn\n{{what_you_will_learn}}\n\n\n<!-- Starting To Take Course Notes From Here -->\n\n## Important Notes/Links:\n'

    # Writing
    template = Template(base)

    final_print =  template.render(title = title, myname = 'Mehdi Rahman', link = link, skill=skill, duration=duration,                                    instructor=instructor, About = about,prerequisite= prerequisite,                                    why = why, projects = projects, what_you_will_learn = lesson)

    filename = '_init-{}-note.md'.format('_'.join(title.split(' ')))
    filename = filename.replace('/','')
    with open(filename, 'w') as outfile:
        outfile.write(final_print)
        #outfile.close()


# In[321]:




# In[ ]:




# In[359]:




# In[16]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[20]:




# In[ ]:




# In[ ]:
