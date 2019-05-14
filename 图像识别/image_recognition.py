# coding: utf-8

# In[2]:


image_folder = 'images/'
txt_folder = 'texts/'

from os import listdir, path

# =========end of user input=======
from aip import AipOcr

file_names = listdir(image_folder)

APP_ID = '11418112'
API_KEY = 'WkK6P0L6UCZk0sXVhz3VX45M'
SECRET_KEY = 'nim9GqYgEsTKlrL5NLqVmOD2GgmcEQQi'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


i = 0
for file_name in file_names:
    if file_name.endswith('JPG') or file_name.endswith('bmp') or file_name.endswith('png') or file_name.endswith('jpg'):
        try:
            image = get_file_content(path.join(image_folder, file_name))

            result = client.basicAccurate(image)

            word_results = result['words_result']
            texts = []
            for word_result in word_results:
                text = word_result['words']
                texts.append(text)

            file_base_name = path.splitext(file_name)[0]
            txt_file_name = file_base_name + '.txt'

            joined_text = '\n'.join(texts)

            with open(path.join(txt_folder, txt_file_name), 'w') as f:
                f.writelines(joined_text)
        except Exception as e:
            print('Failed to process image: {}, error: {}'.format(file_name, str(e)))
        finally:
            i += 1
            print('{} images processed'.format(str(i)))
