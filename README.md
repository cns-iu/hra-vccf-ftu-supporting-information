## Functional Tissue Units in the Human Reference Atlas

Supriya Bidanta<sup>1,4</sup>, Katy Börner<sup>1,4,5</sup>, Bruce W. Herr II<sup>1</sup>, Marcell Nagy<sup>2</sup>, Katherine S. Gustilo<sup>1</sup>, Rachel Bajema<sup>1</sup>, Libby Maier<sup>1</sup>, Roland Molontay<sup>2</sup>, Griffin Weber<sup>3,5</sup>

<sup>1</sup> Indiana University, Bloomington, IN; 
<sup>2</sup> Budapest University of Technology and Economics, Budapest, Hungary;
<sup>3</sup> Harvard Medical School, Boston, MA

<sup>4</sup> Contributed equally (co-first authors)
<sup>5</sup> Corresponding authors 

Functional tissue units (FTUs) form the basic building blocks of organs and are important for understanding and modeling the healthy physiological function of the organ and changes during disease states. In this first comprehensive catalog of FTUs, we document the definition, physical dimensions, vasculature, and cellular composition of 22 anatomically correct, nested functional tissue units (FTUs) in 10 healthy human organs. The catalog includes datasets, illustrations, an interactive online FTU explorer, and a large printable poster. All data and code are freely available. This is part of a larger ongoing international effort to construct a Human Reference Atlas (HRA) of all cells in the human body.

The repo is structured in the following way:

```
├── code
├── data
├── visualization
```

### Data

Table 1: Supplemental file of vascular pathways. This data contains information about the 22 FTUs linked to the heart through vessels. 
  
### Code

This code generates a radial tree visualization of the anatomical structures partonomy and interlinks FTUs of the 5th HRA release via the vasculature using a butterfly-like design. The visualization is composed of two radial tree graphs: (1) The first graph contains the nested “partonomy” of the anatomical structures in the HRA. (2) The second graph contains all the blood vessels in the HRA, with the chambers of the heart in the center, and increasing smaller vessels more distal to the heart again branching outwards from the center.

##### Prerequisite:
    - python
    - pycharm (recommended)
    - jupyter
    - packages: pyvis, networkx, datashader
    - Organ Data

The code expects organ data downloaded from the <a href="https://hubmapconsortium.github.io/ccf-asct-reporter" target="_blank">ASCT+B Reporter</a> in JSON format as input. It has four parts:
1. Compile data per the list of organs one wants to visualize.
2. Layout the anatomical structures partonomy as a radial tree using Vega. Download the network in SVG and JSON format.
3. Visualize the vasculature network.
4. Filter out nodes and edges as needed.

An graphics editor (e.g., Adobe Illustrator) was used to combine the two networks and to add legend, title, FTUs, and other information.

### Visualization
The directory features all files to view and print the 36" poster. To print the poster on a 36" printer, resize the two halves to 35.5".



  
    
