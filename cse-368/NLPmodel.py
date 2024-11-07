import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")


data = pd.read_csv('cse-368/ub_events.csv')


def find_event(query):

    doc = nlp(query.lower())

    dates = [ent.text for ent in doc.ents if ent.label_ in ("DATE", "TIME")]
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    
    results = []
    for _, row in data.iterrows():
        event_name = row['Event Name'].lower()
        date_and_time = row['Date and Time'].lower()
        
        if any(keyword in event_name for keyword in keywords) or any(date in date_and_time for date in dates):
            event_info = f"Event: {row['Event Name']}\nDate & Time: {row['Date and Time']}\nURL: {row['URL']}\n"
            results.append(event_info)
    
    if not results:
        return "Sorry, no events found for your query."
    return "\n".join(results)

def chatbot():
    print("Welcome to the Event Finder Chatbot!")
    print("Ask me about events, like 'Tell me about basketball' or 'What events are on October 22?'")
    
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = find_event(query)
        print("Bot:", response)

# Run the chatbot
chatbot()