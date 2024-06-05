

from googleapiclient.discovery import build
from urllib.parse import urlparse
from fuzzywuzzy import fuzz, process
import re

# API_KEY = 'AIzaSyCvspkLbBiktJNh_Sbl1zexGy85VFmeKSU'
# SEARCH_ENGINE_ID = '80c06cd1c357a45dc'



API_KEY='AIzaSyD1srgtKLebCTX8mwsh3jrfWG6WSnZnXps'
SEARCH_ENGINE_ID='d101fb0359f9d45d9'

def filter_links(links, vendor_name, item_name):
    vendor_links = []
    for link in links:
        link_domain = urlparse(link).netloc
        
        domain_ratio= fuzz.partial_ratio(vendor_name.lower(), link_domain.lower()) 
        match = re.search(r'https?://[^/]+(/.*)', link)
        if match:
            path = match.group(1)[1:] 
            cleaned_path = ' '.join(path.split('/'))
        item_ratio = fuzz.partial_ratio(item_name.lower(), cleaned_path.lower())
        ratio = (0.7 * domain_ratio) + (0.3 * item_ratio)
        print(f"link domain: {link_domain} \ndomain_ratio: {domain_ratio} \ncleaned_path: {cleaned_path} \nitem_ratio: {item_ratio}\n ratio: {ratio}")
        vendor_links.append((link, ratio))
    vendor_links.sort(key=lambda x: x[1], reverse=True)
    return vendor_links

# def google_search(query, num_results=5):
#     """
#     Performs a Google search for the given query and returns the first link. I'll give you item name, brand name and vendor name.
#     Return the link that'll take me to that particular item of that specific brand in the vendor website. 
#     For example, if item is 'shoes', brand is 'Nike' and vendor is 'Amazon', give me a link that'll take me to the Nike shoes page in Amazon.com
    
#     Args:
#         query (str): The search query.
#         num_results (int, optional): The number of results to return. Default is 5.
        
#     Returns:
#         list: A list of URLs for the search results.
#     """
#     service = build("customsearch", "v1", developerKey=API_KEY)
#     result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=num_results).execute()
    
#     links = []
#     if 'items' in result:
#         for item in result['items']:
#             links.append(item['link'])
    
#     return links


links1=['https://carnivorecrisps.com/products/carnivore-crisps-beef-ribeye', 'https://www.amazon.com/Carnivore-Crisps-proteins-carnivore-approved/dp/B09N1PKQ7N', 'https://carnivorecrisps.com/', 'https://www.ribeyerach.com/post/carnivore-crisps-vs-carnivore-snax-full-comparison']


links2=['https://carnivorecrisps.com/products/carnivore-crisps-beef-top-sirloin', 'https://www.amazon.com/Carnivore-Crisps-proteins-carnivore-approved/dp/B09N1PZ6D8', 'https://carnivorecrisps.com/', 'https://carnivorecrisps.com/collections/beef']


links3=['https://carnivorecrisps.com/products/carnivore-crisps-beef-eye-of-round', 'https://carnivorecrisps.com/collections/beef', 'https://www.facebook.com/ketoadapted/posts/i-love-carnivore-crisps-so-much-not-only-because-i-love-supporting-kind-small-bu/10159120699141446/', 'https://carnivorecrisps.com/collections/carnivore-crisps']


links4=['https://ketogenicwoman.com/how-to-make-carnivore-meat-chips/', 'https://carnivorecrisps.com/products/carnivore-crisps-pork-loin', 'https://thethingswellmake.com/meat-chips-carnivore-crisps-copycat/', 'https://carnivorecrisps.com/collections/other', 'https://www.amazon.com/Carnivore-Crisps-proteins-carnivore-approved/dp/B09N1QKXY8']


links5=['https://carnivorecrisps.com/products/carnivore-crisps-leg-of-lamb', 'https://carnivoresnax.com/products/leg-of-lamb', 'https://carnivorecrisps.com/collections/other', 'https://peopleschoicebeefjerky.com/blogs/news/carnivore-diet-snacks', 'https://carnivorecrisps.com/products/carnivore-crumbs-1-5-oz-lamb']


links6=['https://carnivorecrisps.com/products/carnivore-crisps-beef-heart', 'https://shop.carnivoreaurelius.com/', 'https://carnivorecrisps.com/collections/beef', 'https://www.reddit.com/r/carnivore/comments/ifqjug/beef_liver_crisps/', 'https://www.amazon.com/Carnivore-Crisps-proteins-Serving-Approved/dp/B0B3HJDCPV']


links7=['https://shop.carnivoreaurelius.com/', 'https://carnivorecrisps.com/products/carnivore-crisps-beef-liver', 'https://www.reddit.com/r/carnivore/comments/ifqjug/beef_liver_crisps/', 'https://www.amazon.com/Carnivore-Crisps-proteins-Serving-Approved/dp/B0B3HJDCPV', 'https://www.reddit.com/r/carnivore/comments/v9bqvl/carnivore_aurelius_beef_liver_crisps/']


links8=['https://carnivorecrisps.com/products/carnivore-crisps-chicken-breast', 'https://www.amazon.com/Carnivore-Crisps-Chicken-proteins-Approved/dp/B0BMYJHRXB', 'https://www.facebook.com/CarnivorousChef90/photos/a.360043466191340/451331123729240/?type=3', 'https://www.amazon.com/Carnivore-Crisps-Non-GMO-Gluten-Free-Protein/dp/B0C18NHWHP', 'https://hildaskitchenblog.com/recipe/chicken-chips-a-keto-chicken-thigh-recipe/']

q1 = f" buy Beef Ribeye from carnivorous crisps "
q2 = f" buy Beef Top Sirloin from carnivorous crisps"
q3 = f" buy Beef Eye of Round from carnivorous crisps"
q4 = f" buy  Pork Loin from carnivorous crisps"
q5 = f" buy  Leg of Lamb from carnivorous crisps"
q6 = f" buy Beef Heart from carnivorous crisps"
q7 = f" buy indigo Airfare from indigo"
q8 = f" buy Chicken Breast from carnivorous crisps"

vendor_name=' Carnivore Crisps'
item1='Beef Ribeye'
item2=' Beef Top Sirloin'
item3=' Beef Eye of Round'
item4=' Pork Loin'
item5='Leg of Lamb'
item6=' Beef Heart'
item7='Beef Liver'
item8='Chicken Breast'


# # links = google_search(q1)
# print(filter_links(links1,vendor_name, item1))
# print()
# print()
# # links = google_search(q2)
# print(filter_links(links2,vendor_name,item2))
# print()
# print()
# # links = google_search(q3)
# print(filter_links(links3,vendor_name,item3))
# print()
# print()
# # links = google_search(q4)
# print(filter_links(links4,vendor_name,item4))
# print()
# print()
# # links = google_search(q5)
# print(filter_links(links5,vendor_name,item5))
# print()
# print()
# # links = google_search(q6)
# print(filter_links(links6,vendor_name,item6))
print()
print()

# links = google_search(q7)
links= ['https://chouxpastrylove.wordpress.com/tag/vegetarian/page/2/', 'https://www.instagram.com/enokidelivery/p/C4A6Ii2I8Tz/', 'https://www.sandiegofood.net/2015/03/saiko-sushi.html', 'https://hittingthesauce.ca/2020/01/', 'https://hittingthesauce.ca/2018/02/', ]
print(filter_links(links,"Zomato","Make Your Own Poke Bowl"))
print()
print()
# print(filter_links(links8,vendor_name,item8))
print()
print()