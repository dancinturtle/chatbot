# Where am I so far?

## DNN
Given sentences that are tagged, we can train a neural net to identify to predict tags on sentences. If we know the tag, respond with one of many options appropriate to that tag.

Example: if the tag is hours, respond with answer about hours

What I like about this: I see potential here. We can tag the topic of conversation, such as eggs, dairy, nutrition, and then pull from appropriate responses.

Where I'm stuck: How can I use this to make novel sentences?

## Markov
Given sentences, show the probability that a pair of words will lead to another pair of words

What I like about this: This will create novel sentences!

Where I'm stuck: How can I make sure the sentences actually make sense? How do I make sure we're staying on topic?

## Cosine similarity
Pull text from the internet and fit transform it to count vetorizer. Then study the user input and check it for similarity with what we already have. Return with text is the most similar

What I like about this: I see the potential for how this can answer questions based off of the existing text on the website. I can also see how with some tweaking this can be used for grading a person's responses.

Where I'm stuck: How can I make novel sentences?

## Scraping
I figured out how to get past the login and I think I'm just going to pull down enough data about dairy so that I can get started. Maybe switch to Scrapy if I discover that I need something more powerful than Beautiful Soup.


## Let's think about what I want

```
  Bot: Hi! I'm the vegan chat bot! I'm interested in going vegan, but I have some questions. Could you help me?

  You: Sure

  Bot: Great! What's your name?

  You: Kermit

  Bot: Hi Kermit! You can call me Squid. If you ever would like to suggest a topic, like dairy, just type "Let's talk about dairy", and I'll ask a question about that if I can. My first question is, is it healthy to be on a vegan diet?

  You: It sure is.

  Bot: Sounds good, but can you tell me more? I heard that it's difficult to get protein. Where will I get my protein from?

  You: Beans, legumes, tofu.

  Bot: Are there any other things I should know about to remain healthy on a vegan diet?

  You: Take your b12 supplements!

  Bot: Anything else?

  You: No.

  Bot: Great, thank you! Next question, are oysters vegan?

  You: Let's talk about beef.

  Bot: Ok! I heard that free range beef is ethically fine. Is that true?


```

And after the user quits, we can present them with a feedback form.

```
  You chatted with the bot about nutrition.

  Positive points you brought up:  b12, tofu, beans, legumes

  Opportunities: Refer to a vegan dietician

  Overall sentimality: Your responses were 89% positive!

```

snowballpw