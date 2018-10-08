# Brand Safety

### Setup project:

```
make setup
```

Install some requirements

### Prepare data:
#### Step 1

```
make gen_links
```

+ Search article links by 50 keywords for each label (accident or ordinary)
+ Get 10 news links on each keyword
+ --> 500 accident links + 500 ordinary links

#### Step 2

```
make scrape_pages
```

+ Crawl 1000 links and get content from that
+ For each content, extract nouns from them and save to txt data

#### Step 3

```
make gen_csv
```

+ Choose 3000 most common nouns on each label -> 6000 nouns
+ Make a csv file with 6000 nouns as field names, 1000 rows as 1000 pages
+ Each row contains frequencies of 6000 nouns on each page

### Train:

```
make train
```

+ Read the csv dataset from the previous stage
+ Create random forest classifier

### Predict the test set:

```
make predict_test_set
```

+ Apply the classifier and predict result on test set
+ Print out confusion matrix

### Predict a specific url:

```
make predict_specific_url url=your_url
```

+ Input url and get the result (is accident or not)