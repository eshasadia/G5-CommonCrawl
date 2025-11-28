from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
from io import StringIO
import json
import re 
import csv 

llm = ChatOllama(
    model="gemma3:latest",
    temperature=0.1,
    max_tokens=512
)

d25 = pd.read_csv('clean_scrape_data_2025.csv')
# or d24 = pd.read_csv('clean_scrape_data_2024.csv'), whichever we are working with


###### Specify the prompt template ####################################
prompt = ChatPromptTemplate.from_template("""
You are an expert annotator who recognizes policies in the United Kingdom well. You will be given a government news item.

Your task:

1. Identify **ONE** explicit or implicit policy instrument present in the text.

2. Classify it using one **Main Classification**:
   - Welfare (grants, benefits, subsidies)
   - Monetary (tax changes, fiscal incentives)
   - Legislative (laws, regulations, statutory changes)
   - Administrative (guidelines, standards, reporting requirements)
   - Institutional (creation or restructuring of agencies or bodies)
   - Market-based (permits trading, carbon pricing)
   - Informational (public campaigns, nudging)
   - Other (strategic plans, consultations)

3. Assign a **Secondary Classification** (optional).

4. Output **ONLY** a structured JSON with the following keys:
   - "Policy Instrument" (the instrument you identified)
   - "Main Classification" (the primary classification)
   - "Secondary Classification" (if available)

Do not include any explanation, commentary, or text outside the JSON.

Content to analyze:
{news_item}
""")


# ---- Prepare output lists for temporary storage ----
model_outputs = []  # Store raw output for each row
output_data = []  # Final data for CSV or further processing

# Define the CSV output file name
output_file = "gemma_output_2025.csv" # or 2024

# ---- Open the CSV file in write mode at the start ----
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Policy Instrument', 'Main Classification', 'Secondary Classification']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header to the CSV file
    writer.writeheader()

# ---- Open the JSON file in write mode at the start ----
json_output_file = "gemma_temp_raw_outputs_25.json"
# Start the JSON file with an opening bracket to create a JSON array
with open(json_output_file, 'w') as json_file:
    json_file.write("[\n")  # Start the JSON array

###### Process Each Row #########################
for idx, row in d25.iterrows():
    chain = prompt | llm
    result = chain.invoke({"news_item": row["content"]})

    try:
        # Store raw model output for debugging purposes
        raw_output = result.content.strip()  # Strip leading/trailing whitespace

        # Clean the raw output: Remove the markdown-like ```json and ``` parts
        cleaned_output = re.sub(r'^```json\s*\n?', '', raw_output)  # Remove leading ```json
        cleaned_output = re.sub(r'\n?```$', '', cleaned_output)  # Remove trailing ```

        # Print the cleaned raw result for debugging
        print(f"Cleaned raw model output for row {idx+1}: {repr(cleaned_output)}\n")

        # Check if the result is empty or contains only whitespace
        if not cleaned_output or cleaned_output.isspace():
            print(f"Warning: Empty or invalid response for row {idx+1}. Skipping this row.")
            continue  # Skip empty or invalid responses

        # Log raw output to a file for further inspection
        with open("gemma_errors_25.txt", "a") as f:
            f.write(f"\nCleaned raw model output for row {idx+1}:\n{cleaned_output}\n")

        # Try to ensure the cleaned raw output is a valid JSON object
        try:
            model_output = json.loads(cleaned_output)  # Try decoding the cleaned JSON

        except json.JSONDecodeError as e:
            print(f"JSON decoding error on row {idx+1}: {e}. Storing raw output for later inspection.")
            # Store raw output in case of error
            with open("gemma_errors_25.txt", "a") as f:
                f.write(f"\nRow {idx+1} cleaned output (JSON error):\n{cleaned_output}\nError: {e}\n")
            continue  # Skip this row as it's invalid JSON

        # Extract the necessary values from the JSON response
        policy_instrument = model_output.get("Policy Instrument", None)
        main_classification = model_output.get("Main Classification", None)
        secondary_classification = model_output.get("Secondary Classification", None)

        # Ensure that the new columns are added if not already present in the DataFrame
        if "Policy Instrument" not in d25.columns:
            d25["Policy Instrument"] = None
        if "Main Classification" not in d25.columns:
            d25["Main Classification"] = None
        if "Secondary Classification" not in d25.columns:
            d25["Secondary Classification"] = None

        # Add the extracted values to the original DataFrame for this row
        d25.at[idx, "Policy Instrument"] = policy_instrument
        d25.at[idx, "Main Classification"] = main_classification
        d25.at[idx, "Secondary Classification"] = secondary_classification

        # Also store data in output_data for final export or further use
        output_data.append({
            "Policy Instrument": policy_instrument,
            "Main Classification": main_classification,
            "Secondary Classification": secondary_classification
        })

        # Write the processed data into the CSV file after each row iteration
        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'Policy Instrument': policy_instrument,
                'Main Classification': main_classification,
                'Secondary Classification': secondary_classification
            })

        # Append the raw output to the JSON file after processing each row
        with open(json_output_file, 'a') as json_file:
            json.dump(model_output, json_file, indent=4)
            json_file.write(",\n")  # Add a newline for separation between entries

        print(f"Processed row {idx+1}/{len(d25)} and updated DataFrame.")

    except Exception as e:
        print(f"Error processing row {idx+1}: {e}")
        # Store raw output in case of error
        with open("gemma_errors_25.txt", "a") as f:
            f.write(f"\nRow {idx+1} cleaned raw output:\n{cleaned_output}\nError: {e}\n")

##### Close the JSON file properly after processing all rows ############################
with open(json_output_file, 'a') as json_file:
    json_file.write("\n]")  # Close the JSON array

print("Finished processing all rows.")

