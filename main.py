# This script is developed by https://github.com/CodeProcessor
import json

import requests
from bs4 import BeautifulSoup


class ProfSearch:

    def __init__(self):
        self.config = {}
        with open("config.json", "r") as fp:
            self.config = json.load(fp)

    def get_h_index(self, profile):
        r = requests.get(profile)
        soup = BeautifulSoup(r.content, 'lxml')
        table = soup.find('table', attrs={'id': 'gsc_rsb_st'})
        for row in table.findAll('tr'):
            row_text = [td.text for td in row.findAll('td')]
            if len(row_text) > 0 and row_text[0] == "h-index":
                return row_text[1]

    def main(self):
        starting_url = self.config["starting_url"]
        prof_list = []
        try:
            depth = 0
            no_of_profs = 0
            while True:
                depth += 1
                r = requests.get(starting_url)
                soup = BeautifulSoup(r.content, 'lxml')

                profs = soup.findAll('div', attrs={'class': 'gs_ai gs_scl gs_ai_chpr'})
                for prof in profs:
                    no_of_profs += 1
                    prof_name = prof.img['alt']
                    bs_interests = prof.findAll('a', attrs={'class': 'gs_ai_one_int'})
                    prof_profile = f"https://scholar.google.com{prof.a['href']}"
                    interests = []
                    for bs_interest in bs_interests:
                        interests.append(bs_interest.string.lower())

                    my_interests = self.config["my_interests"]
                    my_list = [my_interest.lower() in interests for my_interest in my_interests]
                    if any(my_list):
                        print(
                            f"prof {prof_name} Found with interest fields : {[val for ok, val in zip(my_list, my_interests) if ok]}")
                        h_index = self.get_h_index(prof_profile)
                        print(f"H-index: {h_index}")
                        prof_list.append(
                            {
                                "name": prof_name,
                                "interests": interests,
                                "h-index": h_index,
                                "profile": prof_profile
                            }
                        )

                try:
                    next = soup.find('button', attrs={'aria-label': 'Next'})
                    onclick = next.attrs["onclick"]
                    url_pos = onclick.split("/")[-1]
                    replaced_url = url_pos.replace("\\x26", "&").replace("\\x3d", "=")
                    full_url = f"https://scholar.google.com/{replaced_url}"

                    starting_url = full_url
                except (AttributeError, KeyError):
                    break

                print(f"Page {depth} total professors searched: {no_of_profs}")
                if depth > self.config["search_page_depth"]:
                    break
        except KeyboardInterrupt:
            pass

        print(f"     {'PROF NAME':<25} | {'h-index':<10} |Interests")
        with open(self.config["save_filename"], 'a') as fp:
            for i, p in enumerate(prof_list):
                print(
                    f"{i:2d} | {p['name']:<25} | {p['h-index']:<10} | {','.join(p['interests']):<50} | {p['profile']}")
                fp.write(
                    f"{i},{p['name']},{p['h-index']},{' | '.join(p['interests'])},{p['profile']}\n"
                )


if __name__ == '__main__':
    prof_object = ProfSearch()
    prof_object.main()
