import pandas as pd

from datetime import datetime

data = pd.read_csv('cse-368/ub_events.csv')

def find_event(query):
    results = []
    query = query.lower()
    
    for _, row in data.iterrows():
        event_name = row['Event Name'].lower()
        date_and_time = row['Date and Time'].lower()
        
        if query in event_name or query in date_and_time:
            event_info = f"Event: {row['Event Name']}\nDate & Time: {row['Date and Time']}\nURL: {row['URL']}\n"
            results.append(event_info)
    
    if not results:
        return "Sorry, no events found for your query."
    return "\n".join(results)

# Interactive chatbot
def chatbot():
    print("Welcome to the Event Finder Chatbot!")
    print("Ask me about events, like 'basketball' or 'October 22?'")
    
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = find_event(query)
        print("Bot:", response)


chatbot()