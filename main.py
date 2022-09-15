# This is a sample Python script.

import requests
from bs4 import BeautifulSoup

STOP_DEPTH = 1000
MY_INTERESTS = [
    "machine learning",
    "statistics",
    "artificial intelligence",
    "Data mining",
    "Information Retrieval",
    "Deep Learning",
    "Neural Networks",
    "computer vision",
    "pattern recognition"
]


def get_h_index(profile):
    r = requests.get(profile)
    # print(r.content)
    soup = BeautifulSoup(r.content, 'lxml')
    # print(soup.prettify())

    table = soup.find('table', attrs={'id': 'gsc_rsb_st'})
    # print(table.prettify())
    for row in table.findAll('tr'):
        # row_val = row.find('a').string
        # print(row)
        row_text = [td.text for td in row.findAll('td')]
        if len(row_text) > 0 and row_text[0] == "h-index":
            return row_text[1]


def main(starting_url):
    prof_list = []
    try:
        depth = 0
        no_of_profs = 0
        while True:
            depth += 1
            r = requests.get(starting_url)
            # print(r.content)
            soup = BeautifulSoup(r.content, 'lxml')
            # print("Encoding method :", soup.original_encoding)

            # print(soup.prettify())

            profs = soup.findAll('div', attrs={'class': 'gs_ai gs_scl gs_ai_chpr'})
            for prof in profs:
                no_of_profs += 1
                prof_name = prof.img['alt']
                bs_interests = prof.findAll('a', attrs={'class': 'gs_ai_one_int'})
                prof_profile = f"https://scholar.google.com{prof.a['href']}"
                interests = []
                for bs_interest in bs_interests:
                    interests.append(bs_interest.string.lower())

                my_list = [my_interest.lower() in interests for my_interest in MY_INTERESTS]
                if any(my_list):
                    print(
                        f"prof {prof_name} Found with interest fields : {[val for ok, val in zip(my_list, MY_INTERESTS) if ok]}")
                    h_index = get_h_index(prof_profile)
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
                # print(full_url)

                starting_url = full_url
                # print(json.dumps(prof_dict, indent=4))
                # break
            except (AttributeError, KeyError):
                break

            print(f"Page {depth} total professors searched: {no_of_profs}")
            if depth > STOP_DEPTH:
                break
    except KeyboardInterrupt:
        pass

    print(f"     {'PROF NAME':<25} | {'h-index':<10} |Interests")
    with open("results.txt", 'a') as fp:
        for i, p in enumerate(prof_list):
            print(f"{i:2d} | {p['name']:<25} | {p['h-index']:<10} | {','.join(p['interests']):<50} | {p['profile']}")
            fp.write(
                f"{i},{p['name']},{p['h-index']},{' | '.join(p['interests'])},{p['profile']}\n"
            )


if __name__ == '__main__':
    uni_of_mel = "https://scholar.google.com/citations?view_op=view_org&hl=en&org=10194437184893062620"
    # main_url = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=university+of+melbourn&btnG="
    # # main_url = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=Computer+Science%2C+University+of+Melbourne&btnG="
    # # URL = "https://scholar.google.com/citations?view_op=search_authors&hl=en&oe=ASCII&mauthors=university+of+melbourn&after_author=ZTrkAK62_v8J&astart=10"

    main(uni_of_mel)
    # h_index = get_h_index("https://scholar.google.com/citations?hl=en&user=Vt5edEkAAAAJ")
    # print(h_index)
.0
32