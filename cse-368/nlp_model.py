
import spacy
import pandas as pd

# Load the trained model
nlp = spacy.load("event_and_bus_model")

# Load the event data (example, replace with your own data logic)
events_data = pd.read_csv('ub_events.csv')

# Function to process user query and return event information
def find_event(query):
    # Process the query with the trained model
    doc = nlp(query.lower())
    
    # Extract event-related entities (Event name, Date, Time, URL)
    event_name = None
    event_date = None
    event_url = None
    
    # Extract entities from the doc
    for ent in doc.ents:
        if ent.label_ == "Event Name":
            event_name = ent.text
        elif ent.label_ == "Date and Time":
            event_date = ent.text
        elif ent.label_ == "URL":
            event_url = ent.text

    if event_name and event_date and event_url:
        # Match with event data
        results = []
        for _, row in events_data.iterrows():
            if event_name.lower() in row['Event Name'].lower() and event_date.lower() in row['Date and Time'].lower():
                results.append(f"Event: {row['Event Name']}\nDate/Time: {row['Date and Time']}\nURL: {row['URL']}")
                
        if results:
            return "\n\n".join(results)
        else:
            return "Sorry, no matching events found."
    else:
        return "Sorry, no matching event found."

# Example usage:
query = "What are the events for October?"
print(find_event(query))
