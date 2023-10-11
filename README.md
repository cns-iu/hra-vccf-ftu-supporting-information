## Functional Tissue Unit in Human Reference Atlas

Functional tissue units (FTUs) form the basic building blocks of organs and are important for understanding and modeling the healthy physiological function of the organ and changes during disease states. In this first comprehensive catalog of FTUs, we document the definition, physical dimensions, vasculature, and cellular composition of 22 anatomically correct, nested functional tissue units (FTUs) in 10 healthy human organs. The catalog includes datasets, illustrations, an interactive online FTU explorer, and a large printable poster. All data and code are freely available. This is part of a larger ongoing international effort to construct a Human Reference Atlas (HRA) of all cells in the human body.

Authors: Supriya Bidanta, Katy Börner, Bruce W. Herr II, Marcell Nagy, Katherine S. Gustilo, Rachel Bajema, Libby Maier, Roland Molontay, Griffin Weber

The repo is structured in the following way:

```
├── code
├── data
├── visualization
```

### Data

- Table 1: Supplemental file of vascular pathways. This data contains information about the 22 FTUs linked to the heart through vessels. 
  
### Code

This code generate a photo clickable poster that connects all the 22 FTUs of 5th release HRA with vasculature in butterfly design. This has nodes as anatomical structures and edges as the cell types of both female and male organs. The visualization is composed of two radial tree graphs: (1) The first graph contains the nested “partonomy” of the anatomical structures and cell types in the HRA. (2) The second graph contains all the blood vessels in the HRA, with the chambers of the heart in the center, and increasing smaller vessels more distal to the heart again branching outwards from the center

##### Prerequisite:
    - python
    - pycharm (recommended)
    - jupyter
    - packages: pyvis, networkx, datashader
    - Organ Data

To run the code, organ data was downloaded from ASCT+B Reporter in a JSON format to a folder. 
The code is segmented into four parts:
- First, get the whole organ data and formulate the data as per the list of organs one wants to visualize.
- Constructing a network out of the whole data, female data, and male data individually using vega visualisation. Downlaod the network in SVG and JSON format.
- Add the vasculature to the network we built in previous steps.
- Beautify and/or filter the visualization per the connections we have from the vasculature data.

### Visualization:
We have provided a 36" poster full image along with it two halves of the image as well. Since the poster is of 36",while taking a print we recommend to resize the two halves to 35.5" so that poster looks clean and aligned.



  
    
