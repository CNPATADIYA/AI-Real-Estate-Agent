import streamlit as st
from typing import Dict, List
from pydantic import BaseModel, Field
import pandas as pd
import json

class RealEstateAgent:
    """Agent responsible for finding properties and providing recommendations"""
    
    def __init__(self, city, area, budget, possesion, property_type, property_configuration):
        self.city = city
        self.area = area
        self.budget = budget
        self.possesion = possesion
        self.property_type = property_type
        self.property_configuration = property_configuration

        self.main_data = pd.read_csv("../../data/main_data.csv")
        self.nearby_place = pd.read_csv("../../data/nearby_place.csv")
        self.ratings = pd.read_csv("../../data/ratings.csv")


    def parse_properties(self, properties) -> List:
        nearby_place = self.nearby_place[self.nearby_place["URL"].isin(properties["URL"])]
        ratings = self.ratings[self.ratings["URL"].isin(properties["URL"])]

        properties_list = []
        for i in range(len(properties)):
            URL = properties.iloc[i]["URL"]
            pop = {}
            pop["basic_details"] = properties.iloc[i].to_dict()
            pop["nearby_places"] = []
            pop["ratings"] = []
            for k,v in ratings[ratings["URL"]==URL][["Feature", "Rating"]].T.to_dict().items():
                #print(v)
                pop["ratings"].append(v)
            
            for k,v in nearby_place[nearby_place["URL"]==URL][["Category", "Name", "Travel Time", "Distance"]].T.to_dict().items():
                pop["nearby_places"].append(v)

            properties_list.append(pop)

        return properties_list


    def find_properties(self) -> str:
        """Find and analyze properties based on user preferences"""
        formatted_city = self.city.lower()
        formatted_location = self.area.lower()
        property_type_prompt = "apartment" if self.property_type == "Apartment" else "villa"
        formatted_property_configuration = "2"
        
        if self.property_configuration == "2 BHK":
            formatted_property_configuration = "2"
        elif self.property_configuration == "3 BHK":
            formatted_property_configuration = "3"
        elif self.property_configuration == "4 BHK":
            formatted_property_configuration = "4"
        else:
            formatted_property_configuration = "5"

        min_price = 5000000.0
        max_price = 9000000.0

        if self.budget == "< ₹50 Lakhs":
            min_price = 0.0
            max_price = 5000000.0
        elif self.budget == "₹50L - ₹1Cr":
            min_price = 5000000.0
            max_price = 10000000.0
        else:
            min_price = 10000000.0
            max_price = 500000000.0


        formatted_possesion = pd.to_datetime('today').normalize()

        if self.possesion == "Urgent (0-3 months)":
            formatted_possesion += pd.Timedelta(days=90)
        elif self.possesion == "In 6 months":
            formatted_possesion += pd.Timedelta(days=31*6)
        elif self.possesion == "In 1 year":
            formatted_possesion += pd.Timedelta(days=365)
        elif self.possesion == "Less than 3 year":
            formatted_possesion += pd.Timedelta(days=3*365)
        else:
            formatted_possesion += pd.Timedelta(days=365*10)
        

        area_filter = self.main_data["Address"].str.lower().str.contains(formatted_location)
        property_type_filter = self.main_data["Configuration"].str.lower().str.contains(property_type_prompt)
        property_configuration_filter = self.main_data["Configuration"].str.lower().str.contains(formatted_property_configuration)
        bugdet_filter = (self.main_data["min_price"] >= min_price) & (self.main_data["max_price"] <= max_price)
        possesion_filter = pd.to_datetime(self.main_data["Possession Starts"]) <= formatted_possesion

        properties = self.main_data[area_filter & property_type_filter & property_configuration_filter & bugdet_filter & possesion_filter]
        if len(properties) == 0:
            return "No properties founds with given preference"
        
        #print("INDEX :::::::::::::::::::: ", properties.index, properties.columns)
        properties_json = self.parse_properties(properties)

            
        #print("Processed Properties:", properties_json)

        # Convert properties_json[:5] to a formatted string
        formatted_properties = json.dumps(properties_json[:5], indent=2)  # Converts list of dicts to string

        # Ensure the string is properly escaped for f-string usage
        formatted_properties = formatted_properties.replace("{", "{{").replace("}", "}}")
        
        st.session_state.user_preference = (
            f"""As a real estate expert, analyze these properties and market trends:

            Properties Found:
            {formatted_properties}


            **IMPORTANT INSTRUCTIONS:**
            1. ONLY analyze properties from the above JSON data that match the user's requirements:
               - Property Category: {self.property_type}
               - Property Type: {self.property_configuration}
               - Budget: {self.budget}
               - Possesion Date: within {formatted_possesion}
            2. DO NOT create new categories or property types
            3. From the matching properties, select 5-6 properties with best suitable user requirements

            Please provide your analysis in this format:
            
            🏠 SELECTED PROPERTIES
            • List only 5-6 best matching properties with best suitable user requirements
            • For each property include:
              - Name and Location
              - Price (with value analysis)
              - Key Features
              - Pros and Cons

            💰 BEST VALUE ANALYSIS
            • Compare the selected properties based on:
              - Price per sq ft
              - Location advantage
              - Amenities offered

            📍 LOCATION INSIGHTS
            • Specific advantages of the areas where selected properties are located

            💡 RECOMMENDATIONS
            • Top 3 properties from the selection with reasoning
            • Investment potential
            • Points to consider before purchase

            🤝 NEGOTIATION TIPS
            • Property-specific negotiation strategies

            Format your response in a clear, structured way using the above sections.
            
            After that If user have any specific questions about suggested properties help them to solve their queries.
            If it is not related to properties than just say that dont know answer.
            If user ask question related to different properties or areas just ask user to provide preference in preference tab.
            """
        )
        
        return st.session_state.user_preference

    def get_location_trends(self, city: str) -> str:
        """Get price trends for different localities in the city"""
        raw_response = self.firecrawl.extract([
            f"https://www.99acres.com/property-rates-and-price-trends-in-{city.lower()}-prffid/*"
        ], {
            'prompt': """Extract price trends data for ALL major localities in the city. 
            IMPORTANT: 
            - Return data for at least 5-10 different localities
            - Include both premium and affordable areas
            - Do not skip any locality mentioned in the source
            - Format as a list of locations with their respective data
            """,
            'schema': LocationsResponse.model_json_schema(),
        })
        
        if isinstance(raw_response, dict) and raw_response.get('success'):
            locations = raw_response['data'].get('locations', [])
    
            analysis = self.agent.run(
                f"""As a real estate expert, analyze these location price trends for {city}:

                {locations}

                Please provide:
                1. A bullet-point summary of the price trends for each location
                2. Identify the top 3 locations with:
                   - Highest price appreciation
                   - Best rental yields
                   - Best value for money
                3. Investment recommendations:
                   - Best locations for long-term investment
                   - Best locations for rental income
                   - Areas showing emerging potential
                4. Specific advice for investors based on these trends

                Format the response as follows:
                
                📊 LOCATION TRENDS SUMMARY
                • [Bullet points for each location]

                🏆 TOP PERFORMING AREAS
                • [Bullet points for best areas]

                💡 INVESTMENT INSIGHTS
                • [Bullet points with investment advice]

                🎯 RECOMMENDATIONS
                • [Bullet points with specific recommendations]
                """
            )
            
            return analysis.content
            
        return "No price trends data available"
    

def setsession(city, area, possesion, budget, property_type, property_configuration):
    st.session_state.property_agent = RealEstateAgent(city, area, budget, possesion, property_type, property_configuration)


st.set_page_config(
    page_title="AI Real Estate Agent",
    page_icon="🏠",
    layout="wide"
)

with st.sidebar:
    st.write("Welcome Jay shree Krishna")

st.title("🏠 AI Real Estate Agent")
st.info(
    """
    Welcome to the AI Real Estate Agent! 
    Enter your search criteria below to get property recommendations 
    and location insights.
    """
)

col1, col2 = st.columns(2)

with col1:
    city = st.text_input(
        "City",
        placeholder="Enter city name (e.g., Ahmedabad)",
        help="Enter the city where you want to search for properties",
        value="Ahmedabad"
    )

    area = st.text_input(
        "Area (in Ahmemdabad)",
        placeholder="Enter area name (e.g., Shela)",
        help="Enter the area in ahmedabad where you want to search for properties"
    )
    
    possesion = st.selectbox(
        "How soon are you looking to buy?",
        options= ["Urgent (0-3 months)", "In 6 months", "In 1 year", "Less than 3 year", "Okay after 3 years"],
        help="Property possesion"
    )

with col2:
    budget = st.selectbox(
        "Your Budget",
        ("< ₹50 Lakhs", "₹50L - ₹1Cr", "₹1Cr+"),
        help="Enter your budget"
    )
    
    property_type = st.selectbox(
        "Property Type",
        options=["Apartment", "Individual House"],
        help="Select the specific type of property"
    )

    property_configuration = st.selectbox(
        "Property Configuration",
        options=["2 BHK", "3 BHK", "4 BHK", "4 BHK+"],
        help="Select the specific configuration of property"
    )

if st.button("🔍 Start Search", use_container_width=True):
    if not area:
        st.error("⚠️ Please enter a Area !")
    
    if not city:
        st.error("⚠️ Please enter City")
    
    try:
        setsession(city, area, possesion, budget, property_type, property_configuration)
        with st.spinner("🔍 Searching for properties..."):
            st.session_state.property_agent.find_properties()
            
            st.success("✅ Property search completed!")
            
            st.switch_page("chatbot.py")
            
            # with st.spinner("📊 Analyzing location trends..."):
            #     location_trends = st.session_state.property_agent.get_location_trends(city)
                
            #     st.success("✅ Location analysis completed!")
                
            #     with st.expander("📈 Location Trends Analysis of the city"):
            #         st.markdown(location_trends)
            
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
