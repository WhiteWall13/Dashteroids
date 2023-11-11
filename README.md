# Dashteroids :comet:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

Welcome to Dashteroids, your comprehensive dashboard for visualizing and analyzing meteorite landing data. This tool is designed to provide insightful analytics through interactive charts and maps. **It can be used with our without internet connection**.

## User Guide :book:
### Prerequisites

Before you begin, make sure you have the following prerequisites installed:

- **Python**: Version 3.9 or higher. Python is the backbone of our dashboard, and you'll need it to run the application directly.
- **Pip**: The Python package installer, which you will use to install the dependencies required by Dashteroids.
or
- **Docker**: An optional but recommended way to deploy the application, ensuring consistency across different environments.

### Tech Stack
Dashteroids is built using a few powerful technologies :
- **Python**: For server-side logic and running the Dash app.
- **Dash**: A Python framework for building analytical web applications, making it easy to create interactive, web-based data visualizations.
- **Docker**: For creating a containerized version of the application, which simplifies deployment and scaling.

### How to use
#### Install
1. **Clone the Repository**: Get a copy of the source code on your local machine.
``` bash
git clone https://github.com/WhiteWall13/Dashteroids
```
#### Using python
**Option 1**: Running with Python
If you prefer to run the application directly using Python, follow these steps :
1. **Install Dependencies**: Use pip to install the required Python packages.
``` bash
pip install -r requirements.txt
```

2. **Start the Development Server**: Launch the application using Python.
``` bash
python main.py
```
3. **Access the Dashboard**: Open your preferred web browser and visit `http://localhost:8050` to start exploring the data.


#### Using Docker
**Option 2**: Running with Docker
For those who prefer Docker for its ease of use and deployment, here's how to get started:


1. **Build the Docker Image**: This will create a Docker image with all the necessary dependencies pre-installed.
``` bash
docker build -t dashteroids .
```
2. **Run the Docker Container**: Start a container from the image. This command also maps the container's port to your local port.
``` bash
docker run -p 8050:8050 dashteroids
```
3. **View the Dashboard**: Just like with the Python option, open your browser and go to `http://localhost:8050`.

## Data Analyze :bar_chart:
This [dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh), curated by Javier de la Torre and The Meteoritical Society, offers a detailed record of meteorite landings, capturing each meteorite's location, type, mass, and discovery. Spanning diverse fields from geographical coordinates to meteorite classifications, it provides both a chronological and categorical view of these celestial events. The [dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) distinguishes between 'valid' and 'relict' meteorites, highlighting the interaction between these space objects and Earth's environment. Significantly, post-1969, the year of the first Moon landing, marks an era of increased meteorite documentation, reflecting a surge in space exploration interest. This [dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) not only traces the scientific journey of meteorite discovery but also reflects humanity's evolving curiosity in space.

### Exploration of the Meteorite Landings Dataset: A Datatable
Our first visualization offers an interactive datatable, providing a direct and detailed view of the meteorite landings data. This table is designed to facilitate an initial, in-depth exploration of the [dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh), showcasing the raw data in its most granular form (I just transformed the year data from a timestamp format to an integer format. This modification enhances the readability and usability of the data). This datatable is an excellent starting point for anyone interested in delving into the world of meteorite landings.

### Analysis of Predominant Meteorite Classes in the Dataset : A pie chart
The [dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) reveals a significant distribution of meteorite classes, predominantly featuring various types of chondrites and their subcategories. Here's an analysis of why these particular groups are more commonly found:

#### Chondrites (L and H Classes)
L (Low iron) and H (High iron) Chondrites: These are among the most common types of meteorites. L chondrites have low iron/nickel metal content, while H chondrites have a higher metal content. Their abundance in the [dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) reflects their frequent occurrence in meteorite falls on Earth.
LL (Low metal, Low iron) Chondrites: This subgroup of chondrites has even lower metal content. They are less common than L and H types but still significant in number.
#### Petrologic Types (Numbered Suffixes)
Degrees of Thermal Alteration: The numbers in the classification (e.g., L4, H5) indicate the degree of thermal alteration or metamorphism the meteorite has undergone. Higher numbers suggest more extensive thermal metamorphism, likely from heating events during their space journey or upon entry into Earth's atmosphere.
#### Scientific and Collection Bias
Detection and Collection: More common types, like certain chondrites, are often easier to find and identify due to their size, magnetic properties, and distinctive appearance, leading to higher representation in collections.
Scientific Interest: Some classes may be more represented due to focused scientific interest, leading to more active collection and cataloging efforts.
#### Conclusion
The predominance of certain chondrite classes in the [dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) reflects both their natural abundance in meteoritic falls and the influence of collection and classification practices. These meteorites offer valuable insights into the early solar system and the dynamic processes that bring these celestial objects to Earth.

### Analysis of Meteorite Landings Over Time : Histogram and Line Chart
- The data shows a significant increase in the number of meteorite landings recorded starting around the 1970s. This coincides with the era of the first human landing on the Moon in 1969, which greatly heightened public and scientific interest in space exploration and celestial phenomena. Advancements in technology and scientific methodologies during this period made the detection and recording of meteorite landings more efficient and widespread.
- In earlier times, many meteorite landings likely went unrecorded or unrecognized due to the inability to distinguish them from terrestrial objects. Without modern scientific knowledge and tools, identifying meteorites was a significant challenge. Also, over time, meteorites can become weathered, buried, or otherwise altered, making them harder to identify and catalog. This natural process means that older meteorites are less likely to be found and recorded.

### Analysis of Meteorite Findings by Continent : Bar Chart
The bar chart depicting meteorite findings across different continents reveals some fascinating geographical trends. Here's an expanded analysis of why certain continents show higher numbers:

#### Antarctica (11,919):

- Ideal Preservation Conditions: Antarctica's ice and snow provide a stark background against which dark meteorites can be easily spotted. Additionally, the cold environment helps preserve the meteorites in almost pristine condition.
- Concentrated Efforts: Scientific expeditions specifically aimed at recovering meteorites are more common in Antarctica, contributing to the high number of findings.

#### Africa (9,237):

- Desert Environments: Large desert areas, like the Sahara, offer similar visibility advantages as Antarctica. Meteorites are easier to spot against the sandy background and are less likely to be obscured by vegetation or human activity.
- Size and Exploration: Africa's vast land area and the increasing efforts in scientific exploration in desert regions contribute to the high number of meteorite recoveries.

#### Asia (3,573) and North America (1,827):

- Population Density and Accessibility: In more densely populated or vegetated areas, meteorites are harder to find. Additionally, accessibility for scientific exploration can be limited in certain regions.
- Reporting and Collection Practices: Cultural factors and the presence of established scientific communities can influence how many meteorites are reported and collected.

#### South America (1,576), Oceania (909), and Europe (635):

- Geographical and Climatic Factors: The lower numbers in these continents could be due to a combination of factors like smaller land areas (in the case of Europe and Oceania), denser vegetation, and different climatic conditions that make meteorite discovery and preservation more challenging.
- Historical and Cultural Context: The history of scientific exploration and the level of interest in meteoritics can vary significantly, impacting the number of meteorites found and reported.

#### Conclusion
The distribution of meteorite findings across continents is influenced by a complex interplay of environmental, geographical, and human factors. Antarctica and Africa lead in numbers due to their favorable conditions for meteorite preservation and discovery, as well as concentrated scientific efforts. In contrast, factors like population density, vegetation cover, and the extent of scientific exploration play significant roles in the lower numbers observed in other continents. This distribution underscores the importance of environmental and human elements in the discovery and study of meteorites.

### Population Density and Technological Advancement: A Map

The final visualization in the [dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) is a map showing the points of recorded asteroid landings and a corresponding density map. This map reveals distinct patterns in asteroid discovery, which can be attributed to several factors:

#### Depending to the population
- Higher Discoveries in Populated Areas: The map shows a higher concentration of asteroid discoveries in technologically advanced and densely populated regions. This is likely due to the increased likelihood of human observation and reporting in these areas.
- Technological Resources: Advanced technological capabilities, including better detection equipment and more robust scientific infrastructure, contribute to more frequent discoveries in developed regions.
- Cultural and Scientific Factors: The level of interest in astronomy and space science, as well as the cultural importance placed on such discoveries, can vary by region, influencing the number of reported findings.

#### Geographical and Environmental Factors

- Land vs. Water: It's notable that there are very few, if any, asteroid discoveries in large bodies of water. This is expected, as oceans cover a vast majority of the Earth's surface, yet they are largely unmonitored for such events due to the logistical challenges and the lack of permanent human presence.
- Visibility and Accessibility: In remote or densely vegetated areas, asteroid discoveries are less common. This is due to both the difficulty in spotting these objects and the challenges in accessing these locations for verification and study.

#### Conclusion

The asteroid discovery points and density map provide a compelling visualization of where asteroid landings have been recorded. The distribution is heavily influenced by human factors such as population density, technological advancement, and scientific interest, as well as by geographical and environmental considerations. This map underscores the interplay between human observation, technological capabilities, and natural occurrences in the documentation of celestial events.

### Synthesis of Meteorite Landings Data Analysis 
The Meteorite Landings [dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) offers a unique window into the history of celestial encounters with Earth, enriched by diverse data ranging from geographical locations to meteorite classifications. Key insights include the predominance of certain meteorite classes, reflecting both natural abundance and scientific collection biases. The temporal distribution of meteorite landings, particularly the surge post-1969, highlights the impact of technological advancements and growing scientific interest. Geographical trends in discoveries underscore the interplay of environmental conditions, human factors and technological factors, with notable concentrations in regions like Antarctica and Africa. This [dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) not only charts the physical journey of these space travelers but also encapsulates humanity's evolving curiosity and engagement with the cosmos.

## Developper guide :technologist:

After successfully launching the Dashteroids dashboard, you may be curious about the underlying code and architecture. This section provides a detailed walkthrough of the codebase, making it easier for developers to navigate and understand the project.

### Architecture of the project
In order to provide a clear overview of the project's architecture and file organization, the following diagram illustrates the structure of the Dashteroids project. This visual representation will help developers and contributors to quickly understand the layout and relationships between different components of the application.

```mermaid
graph TD;
    Dashteroids-->Dockerfile;
    Dashteroids-->README.md;
    Dashteroids-->config.ini;
    Dashteroids-->requirements.txt;
    Dashteroids-->main.py;
    Dashteroids-->dashboard;
    dashboard-->app;
    dashboard-->graphs;
    app-->app_py["app.py"];
    app-->assets;
    app-->callbacks_py["callbacks.py"];
    app-->layout_py["layout.py"];
    assets-->favicon["favicon.ico"];
    graphs-->charts_py["charts.py"];
    graphs-->maps_py["maps.py"];
    Dashteroids-->data;
    data-->files;
    data-->get_data_py["get_data.py"];
    files-->csv["Meteorite_Landings.csv"];
```

### Understanding the Entry Point

- `main.py`: This script is where the Dash server is initialized and run. It sets up the server, registers the app's layout and callbacks, and starts the server loop. When you execute `python main.py`, this script kicks off the entire application.

### Dashboard Directory Structure

The `dashboard/` directory is the heart of the application, containing all the Dash-related components.

#### App Module

- `App/`: This subdirectory is crucial as it contains the core components of the Dash application.
  - `app.py`: Defines the Dash app instance and server. It's where you configure global settings for the Dash app, such as the title, external stylesheets, and server settings.
  - `layout.py`: Contains the HTML and Dash components that define the structure and appearance of the web application. It's essentially the blueprint of your dashboard's user interface.
  - `callbacks.py`: Houses the callback functions that make the dashboard interactive. Callbacks in Dash link the interactive components (like buttons and dropdowns) with the backend logic that updates the app's data and visuals.

#### Graphs Module

- `graphs/`: This directory includes the Python modules that create the visualizations.
  - `charts.py`: Contains functions that define the structure and style of the charts used in the dashboard. These functions are called by the callbacks to update the charts based on user interaction.
  - `maps.py`: Similar to `charts.py`, but focused on generating geospatial visualizations. It uses data processing and mapping libraries to turn raw data into interactive maps.

### Data Handling

- `data/`: This directory is where the datasets and data processing scripts reside.
  - `get_data.py`: This file contains functions that handle data retrieval, cleaning, and preprocessing. They transform raw data into a format that can be used by the dashboard's visual components.
  - `file/Meteorite_Landings.csv`: Depending on the project setup, this could include CSV file, JSON data, or links to databases that the application queries to retrieve its data.
- `file/Meteorite_Landings.csv`: This CSV file serves as an offline dataset for the dashboard. This data is used to populate the dashboard with information and visualizations when there is no active internet connection or when live data fetching is not required.


## Author ✍️
#### Nicolas Hameau  
- ![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white) [nicolas.hameau@edu.esiee.fr](mailto:nicolas.hameau@edu.esiee.fr)
- ![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white) [Nicolas Hameau](http://linkedin.com/in/nicolas-hameau-13242002)
- ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) [WhiteWall13](https://github.com/WhiteWall13)


