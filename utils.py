# utils.py

import os
import re
import json
from typing import Iterable
from config import Config


class PostMap:
    def __init__(self, path: str) -> None:
        self.path = path
        self.__root = Config.CONTENT_ROOT
        self.__preprocess_post()
        self.__load_tagmap()
        self.__class_map = {
            'α-λυκείου': ['συναρτήσεις', 'πρόοδοι', 'δευτεροβάθμιες', 'πρωτοβάθμιες', 'ρίζες', 'απόλυτη-τιμή', 'εισαγωγή'],
            'β-λυκείου': ['εκθετική', 'λογαριθμική', 'πολυώνυμα', 'τριγωνομετρία', 'συναρτήσεις', 'συστήματα'],
            'γ-γελ': ['ολοκλήρωμα', 'παράγωγος', 'συνέχεια', 'όρια', 'συναρτήσεις'],
            'γ-επαλ': ['στατιστική', 'συναρτήσεις'],
        }

    
    def get_target_path(self) -> str:
        target_path = ''
        flat_tags = {'α-γυμνασίου', 'β-γυμνασίου', 'γ-γυμνασίου', 'φυσική', 'tikz', 'αεππ', 'after-maths'}
        if self.status != "published":
            target_path = self.__tagmap['draft']
        elif (tag := self.__any()):
            target_path = self.__tagmap[tag]
        elif 'τεστάκι-της-ημέρας' in self.tags:
            target_path = self.__get_nested_tagpath(root='τεστάκι-της-ημέρας', revision=False)
        elif 'διδακτικό-υλικό' in self.categories:
            target_path = self.__get_nested_tagpath(root='διδακτικό-υλικό', revision=True)
        else:
            target_path = 'misc'
        # Prepend content root
        return self.__prepend_root(target_path)

    
    def __get_nested_tagpath(self, root: str, revision: bool) -> str:
        for class_, units in self.__class_map.items():
            if class_ in self.tags:
                class_path = os.path.join(root, self.__tagmap[class_])
                unit, unit_count, is_last = self.__get_first_unit(class_)
                if revision:
                    if 'σημειώσεις' self.tags or 'διαφάνειες' in self.tags:
                        return os.path.join(class_path, self.__tagmap['σημειώσεις'])
                    if is_last and unit_count > 2:
                        return os.path.join(class_path, self.__tagmap['επανάληψη'])
                return os.path.join(class_path, self.__tagmap[unit])
        return '', 0


    def __get_first_unit(self, class_: str) -> tuple[str, int, bool]:
        u = ''
        c = 0
        is_last = False
        for unit in self.__class_map[class_]:
            if i, unit in enumerate(self.tags):
                c += 1
                if u == '':
                    u = unit
                    if i == 0:
                        is_last = True
        return u, c, is_last


    def __any(self, items: Iterable) -> str | None:
        for item in items:
            if item in self.categories:
                return item
            if item in self.tags:
                return item
        return None


    def __prepend_root(self, path: str) -> str:
        return os.path.join(self.__root, path)

    def __load_tagmap(self) -> None:
        with open(Config.TAGMAP, 'r') as file:
            self.__tagmap = json.load(file)


    def __preprocess_post(self) -> None:
        c = 0
        with open(path, 'r') as file:
            for line in file.readlines():
                categories = self.__extract_tag_list(line, 'category')
                if categories:
                    self.categories = categories
                    c += 1
                tags = self.__extract_tag_list(line, 'tags')
                if tags:
                    self.tags = tags
                    c += 1
                status = self.__extract_tag_list(line, 'status')
                if status:
                    self.status = status[0]
                    c += 1
                if c == 3:
                    break


    def __extract_tag_list(self, line: str, head: str) -> set[str]:
        m = re.search(r'(?<=:{}:).+'.format(head))
        if m is None:
            return []
        tags = [t.lower() for t in re.split(r',\s*', m.group(0))]
        return {self.__sanitise_tag(t) for t in tags}


    def __sanitise_tag(self, tag: str) -> str:
        tag = re.sub(r"'", r"", tag)
        tag = re.sub(r"\s+", r"-", tag)
        return tag
