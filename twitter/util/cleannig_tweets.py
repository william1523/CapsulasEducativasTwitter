train_path = '../data/train_E6oV3lV.csv'
test_path = '../data/test_tweets_anuFYb8.csv'
train  = pd.read_csv(train_path)
test = pd.read_csv(test_path)

all_data = train.append(test, ignore_index=True, sort=True)
all_data['tidy_tweet'] = np.vectorize(remove_pattern)(all_data['tweet'], "@[\w]*")
all_data['tidy_tweet'] = rm_pun_num_esp_cha(all_data['tidy_tweet'])
all_data['tidy_tweet'] = rm_length_word(all_data['tidy_tweet'])
tokenized_tweet = tokenize(all_data['tidy_tweet'])

tokenized_tweet = stemmer(tokenized_tweet)
all_data['tidy_tweet'] = join_tokenize(tokenized_tweet)
all_data['hashtag'] = hashtag_extract(all_data['tidy_tweet'], flatten=False)
all_data['tidy_tweet'] = np.vectorize(remove_pattern)(all_data['tidy_tweet'], "#[\w]*")

all_data["Name Length"] = all_data['tidy_tweet'].str.len()
all_data.head()