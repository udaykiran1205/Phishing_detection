# feature_extraction.py

import pandas as pd

selected_features = [
    'length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_qm', 'nb_eq', 'nb_slash',
    'nb_www', 'ratio_digits_url', 'ratio_digits_host', 'tld_in_subdomain', 'prefix_suffix',
    'shortest_word_host', 'longest_words_raw', 'longest_word_path', 'phish_hints',
    'nb_hyperlinks', 'ratio_intHyperlinks', 'empty_title', 'domain_in_title',
    'domain_age', 'google_index', 'page_rank'
]

def extract_features_from_url(url):
    try:
        hostname = url.split('//')[1].split('/')[0] if '//' in url else url
    except:
        hostname = url

    features = {
         'length_url': len(url),
        'length_hostname': len(url.split('//')[1].split('/')[0]) if '//' in url and len(url.split('//')) > 1 else len(url),  # Handle URLs without // or with only one element after split
        'ip': 1 if '//' in url and len(url.split('//')) > 1 and url.split('//')[1].split('/')[0].replace('.', '').isdigit() else 0,  # Handle URLs without // or with only one element after split
        'nb_dots': url.count('.'),
        'nb_qm': url.count('?'),
        'nb_eq': url.count('='),
        'nb_slash': url.count('/'),
        'nb_www': url.count('www'),
        'ratio_digits_url': sum(c.isdigit() for c in url) / len(url) if len(url) > 0 else 0,
        'ratio_digits_host': sum(c.isdigit() for c in url.split('//')[1].split('/')[0]) / len(url.split('//')[1].split('/')[0]) if '//' in url and len(url.split('//')) > 1 and len(url.split('//')[1].split('/')[0]) > 0 else 0,  # Handle URLs without // or with only one element after split
        'suspecious_tld': 0,  # Placeholder, adjust as needed.
    }

    # Convert to DataFrame and reorder columns
    input_df = pd.DataFrame([features])
    for feature in selected_features:
        if feature not in input_df.columns:
            input_df[feature] = 0
    input_df = input_df[selected_features]  # enforce column order
    return input_df
