2021.8.12, 尝试编写能从wikipedia抽取信息python爬虫。
wikipedia不同标题数据爬取算法：
该算法需要预先判断下一索引值，来进行判断，并将字典数据层级关系体现出来，以边后面转换成json格式数据。
wikipedia标题主要分为3类：h2，h3和h4。
(1) 对于h4标题，h4+text：
如果后面跟h4标题，返回字典形式output_dict_4.update({key_4: value})；
如果后面跟h3标题，则将h4标题字典数据并入h3标题字典中，output_dict_4.update({key_4: value})，output_dict_3.update({key_3: output_dict_4})；
如果后面跟h2标题，则将h4标题字典数据并入h3标题字典中，再将h3标题字典并入h2标题字典中，output_dict_4.update({key_4: value})，output_dict_3.update({key_3: output_dict_4})，output_dict_2.update({key_2: output_dict_3})。
(2)对于h3标题，
(2-1)当h3与h4标题之间没有文本时，h3-text：
如果后面跟h4标题，continue
如果后面跟h3标题，将数据并入h3标题字典中，output_dict_3.update({key_3: value})
如果后面跟h2标题，将h3标题数据并入h2标题字典中，output_dict_3.update({key_3: value})，output_dict_2 = {key_2: output_dict_3}，cv_output.update(output_dict_2)
(2-2)当h3和h4标题之间有文本时，h3+text：
如果后面跟h4标题，需要先if判断key_3和value，将这段中间文本以“”为key保存到h4字典中，elif key_3 and value:output_dict_4.update({'': value})
如果后面跟h3标题，跟(2-1)无文本数据时操作一致。
如果后面跟h2标题，与(2-1)无文本数据时操作一致。
(3)对于h2标题，
(3-1)当h2与h3标题之间没有文本时，h2-text：
如果后面跟h3标题，continue
如果后面跟h2标题，将key_2与value保存入字典数据中，output_dict_2 = {key_2: value}，cv_output.update(output_dict_2)
(3-2)当h2与h3标题之间有文本时，h2+text：
如果后面跟h3标题，需要先if判断key_2和value，将这段中间文本以“”为key保存到h3标题字典中，elif key_2 and value:output_dict_3.update({'': value})
如果后面跟h2标题，与(3-1)操作一致。
(4)结尾判断，因为该算法要预先判断下一索引值，所以需要判断最后一位元素数据，if str(br_text_list[-1]).startswith('title')
如果最后以h4+/-text结尾，需要依次将数据保存成h4标题字典，然后并入h3标题字典，再并入h2标题字典，output_dict_4.update({key_4: value})，output_dict_3.update({key_3: output_dict_4})，output_dict_2.update({key_2: output_dict_3})
如果最后以h3+/-text结尾，需要将数据保存成h3标题字典，然后并入h2标题字典，output_dict_3.update({key_3: value})，
如果最后以h2+/-text结尾，需要将数据直接保存为h2字典，output_dict_2 = {key_2: value}
其中，关键在于判断最后一个是否为标题项，如果是，value="";如果不是，按照结尾步骤正常判断即可。
