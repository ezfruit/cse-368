import pandas as pd
import spacy
from spacy.training.example import Example
import random
from sklearn.model_selection import train_test_split
new_events_data = pd.read_csv('csv_files/ub_events.csv')
new_campus_living_data = pd.read_csv('csv_files/campus_living_info.csv')
new_school_data = pd.read_csv('csv_files/ub_campus.csv')

events_data = new_events_data[new_events_data['Event Name'].notna()]
campus_living_data = new_campus_living_data[new_campus_living_data['Link Text'].notna()]
school_data = new_school_data[new_school_data['School/College Name'].notna()]
def create_training_data_from_combined_data(events_data, campus_living_data, school_data):
    training_data = []

    for _, row in events_data.iterrows():
        event_name = row['Event Name']
        date_and_time = row['Date and Time']
        url = row['URL']

        questions = [
            f"What is the URL for {event_name}?",
            f"When is {event_name} happening?",
            f"Where is {event_name} located?",
            f"What time is {event_name}?",
            f"What is the schedule for {event_name}?"
        ]

        for question in questions:
            entities = []
            start_event_name = question.find(event_name)
            if start_event_name != -1:
                end_event_name = start_event_name + len(event_name)
                entities.append((start_event_name, end_event_name, "EVENT_NAME"))

            if "URL" in question and url:
                start_url = question.find("URL")
                end_url = start_url + len("URL")
                entities.append((start_url, end_url, "URL"))

            if date_and_time in question:
                start_date = question.find(date_and_time)
                end_date = start_date + len(date_and_time)
                entities.append((start_date, end_date, "DATE_TIME"))

            training_data.append((question, {"entities": entities}))

    for _, row in campus_living_data.iterrows():
        link_text = row['Link Text']
        url = row['URL']

        if link_text:
            questions = [
                f"What is the URL for {link_text}?",
                f"Where can I find {link_text}?"
            ]

            for question in questions:
                entities = []

                start_link_text = question.find(link_text)
                if start_link_text != -1:
                    end_link_text = start_link_text + len(link_text)
                    entities.append((start_link_text, end_link_text, "RESOURCE_NAME"))

                if "URL" in question and url:
                    start_url = question.find("URL")
                    if start_url != -1:
                        end_url = start_url + len("URL")
                        entities.append((start_url, end_url, "URL"))

                training_data.append((question, {"entities": entities}))


    for _, row in school_data.iterrows():
        school_name = row['School/College Name']
        website = row['Key Website']
        departments = row['Departments/Programs Available']

        questions = [
            f"What is the website for {school_name}?",
            f"Where can I find information about {school_name}?",
            f"Tell me about {school_name}.",
            f"What programs are available at {school_name}?",
            f"Which departments are available at {school_name}?"
        ]

        for question in questions:
            entities = []
            start_school_name = question.find(school_name)
            if start_school_name != -1:
                end_school_name = start_school_name + len(school_name)
                entities.append((start_school_name, end_school_name, "SCHOOL_NAME"))
            if website:
                start_url = question.find("website")
                if start_url != -1:
                    entities.append((start_url, start_url + len("website"), "URL"))
            if departments:
                start_dept = question.find(departments)
                if start_dept != -1:
                    end_dept = start_dept + len(departments)
                    entities.append((start_dept, end_dept, "DEPARTMENT"))

            training_data.append((question, {"entities": entities}))

    return training_data

training_data = create_training_data_from_combined_data(events_data, campus_living_data, school_data)


random.shuffle(training_data)

train_data, val_data = train_test_split(training_data, test_size=0.2, random_state=42)


nlp = spacy.load("UB_chatbot")
# if "ner" not in nlp.pipe_names:
#     ner = nlp.create_pipe("ner")
#     nlp.add_pipe("ner", last=True)
# else:
#     ner = nlp.get_pipe("ner")


# for label in ["EVENT_NAME", "DATE_TIME", "URL", "RESOURCE_NAME","SCHOOL_NAME"]:
#     ner.add_label(label)

# optimizer = nlp.begin_training()
# # optimizer.learn_rate = 0.001
# # nlp.batch_size = 32
# for epoch in range(50):
#     random.shuffle(train_data)
#     losses = {}
#     epoch_loss = 0.0
#     for text, annotations in train_data:
#         doc = nlp.make_doc(text)
#         example = Example.from_dict(doc, annotations)
#         nlp.update([example], drop=0.5, losses=losses)
#         epoch_loss += losses.get('ner', 0)

#     val_loss = 0.0
#     for text, annotations in val_data:
#         doc = nlp.make_doc(text)
#         example = Example.from_dict(doc, annotations)
#         val_loss += nlp.evaluate([example])['ents_p']

#     print(f"Epoch {epoch + 1} completed. Loss: {epoch_loss}. Validation loss: {val_loss}")


# nlp.to_disk("UB_chatbot")

# nlp = spacy.load("en_core_web_sm")

events_data.columns = events_data.columns.str.strip()
campus_living_data.columns = campus_living_data.columns.str.strip()

def answer_query(query, events_data, campus_living_data, school_data):

    doc = nlp(query)

    entities = {ent.label_: ent.text for ent in doc.ents}
    
    print(f"Extracted Entities: {entities}")

    campus_names = {
        "North Campus": "UB’s North Campus, located just outside the city in Amherst, N.Y., is where most of the university’s core academic programs are offered. Opened in the early 1970s, it is the largest of our three campuses, encompassing cutting-edge academic and research spaces, student residence halls and apartments, award-winning dining facilities, the Student Union and athletic venues. Abundant green spaces, including a recreational lake and a 65-acre living woods, complement the built environment.",
        "South Campus": "UB’s South Campus is a Western New York landmark dating back to the 1920s. Situated in a leafy residential neighborhood in North Buffalo, the 153-acre parcel is home to classic ivy-covered buildings and grassy, tree-filled quads along with high-rise residence halls and innovative research and teaching facilities. The schools of Architecture and Planning, Dental Medicine, Nursing, Pharmacy and Pharmaceutical Sciences, and Public Health and Health Professions are all located here.",
        "Downtown Campus": "The pillar of our Downtown Campus is the Jacobs School of Medicine and Biomedical Sciences, which moved there in 2017 following construction of a state-of-the-art building at Main and High streets. Most of our other Downtown Campus entities—including the New York State Center of Excellence in Bioinformatics and Life Sciences, the Clinical and Research Institute on Addictions, and the Clinical and Translational Research Center—are located near the Jacobs School in Buffalo’s medical corridor, a quickly growing hub of clinical care, research and education."
    }

    campus_features = {
        "North Campus": "UB boasts unique features such as the 60-acre lake in the middle of campus and Greiner Hall, the first residence hall in the country built in accordance with the principles of Universal Design.",
        "South Campus": "The Abbott Library reading room houses custom woodwork from a company that helped furnish the White House. The Apothecary Museum contains historical artifacts like medicinal whiskey and asthma cigarettes.",
        "Downtown Campus": "The Jacobs School of Medicine's seven-story atrium features over 19,000 feet of glass. Additionally, research projects supported by the Center for Computational Research include smart bandages and fairer NFL schedules."
    }
    if "campus" in query.lower():
        if "north" in query.lower():
            return f"Here’s some information about North Campus: {campus_names['North Campus']}"
        elif "south" in query.lower():
            return f"Here’s some information about South Campus: {campus_names['South Campus']}"
        elif "downtown" in query.lower():
            return f"Here’s some information about Downtown Campus: {campus_names['Downtown Campus']}"

    if "features" in query.lower():
        if "north" in query.lower():
            return f"North Campus has the following special features: {campus_features['North Campus']}"
        elif "south" in query.lower():
            return f"South Campus features include: {campus_features['South Campus']}"
        elif "downtown" in query.lower():
            return f"Downtown Campus has unique features such as: {campus_features['Downtown Campus']}"

    if "archives" in query.lower():
        return "UB’s archives contain early manifestos of punk and original Lone Ranger radio scripts. The university community also enjoys free access to kayaks at the 60-acre lake in the middle of campus."
    
    if "kayaks" in query.lower():
        return "The UB community enjoys free access to kayaks at the 60-acre lake located in the middle of North Campus."

    if "RESOURCE_NAME" in entities:
        resource_name = entities["RESOURCE_NAME"]
        resource_match = campus_living_data[campus_living_data['Link Text'].str.contains(resource_name, case=False, na=False)]
        if not resource_match.empty:
            resource_url = resource_match.iloc[0]['URL']
            return f"Here's where you can find what you're looking for\n {resource_url}."
    

    if "EVENT_NAME" in entities:
        event_name = entities["EVENT_NAME"]
        event_match = events_data[events_data['Event Name'].str.contains(event_name, case=False, na=False)]
        if not event_match.empty:
            event_url = event_match.iloc[0]['URL']
            return f"Here's where you can find what you're looking for\n {event_url}"
        
    if "SCHOOL_NAME" in entities:
        school_name = entities["SCHOOL_NAME"]
        school_match = school_data[school_data['School/College Name'].str.contains(school_name, case=False, na=False)]
        if not school_match.empty:
            school_website = school_match.iloc[0]['Key Website']
            departments = school_match.iloc[0]['Departments/Programs Available']
            response = f"Here's some information about {school_name}:\n"
            response += f"Website: {school_website}\n"
            response += f"Departments/Programs: {departments}"
            return response
    
    return "Sorry, I couldn't find that event or resource."

# query = "What is the URL for Access to Justice Clinic?"
# response = answer_query(query, events_data, campus_living_data)
# print(response)

# query = "What is the URL for apply for housing?"
# response = answer_query(query, events_data, campus_living_data)
# print(response)