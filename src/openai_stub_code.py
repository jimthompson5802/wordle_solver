from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {
      "role": "user",
      "content": "You are a virutal assistant that will help solve the Wordle puzzle. Solve the puzzle by guessing a five-letter word using these clues.\nWords must contain these letters in the following positions: 'a' in the first, 'e' in the fifth.\nWords must contain these letters with the position restrictions:  'l' should not be in the second position,  'a' should not be in the third position,  'e' should not be in the third position,  'e' should not be in the fourth position.\nWords that do not contain these letters:  'b',  'o',  'v',  'i',  'd',  'u',  'n',  'm',  'r',  'g'.\nSelect a word from the list that solves the puzzle or can be used to eliminate a large number of words. If more than one word meets the criteria, select the word that is more common. Provide step-by-step instructions for how you arrived at the selected word.\napple\nasyle\nattle"
    },
  ],
  temperature=0.16,
  max_tokens=4607,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)