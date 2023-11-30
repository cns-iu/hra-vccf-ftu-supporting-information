## Functional Tissue Units in the Human Reference Atlas

Supriya Bidanta<sup>1,4</sup>, Katy Börner<sup>1,4,5</sup>, Ellen M. Quardokus<sup>1</sup>, Bruce W. Herr II<sup>1</sup>, Marcell Nagy<sup>2</sup>, Katherine S. Gustilo<sup>1</sup>, Rachel Bajema<sup>1</sup>, Libby Maier<sup>1</sup>, Roland Molontay<sup>2</sup>, Griffin Weber<sup>3,5</sup>

<sup>1</sup> Indiana University, Bloomington, IN; 
<sup>2</sup> Budapest University of Technology and Economics, Budapest, Hungary;
<sup>3</sup> Harvard Medical School, Boston, MA

<sup>4</sup> Contributed equally (co-first authors)
<sup>5</sup> Corresponding authors 

Functional tissue units (FTUs) form the basic building blocks of organs and are important for understanding and modeling the healthy physiological function of the organ and changes that occur during disease states. In this first comprehensive catalog of 22 anatomically correct, nested functional tissue units (FTUs) from 10 healthy human organs, we document the definition, physical dimensions, blood vasculature connections, and cellular composition. All anatomy terms are mapped to the multi-species Uber-anatomy Ontology (UBERON) and Cell Ontology (CL) to support computational access via standardized metadata. The catalog includes datasets, illustrations, an online interactive FTU Explorer that supports exploration of published experimental datasets at single cell level, and a large printable poster illustrating how the blood vasculature connects the 22 FTUs in 10 organs. All data and code are freely available. The work is part of an ongoing international effort to construct a Human Reference Atlas (HRA) of all cells in the human body.

The repo is structured in the following way:

```
├── code
├── data
├── exploration
├── visualization
```

### Data
The data folder consists of information about the blood vasculature of all the 22 FTUs. Alng with the cell types, cell count, percentage of each cell in FTU, top 100 expressed genes for eight FTUs of three organ kidney, liver and lung, the folder has illustration(SVG, PNG, AI file format) and cell count information about small intestine - intestinal villus.
```
Table 1: Supplemental file of vascular pathways. This data contains information about the 22 FTUs linked to the heart through vessels.
Table 2: Supplemental file of experimental data for kidney, liver, and lung together with cell count, percentage per cell type per organ and mean gene expression values per cell type.
Table 3: Supplemental file of cell type per gene expression matrices for 11 FTUs with mapping between experimental data, 2D illustrations and ASCT+B table
```
  
### Code

The two codes generates a web compatible JOSN file for the interactive FTU explorer and a radial tree visualization of the anatomical structures partonomy. The butterly visualisation interlinks FTUs of the 5th HRA release via the vasculature. The visualization is composed of two radial tree graphs: (1) The first graph contains the nested “partonomy” of the anatomical structures in the HRA. (2) The second graph contains all the blood vessels in the HRA, with the chambers of the heart in the center, and increasing smaller vessels more distal to the heart again branching outwards from the center.

##### Prerequisite:
  - python (version > 3.9)
  - R-studio
  - pycharm (recommended)
  - jupyter
  - packages: pyvis, networkx, datashader, scanpy  ``` pip install pyvis, networkx, datashader, scanpy```
  - Organ Data

The interactive FTU Explorer code uses single-nucleus RNA sequencing data obtained from the <a href="https://www.ebi.ac.uk/gxa/sc/experiments?species=%22homo%20sapiens%22" target="_blank">Single Cell Expression Atlas website</a> for various organs that have anatomograms attached to them. The reference files are loaded to obtain the gene and cell type information, which is then used to create a dataframe that includes cell type, Ensemble ID, HGNC gene ID, HGNC gene symbol, and mean expression value. This dataframe is then converted to a JSON file that is utilized by the iFTU explorer portal.

To use the butterfly visualisation code, you'll need to download organ data from the <a href="https://hubmapconsortium.github.io/ccf-asct-reporter" target="_blank">ASCT+B Reporter</a> in JSON format. Once you have the data, you can use a graphics editor like Adobe Illustrator to combine the two networks and add a legend, title, FTUs, and any other information you need.

### Visualization
The directory features all files to view and print the 36" poster. To print the poster on a 36" printer, resize the two halves to 35.5".



  
    
