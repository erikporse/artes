## Modeling Water in Los Angeles

_The history of the growth and development of Los Angeles... reveals its conscious use of water as a tool to build the “great metropolis of the Pacific”_ <br>-- Vincent Ostrom, 1962 

Welcome to the repository for <i>Artes</i>, an integrated model of urban water resources in metropolitan Los Angeles. It  analyzes the potential for enhanced local water supplies in LA.<br><br>
The model is a product of the [California Center for Sustainable Communities](https://www.ioes.ucla.edu/ccsc/) at UCLA. <br><br>
Learn more about LA water management at the [The LA Water Hub](http://waterhub.ucla.edu) <br>
Github site: https://erikporse.github.io/artes/<br>

### Cast and Crew
**Principal Architect:** Erik Porse <br>
**Principal Investigator:** Stephanie Pincetl <br>
**Contributors and Collaborators**: <br>
Katie Mika, Mark Gold, Madelyn Glickfeld, Eric Fournier, and Kartiki Naik at UCLA <br>
Terri Hogue and Kimberly Manago at the [Hogue Hydrology Group](http://inside.mines.edu/THOGUE-home), Colorado School of Mines <br>
Diane Pataki and Liza Litvak at the [Urban Ecology Lab](http://bioweb.biology.utah.edu/pataki/), University of Utah<br>

### What's Here
The repository contains source code, data, and a descriptive manual of the model.

_Manual_<br>
Documentation on model operations, development, and workflow (Updated August 2019)

_Code_<br>
- Model source code, including multiple versions used in studies for applications maximizing local sources, minimizing costs, and simulating groundwater exchange pools. Scripted in Python, the code builds the model, interacts with the solver, and manages inputs and outputs. (LASM_31Dec16.py, for example). <br>
- Scripts for aggregating sub-watersheds from the WMMS hydrologic model to the sub-watershed zones used in Artes (Located in Hydrology folder)
- R scripts for plotting watershed and wastewater treatment plant outflows for comparing and calibrating (Plots.r)

_Hydrology_
- A mash of moderately organized scripts and data derived from the LA County WMMS model, which provides hydrologic inputs and is used for calibrating optimization in _Artes_.

_Data_
- Databases with model data inputs for three model variations: maximizing flows from local sources (Porse et al, 2017), simulating groundwater exchange pools (Porse et al, 2017), and minimizing total costs (Porse et al, 2018). 
- Data files are named according to scenario parameters, For instance, for the max_flows scenario, databases include full demands and full historic imported water supplies (LASM_Data_D100_S100). The second includes full demands and no imported water (LASM_Data_D100_S0). The third includes agreesive conservation and no imported water supplies (LASM_Data_SP_S0). More documentation available in the manual and the JWRPM study describes development of methods and results. 
- Example output files, which can be copied to a local folder for output. The script searches for existing output files and will return an error without them. The folder sp_scenario shows output files for the <i>Sustainability Planning</i> scenario presented in Porse (2017).
- Historic data, used in calibrating or populating the model. This includes data for wastewater treatment and reuse plants and LA County stormwater capture basins, along with an analysis of historical and current pumping rights in groundwater basins (<i>see Porse et al, 2015, Geojournal</i>). Source credits are provided in the model manual and documentation. 

_Geo_
- Repository of shape files used in building the link-node network of the model. 
- Shape files of watersheds derived from the WMMS model. 
- Shape files of LA County water retailers represented in the model and mapped on the [The LA Water Hub](http://waterhub.ucla.edu), with associated data (primarily from 2010 Urban Water Management Plans). Includes shape files for both water retailers and MWD member agencies. Some agencies are members of both data sets. 

### Support
This work was supported by the Water Sustainability, & Climate Program at the National Science Foundation (NSF Award # 1204235), the Los Angeles Bureau of Sanitation, and the John Randolph Haynes and Dora Haynes Foundation. 

### Citing Research and the Model
Porse, Erik, Kathryn B. Mika, Elizaveta Litvak, Kimberly F. Manago, Kartiki Naik, Madelyn Glickfeld, Terri S. Hogue, Mark Gold, Diane E. Pataki, and Stephanie Pincetl10. "Systems Analysis and Optimization of Local Water Supplies in Los Angeles." Journal of Water Resources Planning and Management. Vol. 143, no. 9 (2017).

Porse, Erik, Kathryn B. Mika, Elizaveta Litvak, Kimberly F. Manago, Terri S. Hogue, Mark Gold, Diane E. Pataki, and Stephanie Pincetl10. "The Economic Value of Local Water Supplies in Los Angeles." Nature Sustainability. 1. (6). 289 (2018).

Porse, Erik C., Artes: A Model of Urban Water Resources Management in Los Angeles. v. 4.0. UCLA California Center for Sustainable Communities, Los Angeles, CA, 2019; URL: https://erikporse.github.io/artes/.
