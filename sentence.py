def extract_first_three_sentences(paragraph):
    sentences = paragraph.split(".")
    first_three_sentences=""
    for s in sentences[:4]:
        if s.strip():
            first_three_sentences += s.strip()  
    return first_three_sentences


paragraph = """
 ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ View In Browser Automate your future refills with Autoship, Erin You may be running out of Liquid L-Carnitine CoQ10 (16 Ounces), and 3 other products that you ordered through Courtney Saye. Take an item off your future to-do list by adding these products to Autoship when you refill today. Add products, reschedule an order or cancel anytime! Schedule with Autoship View your order history Your products: Liquid L-Carnitine CoQ10 (16 Ounces)Dr's Advantage $36.99 $24.04Liquid L-Carnitine CoQ10 (16 Ounces)Dr's Advantage $36.99 $24.04 MegaMucosa - Berry Acai Flavored (150 Grams)Microbiome Labs $63.99 $41.59MegaMucosa - Berry Acai Flavored (150 Grams) Microbiome Labs$63.99 $41.59 Candid-X (90 capsules)BioMatrix $40.99 $26.64Candid-X (90 capsules) BioMatrix$40.99 $26.64 Prenatal Multi Powder, Vanilla (270 Grams)Needed $69.99 $45.49Prenatal Multi Powder, Vanilla (270 Grams) Needed$69.99 $45.49 Schedule with Autoship View your order history This email was sent to erinsalik@gmail.com by Fullscript, 360 Albert St, Ottawa, Ontario, Canada, K1R 7X7. If you no longer wish to receive these emails you may unsubscribe at any time. *Note, unsubscribes may take up to 2 days to process and do not include transactional messages and necessary communications from your practitioner.  
"""
first_three_sentences = extract_first_three_sentences(paragraph)
print(first_three_sentences)
