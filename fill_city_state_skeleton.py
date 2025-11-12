import pandas as pd
import time
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional
import os 

# ⚠️ SICHERHEITSWARNUNG: Ersetzen Sie diesen Platzhalter durch Ihren ECHTEN API-Schlüssel.
# DIES IST NICHT EMPFOHLEN.
API_KEY = "AIzaSyC87YUMKSN3qSrb_qhXiIAI25V-GV_Cj78" 

# --- File Paths ---
# IMPORTANT: Using the specific absolute path you provided.
INPUT_CSV = os.path.normpath(r'C:\Studium_TU_Darmstadt\Master\3. Semester (Auslandssemester - Soul)\AI in Urban Planning and Design\ai-urban-final-project\data\raw\formatted_city_dates_skeleton.csv')

# The output file will be created in the same directory as the input file.
OUTPUT_CSV = os.path.join(os.path.dirname(INPUT_CSV), 'enriched_city_data_output_en.csv')

print(f"Input Path: {INPUT_CSV}")
print(f"Output Path: {OUTPUT_CSV}")

# --- Pydantic Schema for Structured LLM Output ---
class CityData(BaseModel):
    """Schema for the enriched data, matching the CSV columns."""
    Country: str = Field(description="The country of the city at the specified date. Use 'Not Found' if no data is available.")
    Region_Code: str = Field(description="The region code or administrative region at the specified date. Use 'Not Found' if no data is available.")
    Climate_Zone: str = Field(description="The climate zone of the city (e.g., 'Cfa', 'Köppen classification'). Use 'Not Found' if no data is available.")
    Population_2025_Mio: Optional[float] = Field(description="The estimated population in millions for the year of the date. Use 0.0 if not found.")
    Median_Age_Years: Optional[float] = Field(description="The median age of the population in years for the year of the date. Use 0.0 if not found.")
    GDP_Billion_USD: Optional[float] = Field(description="The GDP of the city/region in billions USD for the year of the date. Use 0.0 if not found.")
    GDP_per_Capita_USD: Optional[int] = Field(description="The GDP per capita in USD for the year of the date. Use 0 if not found.")
    Search_Status: str = Field(description="Brief summary of the search result (e.g., 'All data found', 'Population only found', 'No data found').")


def enrich_data_with_gemini(csv_file_path: str, output_file_path: str):
    """
    Performs data enrichment using the Gemini API.
    """
    if API_KEY == "YOUR_API_KEY_HERE":
        print("🛑 ERROR: Please replace 'YOUR_API_KEY_HERE' with your actual API key in the script.")
        return

    try:
        # Initialize the Gemini Client with the hard-coded API key
        client = genai.Client(api_key=API_KEY) 
        print("Gemini Client initialized.")
        
        # Read the CSV file from the specified path
        df = pd.read_csv(csv_file_path)
        print(f"File '{csv_file_path}' loaded with {len(df)} rows.")
        
        # Add the Status column if it doesn't exist
        if 'Search_Status' not in df.columns:
            df['Search_Status'] = None

    except FileNotFoundError:
        print(f"🛑 ERROR: File not found at the path: '{csv_file_path}'. Please check the path.")
        return
    except Exception as e:
        print(f"Error during loading or initialization: {e}")
        return

    # Iterate through each row of the DataFrame
    for index, row in df.iterrows():
        city = row['City_ID']
        date_str = row['Date']
        
        print(f"\nProcessing row {index} of {len(df)}: {city} on date {date_str}...")

        # Create the specific prompt
        prompt = f"""
        Perform a **Google Search** to find the following historical data for the city "{city}" 
        at the **closest possible year near the date {date_str}**. 
        Search for: Country, Region Code, Climate Zone, Population (in millions), Median Age, 
        GDP (in billion USD), and GDP per Capita (in USD).

        - The date is {date_str}. Try to find data as close to this date/year as possible.
        - If data is not found, use the exact string 'Not Found' for string fields 
          and the value '0.0'/'0' for numerical fields.
        - The population must be given in millions (e.g., 15.3 for 15,300,000).
        - The result must strictly conform to the provided JSON schema.
        - Summarize the search result briefly in the 'Search_Status' field.
        """
        
        try:
            # Sende die Anfrage mit aktiviertem Tool und strukturiertem Output
            response = client.models.generate_content(
                model='gemini-2.5-pro',
                contents=prompt,
                config=types.GenerateContentConfig(
                    # 1. Google Search Tool is enabled
                    tools=[{"google_search": {}}], 
                    # 2. REMOVED response_mime_type="application/json" to fix the 400 error
                    response_schema=CityData,
                ),
            )
            
            # Parse the JSON response
            enriched_data = CityData.model_validate_json(response.text)
            
            # Transfer the data to the DataFrame
            data_to_update = enriched_data.model_dump()
            for field, value in data_to_update.items():
                if field not in ['City_ID', 'Date']:
                     df.at[index, field] = value 

            print(f" -> Data successfully enriched. Status: {data_to_update.get('Search_Status', 'N/A')}")
            
            # INCREASED PAUSE to 31 seconds to respect the 2 RPM free-tier quota limit (30 seconds per request)
            time.sleep(31) 

        except Exception as e:
            print(f" -> Error in LLM request or parsing for {city}: {e}")
            df.at[index, 'Search_Status'] = f"LLM Error: {str(e)[:50]}..."
            # Mark fields as error for easy identification
            for col in ['Country', 'Region_Code', 'Climate_Zone']:
                 df.at[index, col] = 'LLM_ERROR'
            for col in ['Population_2025_Mio', 'Median_Age_Years', 'GDP_Billion_USD', 'GDP_per_Capita_USD']:
                 df.at[index, col] = 0.0
                 
            # PAUSE on error as well, since the failed call still counts against the quota
            time.sleep(31)


    # Save the enriched DataFrame
    df.to_csv(output_file_path, index=False)
    print(f"\n✅ Enrichment complete. Result saved to '{output_file_path}'.")

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    enrich_data_with_gemini(INPUT_CSV, OUTPUT_CSV)