## Modeling Water in Los Angeles

_The history of the growth and development of Los Angeles... reveals its conscious use of water as a tool to build the “great metropolis of the Pacific”_ -- Vincent Ostrom, 1962 

Welcome to the repository for <i>Artes</i>, an integrated model of urban water resources in metropolitan Los Angeles. It  analyzes the potential for enhanced local water supplies in LA.<br><br>
The model is a product of the [California Center for Sustainable Communities](https://www.ioes.ucla.edu/ccsc/) at UCLA. <br><br>
Learn more about LA water management at the [The LA Water Hub](http://waterhub.ucla.edu) <br>
Github site: https://erikporse.github.io/artes/<br><br>

### Cast and Crew
**Principal Architect:** Erik Porse <br>
**Principal Investigator:** Stephanie Pincetl <br>
**Contributors and Collaborators**: <br>
Katie Mika, Mark Gold, Madelyn Glickfeld, and Kartiki Naik at UCLA <br>
Terri Hogue and Kimberly Manago at the [Hogue Hydrology Group](http://inside.mines.edu/THOGUE-home), Colorado School of Mines <br>
Diane Pataki and Liza Litvak at the [Urban Ecology Lab](http://bioweb.biology.utah.edu/pataki/), University of Utah<br>

### What's Here
The repository contains source code, model data, and a descriptive manual of the model.

**Manual**<br>
Documentation on model operations, development, and workflow.

**Code**<br>
- Model source code for the JWRPM study referenced below. Scripted in Python, it builds the model, interacts with the solver, and manages inputs and outputs. (LASM_31Dec16.py). <br>
- Scripts for aggregating sub-watersheds from the WMMS hydrologic model to the sub-watershed zones used in Artes (Located in Hydrology folder)
- R scripts for plotting watershed and wastewater treatment plant outflows for comparing and calibrating (Plots.r)

**Hydrology Folder**
- A mash of relatively unorganized scripts and data derived from the LA County WMMS model, which provides hydrologic inputs and is used for calibrating optimization in _Artes_.

**Data**
- Database with all model data inputs. Three databases are included. The first includes full demands and full historic imported water supplies (LASM_Data_D100_S100). The second includes full demands and no imported water (LASM_Data_D100_S0). The third includes agreesive conservation and no imported water supplies (LASM_Data_SP_S0). More documentation available in the manual and the JWRPM study describes development of methods and results. Spreadsheets are not cleaned up for prime time as of yet and contained links between some tables/sheets.
- Example output files, which can be copied to a local folder for output. The script searches for existing output files and will return an error without them. 

### Support
This work was supported by the Water Sustainability, & Climate Program at the National Science Foundation (NSF Award # 1204235), the Los Angeles Bureau of Sanitation, and the John Randolph Haynes and Dora Haynes Foundation. 

### Citing and Referencing the Model
Porse, Erik C., Kathryn B. Mika, Elizabeth Litvak, Kim Manago, Kartiki Naik, Madelyn Glickfeld, Terri Hogue, Mark Gold, Diane Pataki, and Stephanie Pincetl. “Systems Analysis and Optimization of Local Water Supplies in Los Angeles.” _Journal of Water Resources Planning and Management_. (In Press)

